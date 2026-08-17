# Contributing to FIRE ComfyUI Workflows

Thanks for helping improve the public workflow library. Contributions should be reproducible, clearly documented, and safe for readers to inspect before they install third-party nodes or models.

## Before opening a change

- Search existing issues and workflow pages for duplicates.
- Do not commit model weights, generated outputs, credentials, API keys, or private data.
- Confirm that you have permission to share the workflow JSON and any accompanying media.
- Keep third-party names factual and avoid implying endorsement.

## Add or update a workflow

1. Place the JSON file in the matching model-family directory.
2. Use a descriptive filename and preserve valid JSON formatting.
3. Update that directory's `README.md` table.
4. Add or update the workflow detail page under `workflows/<family>/<workflow>/index.html`.
5. Link the detail page from its family page and each relevant task page.
6. Add the canonical page URL to `sitemap.xml` with the date of the last significant content change.
7. Run the repository validator.

```bash
python3 scripts/validate_site.py
```

## Workflow documentation checklist

- A plain-language purpose and expected inputs/outputs
- Direct links to the JSON file and GitHub source
- Node count and custom-node names only when verified from the graph
- Model or checkpoint names only when present in the graph
- Known limitations or unverified requirements called out explicitly
- Related workflows linked with descriptive anchor text

Do not invent version support, VRAM requirements, speed claims, model paths, licenses, or benchmark results. If a fact has not been tested, label it as unverified.

## Site requirements

Every indexed HTML page must have:

- one unique `<title>` and one `<h1>`
- a useful meta description
- a self-referencing canonical URL
- Open Graph and Twitter card metadata
- valid JSON-LD
- descriptive image alt text and explicit image dimensions
- working internal links
- an entry in `sitemap.xml`

## Pull requests

Keep each pull request focused. Explain what changed, how you verified it, and which workflow or page is affected. Screenshots are useful for layout changes, but never include sensitive data.

By submitting a contribution, you confirm that you have the right to share it. A repository-wide license has not yet been selected, so maintainers may ask for explicit licensing clarification before accepting substantial contributions.
