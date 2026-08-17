# FIRE ComfyUI Workflows

Free ComfyUI workflow JSONs for AI image generation, image editing, character consistency, video generation, LoRA dataset creation, and upscaling.

[![Site validation](https://github.com/thefiregroupai-ops/comfyUI/actions/workflows/validate-site.yml/badge.svg)](https://github.com/thefiregroupai-ops/comfyUI/actions/workflows/validate-site.yml)
[![GitHub stars](https://img.shields.io/github/stars/thefiregroupai-ops/comfyUI?style=flat-square&color=ff5500)](https://github.com/thefiregroupai-ops/comfyUI/stargazers)
[![Browse workflows](https://img.shields.io/badge/Browse-GitHub%20Pages-ff7700?style=flat-square)](https://thefiregroupai-ops.github.io/comfyUI/)

## Start here

1. [Browse the visual workflow library](https://thefiregroupai-ops.github.io/comfyUI/) or choose a family below.
2. Download the workflow's `.json` file.
3. Open [ComfyUI](https://github.com/Comfy-Org/ComfyUI), then drag the JSON file onto the canvas.
4. If nodes are missing, use [ComfyUI-Manager](https://github.com/Comfy-Org/ComfyUI-Manager) to identify them and review the workflow page before installing third-party code.

New to workflow files? Read the [ComfyUI workflow JSON installation guide](https://thefiregroupai-ops.github.io/comfyUI/guides/how-to-install-comfyui-workflow-json/).

## Workflow library

| Model or tool family | Workflows | Typical tasks | Browse |
|---|---:|---|---|
| Ideogram & Flux 2 Klein | 3 | Text-to-image, reference conditioning, prompt refinement | [Open family](https://thefiregroupai-ops.github.io/comfyUI/workflows/ideogram-flux/) |
| Krea2 | 4 | Identity editing, depth control, multi-reference generation | [Open family](https://thefiregroupai-ops.github.io/comfyUI/workflows/krea2/) |
| LoRA Dataset Tools | 1 | Character dataset preparation | [Open family](https://thefiregroupai-ops.github.io/comfyUI/workflows/lora-dataset-tools/) |
| MiniMax-H3 Video | 3 | First/last-frame video, auto-aspect video, cinema/audio reference | [Open family](https://thefiregroupai-ops.github.io/comfyUI/workflows/minimax-h3-video/) |
| Qwen | 5 | Image editing, face swap, skin realism, ControlNet | [Open family](https://thefiregroupai-ops.github.io/comfyUI/workflows/qwen/) |
| Upscalers & Tools | 2 | Image upscaling and finishing | [Open family](https://thefiregroupai-ops.github.io/comfyUI/workflows/upscalers-tools/) |
| Wan Video | 2 | Image-to-video extension and talking-head video | [Open family](https://thefiregroupai-ops.github.io/comfyUI/workflows/wan-video/) |

You can also [browse all 20 workflows by task](https://thefiregroupai-ops.github.io/comfyUI/workflows/).

## Technical guides

- [Import and load a ComfyUI workflow JSON](https://thefiregroupai-ops.github.io/comfyUI/guides/how-to-install-comfyui-workflow-json/)
- [Choose a character-consistency workflow](https://thefiregroupai-ops.github.io/comfyUI/guides/comfyui-character-consistency-guide/)
- [Krea2 identity and depth workflows](https://thefiregroupai-ops.github.io/comfyUI/guides/krea2-comfyui-character-consistency/)
- [MiniMax H3 video workflows](https://thefiregroupai-ops.github.io/comfyUI/guides/minimax-h3-comfyui/)
- [Qwen face swap and skin realism](https://thefiregroupai-ops.github.io/comfyUI/guides/qwen-comfyui-faceswap-guide/)
- [Wan image-to-video workflows](https://thefiregroupai-ops.github.io/comfyUI/guides/comfyui-wan-video-guide/)

## What is included

- ComfyUI workflow graphs in JSON format
- Static workflow detail pages with direct downloads
- Model-family and task-based comparison pages
- Technical guides, `robots.txt`, an XML sitemap, and structured data

Model weights, custom-node packages, and ComfyUI itself are not bundled. A workflow may reference third-party components that need to be downloaded separately.

## Repository structure

```text
<model-family>/       Workflow JSON files and a family README
workflows/            Search-friendly family, task, and workflow pages
guides/               Technical guides
assets/               Site images and shared styles
index.html            GitHub Pages homepage
sitemap.xml           Published-page inventory
scripts/              Local validation tools
```

## Safety and compatibility

ComfyUI workflows can reference arbitrary custom nodes. Review each missing-node package and its source before installation. Keep ComfyUI, custom nodes, and model files in an isolated environment, and do not load workflow files from sources you do not trust.

Names such as ComfyUI, Flux, Ideogram, Krea, MiniMax, Qwen, SeedVR2, and Wan belong to their respective owners. Their inclusion describes compatibility; it does not imply affiliation or endorsement. Showcase imagery illustrates creative use cases and is not a guarantee that every workflow will reproduce an identical result.

## Contributing

Corrections, compatibility notes, and new public workflows are welcome. Read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening an issue or pull request. Every change is checked for valid JSON, local links, page metadata, structured data, and sitemap coverage.

## License status

This repository does not currently include a repository-wide license. Public access does not by itself grant permission to copy, redistribute, or create derivative works. The repository owner should add an explicit license before describing the project as open source.

Referenced models, custom nodes, fonts, and other third-party components retain their own licenses and terms.

## Community and support

- [FIRE AI Creator Lab on Skool — free community](https://www.skool.com/fire-ai-creator-lab-9667)
- [FIRE Group AI Ops on GitHub](https://github.com/thefiregroupai-ops)

Maintained by FIRE Group AI Ops.
