#!/usr/bin/env python3
"""Validate the FIRE ComfyUI static site without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


BASE_URL = "https://thefiregroupai-ops.github.io/comfyUI/"
BASE_PARTS = urlsplit(BASE_URL)
BASE_PATH = BASE_PARTS.path

TITLE_MIN = 30
TITLE_MAX = 60
DESCRIPTION_MIN = 70
DESCRIPTION_MAX = 160

REQUIRED_OG_TAGS = (
    "og:type",
    "og:url",
    "og:title",
    "og:description",
    "og:image",
)
REQUIRED_TWITTER_TAGS = (
    "twitter:card",
    "twitter:url",
    "twitter:title",
    "twitter:description",
    "twitter:image",
)

IGNORED_PARTS = {".git", ".venv", "node_modules", "venv"}
REFERENCE_DEFINITION_RE = re.compile(
    r"^\s{0,3}\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))", re.MULTILINE
)
INLINE_CODE_RE = re.compile(r"(`+).*?\1")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
POSITIVE_INTEGER_RE = re.compile(r"^[1-9][0-9]*$")


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def split_xml_name(tag: str) -> tuple[str, str]:
    if tag.startswith("{") and "}" in tag:
        namespace, local_name = tag[1:].split("}", 1)
        return namespace, local_name
    if ":" in tag:
        prefix, local_name = tag.split(":", 1)
        return prefix, local_name
    return "", tag


def reject_nonstandard_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant {value!r}")


@dataclass(frozen=True)
class HtmlReference:
    tag: str
    attribute: str
    value: str
    line: int
    is_download: bool = False


@dataclass(frozen=True)
class HtmlImage:
    attributes: dict[str, str]
    line: int


@dataclass(frozen=True)
class LocalMapping:
    is_local: bool
    target: Path | None = None
    error: str | None = None


class StaticPageParser(HTMLParser):
    """Collect only the HTML state needed by this validator."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.titles: list[tuple[int, str]] = []
        self.h1_count = 0
        self.meta_by_name: dict[str, list[tuple[int, str]]] = defaultdict(list)
        self.meta_by_property: dict[str, list[tuple[int, str]]] = defaultdict(list)
        self.twitter_property_tags: list[tuple[int, str]] = []
        self.canonicals: list[tuple[int, str]] = []
        self.json_ld: list[tuple[int, str]] = []
        self.images: list[HtmlImage] = []
        self.references: list[HtmlReference] = []
        self.downloads_without_href: list[int] = []

        self._title_parts: list[str] | None = None
        self._title_line = 0
        self._json_ld_parts: list[str] | None = None
        self._json_ld_line = 0

    @staticmethod
    def _attribute_map(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {name.casefold(): value or "" for name, value in attrs}

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.casefold()
        attributes = self._attribute_map(attrs)
        line, _ = self.getpos()

        if tag == "title":
            if self._title_parts is not None:
                self.titles.append(
                    (self._title_line, normalize_text("".join(self._title_parts)))
                )
            self._title_parts = []
            self._title_line = line

        if tag == "h1":
            self.h1_count += 1

        if tag == "meta":
            content = attributes.get("content", "")
            name = attributes.get("name", "").casefold()
            property_name = attributes.get("property", "").casefold()
            if name:
                self.meta_by_name[name].append((line, content))
            if property_name:
                self.meta_by_property[property_name].append((line, content))
            if property_name.startswith("twitter:"):
                self.twitter_property_tags.append((line, property_name))

        if tag == "link":
            rel_tokens = {
                token.casefold() for token in attributes.get("rel", "").split()
            }
            if "canonical" in rel_tokens:
                self.canonicals.append((line, attributes.get("href", "")))

        if tag == "script" and attributes.get("type", "").casefold() == (
            "application/ld+json"
        ):
            if self._json_ld_parts is not None:
                self.json_ld.append(
                    (self._json_ld_line, "".join(self._json_ld_parts))
                )
            self._json_ld_parts = []
            self._json_ld_line = line

        if tag == "img":
            self.images.append(HtmlImage(attributes, line))

        is_download = "download" in attributes
        if is_download and "href" not in attributes:
            self.downloads_without_href.append(line)

        for attribute in ("href", "src"):
            if attribute in attributes:
                self.references.append(
                    HtmlReference(
                        tag=tag,
                        attribute=attribute,
                        value=attributes[attribute],
                        line=line,
                        is_download=is_download and attribute == "href",
                    )
                )

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self._title_parts is not None:
            self._title_parts.append(data)
        if self._json_ld_parts is not None:
            self._json_ld_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if tag == "title" and self._title_parts is not None:
            self.titles.append(
                (self._title_line, normalize_text("".join(self._title_parts)))
            )
            self._title_parts = None
        if tag == "script" and self._json_ld_parts is not None:
            self.json_ld.append((self._json_ld_line, "".join(self._json_ld_parts)))
            self._json_ld_parts = None

    def finish(self) -> None:
        """Preserve useful diagnostics even if a closing tag is omitted."""
        if self._title_parts is not None:
            self.titles.append(
                (self._title_line, normalize_text("".join(self._title_parts)))
            )
            self._title_parts = None
        if self._json_ld_parts is not None:
            self.json_ld.append((self._json_ld_line, "".join(self._json_ld_parts)))
            self._json_ld_parts = None


class SiteValidator:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.errors: list[str] = []
        self._seen_errors: set[str] = set()
        self.title_index: dict[str, list[tuple[Path, str]]] = defaultdict(list)
        self.description_index: dict[str, list[tuple[Path, str]]] = defaultdict(list)
        self.page_count = 0
        self.json_count = 0
        self.markdown_count = 0

    def display_path(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    def add_error(self, path: Path | str, message: str, line: int | None = None) -> None:
        location = self.display_path(path) if isinstance(path, Path) else path
        if line:
            location = f"{location}:{line}"
        formatted = f"{location}: {message}"
        if formatted not in self._seen_errors:
            self._seen_errors.add(formatted)
            self.errors.append(formatted)

    def ignored(self, path: Path) -> bool:
        try:
            parts = path.relative_to(self.root).parts
        except ValueError:
            return True
        return any(part in IGNORED_PARTS for part in parts)

    def expected_page_url(self, path: Path) -> str:
        relative = path.relative_to(self.root).as_posix()
        if relative == "index.html":
            return BASE_URL
        return BASE_URL + relative[: -len("index.html")]

    def parse_page(self, path: Path) -> StaticPageParser | None:
        parser = StaticPageParser()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
            parser.finish()
        except (OSError, UnicodeError) as exc:
            self.add_error(path, f"cannot read HTML as UTF-8: {exc}")
            return None
        except Exception as exc:  # HTMLParser extensions should still fail clearly.
            self.add_error(path, f"cannot parse HTML: {exc}")
            return None
        return parser

    def map_local_url(self, source: Path, raw_value: str) -> LocalMapping:
        value = raw_value.strip()
        try:
            parsed = urlsplit(value)
        except ValueError as exc:
            return LocalMapping(True, error=f"malformed URL {value!r}: {exc}")

        scheme = parsed.scheme.casefold()
        if scheme and scheme not in {"http", "https"}:
            return LocalMapping(False)

        if parsed.netloc or scheme in {"http", "https"}:
            host = (parsed.hostname or "").casefold()
            if host != (BASE_PARTS.hostname or "").casefold():
                return LocalMapping(False)
            site_path = unquote(parsed.path)
            base_without_slash = BASE_PATH.rstrip("/")
            if site_path.rstrip("/") == base_without_slash:
                relative_url_path = ""
            elif site_path.startswith(BASE_PATH):
                relative_url_path = site_path[len(BASE_PATH) :]
            else:
                return LocalMapping(
                    True,
                    error=(
                        f"same-host URL {value!r} is outside the site base "
                        f"{BASE_PATH!r}"
                    ),
                )
            candidate = self.root / relative_url_path
        elif parsed.path.startswith("/"):
            site_path = unquote(parsed.path)
            base_without_slash = BASE_PATH.rstrip("/")
            if site_path.rstrip("/") == base_without_slash:
                relative_url_path = ""
            elif site_path.startswith(BASE_PATH):
                relative_url_path = site_path[len(BASE_PATH) :]
            else:
                return LocalMapping(
                    True,
                    error=(
                        f"root-relative URL {value!r} is outside the site base "
                        f"{BASE_PATH!r}"
                    ),
                )
            candidate = self.root / relative_url_path
        else:
            relative_url_path = unquote(parsed.path)
            candidate = source.parent / relative_url_path if relative_url_path else source

        candidate = candidate.resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError:
            return LocalMapping(
                True, error=f"local URL {value!r} resolves outside the repository"
            )
        return LocalMapping(True, target=candidate)

    def validate_reference(
        self,
        source: Path,
        value: str,
        label: str,
        line: int | None = None,
        *,
        allow_directory: bool = False,
        html_href: bool = False,
    ) -> None:
        if not value.strip():
            if label != "href":
                self.add_error(source, f"{label} is empty", line)
            return

        mapping = self.map_local_url(source, value)
        if not mapping.is_local:
            return
        if mapping.error:
            self.add_error(source, f"broken local {label}: {mapping.error}", line)
            return
        if mapping.target is None:
            self.add_error(source, f"broken local {label}: cannot resolve {value!r}", line)
            return

        target = mapping.target
        if target.is_dir():
            if allow_directory:
                return
            if html_href and (target / "index.html").is_file():
                return
            self.add_error(
                source,
                f"broken local {label} {value!r}: target is a directory",
                line,
            )
            return
        if not target.is_file():
            self.add_error(
                source,
                (
                    f"broken local {label} {value!r}: "
                    f"{self.display_path(target)} does not exist"
                ),
                line,
            )

    def validate_common_html(self, path: Path, page: StaticPageParser) -> None:
        for line, payload in page.json_ld:
            try:
                json.loads(
                    payload,
                    parse_constant=reject_nonstandard_json_constant,
                )
            except json.JSONDecodeError as exc:
                self.add_error(
                    path,
                    (
                        "invalid JSON-LD "
                        f"at JSON line {exc.lineno}, column {exc.colno}: {exc.msg}"
                    ),
                    line,
                )
            except ValueError as exc:
                self.add_error(path, f"invalid JSON-LD: {exc}", line)

        for image in page.images:
            attrs = image.attributes
            if "alt" not in attrs:
                self.add_error(path, "image is missing an alt attribute", image.line)
            if "src" not in attrs or not attrs.get("src", "").strip():
                self.add_error(path, "image is missing a non-empty src", image.line)
            for dimension in ("width", "height"):
                value = attrs.get(dimension, "")
                if not value:
                    self.add_error(
                        path, f"image is missing a {dimension} attribute", image.line
                    )
                elif not POSITIVE_INTEGER_RE.fullmatch(value.strip()):
                    self.add_error(
                        path,
                        f"image {dimension} must be a positive integer, found {value!r}",
                        image.line,
                    )

        for line in page.downloads_without_href:
            self.add_error(path, "download link is missing href", line)

        for reference in page.references:
            if (
                reference.tag == "img"
                and reference.attribute == "src"
                and not reference.value.strip()
            ):
                continue  # The image-specific diagnostic above is clearer.
            label = "download href" if reference.is_download else reference.attribute
            self.validate_reference(
                path,
                reference.value,
                label,
                reference.line,
                html_href=reference.attribute == "href",
            )

    def validate_index_page(self, path: Path, page: StaticPageParser) -> None:
        if len(page.titles) != 1:
            self.add_error(
                path, f"expected exactly one <title>, found {len(page.titles)}"
            )
        else:
            line, title = page.titles[0]
            length = len(title)
            if not TITLE_MIN <= length <= TITLE_MAX:
                self.add_error(
                    path,
                    (
                        f"title length is {length}; expected "
                        f"{TITLE_MIN}-{TITLE_MAX} characters: {title!r}"
                    ),
                    line,
                )
            if title:
                self.title_index[title.casefold()].append((path, title))

        descriptions = page.meta_by_name.get("description", [])
        if len(descriptions) != 1:
            self.add_error(
                path,
                (
                    "expected exactly one meta description, found "
                    f"{len(descriptions)}"
                ),
            )
        else:
            line, description = descriptions[0]
            description = normalize_text(description)
            length = len(description)
            if not DESCRIPTION_MIN <= length <= DESCRIPTION_MAX:
                self.add_error(
                    path,
                    (
                        f"description length is {length}; expected "
                        f"{DESCRIPTION_MIN}-{DESCRIPTION_MAX} characters: "
                        f"{description!r}"
                    ),
                    line,
                )
            if description:
                self.description_index[description.casefold()].append(
                    (path, description)
                )

        expected_canonical = self.expected_page_url(path)
        if len(page.canonicals) != 1:
            self.add_error(
                path,
                f"expected exactly one canonical link, found {len(page.canonicals)}",
            )
        else:
            line, canonical = page.canonicals[0]
            if canonical.strip() != expected_canonical:
                self.add_error(
                    path,
                    (
                        f"canonical mismatch: expected {expected_canonical!r}, "
                        f"found {canonical.strip()!r}"
                    ),
                    line,
                )

        if page.h1_count != 1:
            self.add_error(path, f"expected exactly one H1, found {page.h1_count}")

        if not page.json_ld:
            self.add_error(path, "missing application/ld+json structured data")

        for tag_name in REQUIRED_OG_TAGS:
            values = page.meta_by_property.get(tag_name, [])
            if not any(content.strip() for _, content in values):
                self.add_error(
                    path,
                    f"missing required Open Graph property={tag_name!r}",
                )

        for tag_name in REQUIRED_TWITTER_TAGS:
            values = page.meta_by_name.get(tag_name, [])
            if not any(content.strip() for _, content in values):
                self.add_error(
                    path,
                    f"missing required Twitter name={tag_name!r}",
                )

        for tag_name, values in (
            ("og:url", page.meta_by_property.get("og:url", [])),
            ("twitter:url", page.meta_by_name.get("twitter:url", [])),
        ):
            for line, value in values:
                if value.strip() != expected_canonical:
                    self.add_error(
                        path,
                        f"{tag_name} mismatch: expected {expected_canonical!r}, found {value.strip()!r}",
                        line,
                    )

        for line, property_name in page.twitter_property_tags:
            self.add_error(
                path,
                (
                    f"Twitter tag {property_name!r} uses property=; "
                    "Twitter tags must use name="
                ),
                line,
            )

        for metadata_key, values in (
            ("og:image", page.meta_by_property.get("og:image", [])),
            ("twitter:image", page.meta_by_name.get("twitter:image", [])),
        ):
            for line, value in values:
                if value.strip():
                    self.validate_reference(
                        path, value, f"{metadata_key} asset", line
                    )

    def validate_duplicates(self) -> None:
        for label, index in (
            ("title", self.title_index),
            ("description", self.description_index),
        ):
            for entries in index.values():
                if len(entries) < 2:
                    continue
                paths = ", ".join(self.display_path(path) for path, _ in entries)
                self.add_error(
                    "site metadata",
                    f"duplicate {label} {entries[0][1]!r} used by: {paths}",
                )

    def validate_sitemap(self, index_pages: list[Path]) -> set[str]:
        sitemap_path = self.root / "sitemap.xml"
        expected_urls = {self.expected_page_url(path) for path in index_pages}
        if not sitemap_path.is_file():
            self.add_error(sitemap_path, "sitemap is missing")
            return set()

        try:
            sitemap_root = ET.parse(sitemap_path).getroot()
        except ET.ParseError as exc:
            self.add_error(sitemap_path, f"invalid XML: {exc}")
            return set()
        except OSError as exc:
            self.add_error(sitemap_path, f"cannot read sitemap: {exc}")
            return set()

        forbidden_counts: dict[str, int] = defaultdict(int)
        listed_urls: list[str] = []
        for element in sitemap_root.iter():
            namespace, local_name = split_xml_name(element.tag)
            if local_name in {"priority", "changefreq"}:
                forbidden_counts[local_name] += 1
            if local_name == "title" and "image" in namespace.casefold():
                forbidden_counts["image:title"] += 1
            if local_name != "url":
                continue
            loc_values = [
                (child.text or "").strip()
                for child in list(element)
                if split_xml_name(child.tag)[1] == "loc"
            ]
            if len(loc_values) != 1 or not loc_values[0]:
                self.add_error(
                    sitemap_path,
                    f"each <url> must have one non-empty <loc>; found {loc_values!r}",
                )
            else:
                listed_urls.append(loc_values[0])

            lastmod_values = [
                (child.text or "").strip()
                for child in list(element)
                if split_xml_name(child.tag)[1] == "lastmod"
            ]
            if len(lastmod_values) != 1:
                self.add_error(
                    sitemap_path,
                    f"each <url> must have one <lastmod>; found {lastmod_values!r}",
                )
            elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", lastmod_values[0]):
                self.add_error(
                    sitemap_path,
                    f"lastmod must use YYYY-MM-DD: {lastmod_values[0]!r}",
                )
            else:
                try:
                    date.fromisoformat(lastmod_values[0])
                except ValueError:
                    self.add_error(
                        sitemap_path,
                        f"lastmod is not a real calendar date: {lastmod_values[0]!r}",
                    )

        for tag_name, count in sorted(forbidden_counts.items()):
            self.add_error(
                sitemap_path,
                f"contains {count} forbidden <{tag_name}> element(s)",
            )

        occurrences: dict[str, int] = defaultdict(int)
        for url in listed_urls:
            occurrences[url] += 1
        for url, count in sorted(occurrences.items()):
            if count > 1:
                self.add_error(
                    sitemap_path, f"URL appears {count} times in sitemap: {url}"
                )

        actual_urls = set(listed_urls)
        for missing in sorted(expected_urls - actual_urls):
            self.add_error(sitemap_path, f"missing index.html page URL: {missing}")
        for extra in sorted(actual_urls - expected_urls):
            self.add_error(sitemap_path, f"unexpected URL not backed by index.html: {extra}")
        return actual_urls

    def validate_robots(self) -> None:
        path = self.root / "robots.txt"
        if not path.is_file():
            self.add_error(path, "robots.txt is missing")
            return
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self.add_error(path, f"cannot read robots.txt as UTF-8: {exc}")
            return
        expected = f"Sitemap: {BASE_URL}sitemap.xml"
        if expected.casefold() not in content.casefold():
            self.add_error(path, f"missing sitemap directive {expected!r}")
        if re.search(r"(?im)^\s*disallow:\s*/\s*$", content):
            self.add_error(path, "robots.txt blocks the entire site")

    def validate_404(self, sitemap_urls: set[str]) -> None:
        path = self.root / "404.html"
        if not path.is_file():
            return
        page = self.parse_page(path)
        if page is None:
            return
        self.validate_common_html(path, page)
        robots_values = page.meta_by_name.get("robots", [])
        is_noindex = any(
            "noindex"
            in {
                token.casefold()
                for token in re.split(r"[\s,]+", content.strip())
                if token
            }
            for _, content in robots_values
        )
        if not is_noindex:
            self.add_error(path, "404 page must declare meta robots noindex")
        expected_404_url = BASE_URL + "404.html"
        if expected_404_url in sitemap_urls:
            self.add_error(path, "404 page must not be listed in sitemap.xml")

    def validate_json_files(self) -> None:
        for path in sorted(self.root.rglob("*.json")):
            if not path.is_file() or self.ignored(path):
                continue
            self.json_count += 1
            try:
                payload = path.read_text(encoding="utf-8")
                json.loads(
                    payload,
                    parse_constant=reject_nonstandard_json_constant,
                )
            except json.JSONDecodeError as exc:
                self.add_error(
                    path,
                    (
                        f"invalid workflow JSON at line {exc.lineno}, "
                        f"column {exc.colno}: {exc.msg}"
                    ),
                )
            except (OSError, UnicodeError, ValueError) as exc:
                self.add_error(path, f"invalid workflow JSON: {exc}")

    @staticmethod
    def markdown_without_code(markdown: str) -> str:
        output: list[str] = []
        fence_character = ""
        fence_length = 0
        for line in markdown.splitlines():
            fence_match = FENCE_RE.match(line)
            if fence_character:
                if (
                    fence_match
                    and fence_match.group(1)[0] == fence_character
                    and len(fence_match.group(1)) >= fence_length
                ):
                    fence_character = ""
                    fence_length = 0
                output.append("")
                continue
            if fence_match:
                fence_character = fence_match.group(1)[0]
                fence_length = len(fence_match.group(1))
                output.append("")
                continue
            output.append(INLINE_CODE_RE.sub("", line))
        return "\n".join(output)

    @staticmethod
    def inline_markdown_destinations(markdown: str) -> list[str]:
        """Extract inline link destinations while allowing balanced parentheses."""
        destinations: list[str] = []
        cursor = 0
        while True:
            marker = markdown.find("](", cursor)
            if marker == -1:
                break
            start = marker + 2
            while start < len(markdown) and markdown[start].isspace():
                start += 1
            if start >= len(markdown):
                break

            if markdown[start] == "<":
                end = markdown.find(">", start + 1)
                if end != -1:
                    destinations.append(markdown[start + 1 : end])
                    cursor = end + 1
                    continue

            depth = 0
            escaped = False
            destination: list[str] = []
            position = start
            while position < len(markdown):
                character = markdown[position]
                if escaped:
                    destination.append(character)
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == "(":
                    depth += 1
                    destination.append(character)
                elif character == ")":
                    if depth == 0:
                        break
                    depth -= 1
                    destination.append(character)
                elif character.isspace() and depth == 0:
                    break
                else:
                    destination.append(character)
                position += 1
            destinations.append("".join(destination))
            cursor = max(position + 1, start + 1)
        return destinations

    def validate_markdown_files(self) -> None:
        for path in sorted(self.root.rglob("*.md")):
            if not path.is_file() or self.ignored(path):
                continue
            self.markdown_count += 1
            try:
                markdown = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                self.add_error(path, f"cannot read Markdown as UTF-8: {exc}")
                continue

            markdown = self.markdown_without_code(markdown)
            destinations = self.inline_markdown_destinations(markdown)
            destinations.extend(
                angle or plain
                for angle, plain in REFERENCE_DEFINITION_RE.findall(markdown)
            )
            for destination in destinations:
                self.validate_reference(
                    path,
                    destination,
                    "Markdown link",
                    allow_directory=True,
                )

            raw_html = StaticPageParser()
            try:
                raw_html.feed(markdown)
                raw_html.close()
            except Exception as exc:
                self.add_error(path, f"cannot parse embedded Markdown HTML: {exc}")
                continue
            for reference in raw_html.references:
                self.validate_reference(
                    path,
                    reference.value,
                    f"Markdown HTML {reference.attribute}",
                    reference.line,
                    allow_directory=reference.attribute == "href",
                )

    def run(self) -> int:
        index_pages = sorted(
            path
            for path in self.root.rglob("index.html")
            if path.is_file() and not self.ignored(path)
        )
        if not index_pages:
            self.add_error(self.root, "no index.html pages found")

        for path in index_pages:
            page = self.parse_page(path)
            if page is None:
                continue
            self.page_count += 1
            self.validate_common_html(path, page)
            self.validate_index_page(path, page)

        self.validate_duplicates()
        sitemap_urls = self.validate_sitemap(index_pages)
        self.validate_robots()
        self.validate_404(sitemap_urls)
        self.validate_json_files()
        self.validate_markdown_files()

        if self.errors:
            print(f"Site validation failed with {len(self.errors)} error(s):", file=sys.stderr)
            for error in sorted(self.errors):
                print(f"- {error}", file=sys.stderr)
            return 1

        print(
            "Site validation passed: "
            f"{self.page_count} indexed HTML pages, "
            f"{self.json_count} JSON files, and "
            f"{self.markdown_count} Markdown files checked."
        )
        return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of scripts/)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.root.is_dir():
        print(f"Repository root does not exist: {args.root}", file=sys.stderr)
        return 2
    return SiteValidator(args.root).run()


if __name__ == "__main__":
    raise SystemExit(main())
