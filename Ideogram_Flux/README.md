# Ideogram and Flux Workflows

This folder contains ComfyUI workflows for Flux 2 Klein text-to-image generation and Ideogram-based reference conditioning and prompt refinement.

## Workflows

| Workflow | Summary | JSON | Details |
| --- | --- | --- | --- |
| Flux 2 Klein FP8 Text-to-Image | Runs sequential prompt lists with random-noise seed control. | [FIRE_Flux_2_Klein_FP8_3.json](./FIRE_Flux_2_Klein_FP8_3.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/ideogram-flux/flux-2-klein-fp8/) |
| Ideogram 4 + LoRA Single Reference | Conditions generation from one reference image with dual model guiders and CFG override. | [FIRE_IDEO+LORA_Single_Reference_2.json](./FIRE_IDEO+LORA_Single_Reference_2.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/ideogram-flux/ideogram-lora-single-reference/) |
| Ideogram Director v10 LLM Refiner | Combines prompt direction and resolution setup with local-LLM prompt refinement. | [FIRE_ideogramDirector_v10.json](./FIRE_ideogramDirector_v10.json) | [View workflow details](https://thefiregroupai-ops.github.io/comfyUI/workflows/ideogram-flux/ideogram-director-v10/) |

## Quick start

1. Download a workflow JSON from the table above.
2. Launch ComfyUI and load the JSON file onto the canvas.
3. Resolve any missing models or nodes shown by the workflow, then queue it. See [How to Install and Load a ComfyUI Workflow JSON File](https://thefiregroupai-ops.github.io/comfyUI/guides/how-to-install-comfyui-workflow-json/) for the site's import guidance.

## Support and community

For workflow discussion and setup support, visit the [FIRE AI Creator Lab](https://www.skool.com/fire-ai-creator-lab-9667).

## Licensing

This repository currently does not include a `LICENSE` file. Models and custom nodes referenced by these workflows retain their respective authors' licenses and terms; review those terms before use or redistribution.
