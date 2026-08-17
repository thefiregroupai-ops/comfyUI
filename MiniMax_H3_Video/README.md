# MiniMax-H3 Video Workflows

This folder contains ComfyUI workflows for MiniMax-H3 video generation with frame control, automatic aspect handling, interpolation, and audio-reference inputs.

## Workflows

| Workflow | Summary | JSON | Details |
| --- | --- | --- | --- |
| MiniMax-H3 First and Last Frame | Generates controlled animation between supplied start and end frames with duration controls. | [FIRE_MINIMAX_H3_FIRSTLASTFRAME.json](./FIRE_MINIMAX_H3_FIRSTLASTFRAME.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/minimax-h3-video/first-last-frame/) |
| MiniMax-H3 v3 Auto-Aspect FP8 | Applies automatic aspect-ratio scaling in a MiniMax-H3 FP8 video pipeline. | [FIRE_MiniMax_H3_V3_AutoAspect_FP8_AB.json](./FIRE_MiniMax_H3_V3_AutoAspect_FP8_AB.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/minimax-h3-video/v3-auto-aspect-fp8/) |
| MiniMax-H3 Top Cinema and Audio Reference | Supports custom dimensions, RIFE frame interpolation, and audio-reference inputs for video rendering. | [FIRE_minimax_top.json](./FIRE_minimax_top.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/minimax-h3-video/top-cinema/) |

## Quick start

1. Download a workflow JSON from the table above.
2. Launch ComfyUI and load the JSON file onto the canvas.
3. Resolve any missing models or nodes shown by the workflow, then queue it. See [How to Install and Load a ComfyUI Workflow JSON File](https://thefiregroupai-ops.github.io/comfyUI/guides/how-to-install-comfyui-workflow-json/) for the site's import guidance.

## Support and community

For workflow discussion and setup support, visit the [FIRE AI Creator Lab](https://www.skool.com/fire-ai-creator-lab-9667).

## Licensing

This repository currently does not include a `LICENSE` file. Models and custom nodes referenced by these workflows retain their respective authors' licenses and terms; review those terms before use or redistribution.
