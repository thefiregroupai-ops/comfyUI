# Qwen Workflows

This folder contains ComfyUI workflows for Qwen-based image restaging, face swapping, image editing, skin-detail enhancement, and ControlNet processing.

## Workflows

| Workflow | Summary | JSON | Details |
| --- | --- | --- | --- |
| Qwen AI Real Skin v5 | Enhances skin texture and facial detail with Qwen and SeedVR2 processing. | [FIRE_AI_Real_Skin_V5_ComfyUI_Free.json](./FIRE_AI_Real_Skin_V5_ComfyUI_Free.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/qwen/ai-real-skin-v5/) |
| Qwen Classic Img2Img | Restages a source image with prompt conditioning. | [FIRE_IMG2IMG_CLASSIC.json](./FIRE_IMG2IMG_CLASSIC.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/qwen/img2img-classic/) |
| Qwen Faceswap v1 | Preserves identity while processing face swaps from an image folder. | [FIRE_QWEN_Faceswap_v1.json](./FIRE_QWEN_Faceswap_v1.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/qwen/faceswap-v1/) |
| Qwen Image Unleashed v2 | Provides image generation and prompt-driven editing with Qwen Image Edit Plus encoding. | [FIRE_QWEN_IMAGE_UNLEASHED_v2.json](./FIRE_QWEN_IMAGE_UNLEASHED_v2.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/qwen/image-unleashed-v2/) |
| Qwen Z-Base ControlNet and Sage Attention | Combines ControlNet preprocessing with a Sage Attention patch for Qwen rendering. | [FIRE_zbase+zit+control_v1.json](./FIRE_zbase+zit+control_v1.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/qwen/zbase-zit-control/) |

## Quick start

1. Download a workflow JSON from the table above.
2. Launch ComfyUI and load the JSON file onto the canvas.
3. Resolve any missing models or nodes shown by the workflow, then queue it. See [How to Install and Load a ComfyUI Workflow JSON File](https://thefiregroupai-ops.github.io/comfyUI/guides/how-to-install-comfyui-workflow-json/) for the site's import guidance.

## Support and community

For workflow discussion and setup support, visit the [FIRE AI Creator Lab](https://www.skool.com/fire-ai-creator-lab-9667).

## Licensing

This repository currently does not include a `LICENSE` file. Models and custom nodes referenced by these workflows retain their respective authors' licenses and terms; review those terms before use or redistribution.
