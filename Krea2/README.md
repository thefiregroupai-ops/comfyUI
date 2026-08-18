# Krea2 Workflows

This folder contains ComfyUI workflows for Krea2 depth control, identity editing, multi-reference conditioning, and image comparison.

## Workflows

| Workflow | Summary | JSON | Details |
| --- | --- | --- | --- |
| Krea2 ControlNet Depth Anything v3 | Uses depth guidance for image generation and structural control. | [FIRE_KERA_2_CONTROLNET_WORKFLOW_1.json](./FIRE_KERA_2_CONTROLNET_WORKFLOW_1.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/krea2/controlnet-depth/) |
| Krea2 Depth Control and Image Compare | Applies depth conditioning and provides a before-and-after image comparison. | [FIRE_Krea2_Depth_Control_1.json](./FIRE_Krea2_Depth_Control_1.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/krea2/depth-control-compare/) |
| Krea2 Identity Edit v1.2 Grounded Encode | Restages identity and edits facial features from two image inputs. | [FIRE_Krea2_Identity_Edit_V1.json](./FIRE_Krea2_Identity_Edit_V1.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/krea2/identity-edit-v1/) |
| Krea2 T2I Multi-Reference Selector | Selects from multiple reference photos for text-to-image generation and face-detail refinement with explicit LoRA loaders to review. | [FIRE_Krea2_No_Lora.json](./FIRE_Krea2_No_Lora.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/krea2/no-lora-t2i/) |

## Quick start

1. Download a workflow JSON from the table above.
2. Launch ComfyUI and load the JSON file onto the canvas.
3. Resolve any missing models or nodes shown by the workflow, then queue it. See [How to Install and Load a ComfyUI Workflow JSON File](https://thefiregroupai-ops.github.io/comfyUI/guides/how-to-install-comfyui-workflow-json/) for the site's import guidance.

## Support and community

For workflow discussion and setup support, visit the [FIRE AI Creator Lab](https://www.skool.com/fire-ai-creator-lab-9667).

## Licensing

This repository currently does not include a `LICENSE` file. Models and custom nodes referenced by these workflows retain their respective authors' licenses and terms; review those terms before use or redistribution.
