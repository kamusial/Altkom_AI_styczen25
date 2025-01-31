import torch
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image

model_id_inpaint = "runwayml/stable-diffusion-inpainting"
inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained(model_id_inpaint)
inpaint_pipe.to("cpu")

# Wczytujemy oryginalny obraz (init_image) i maskę (mask_image)
init_image = Image.open("landscape_cpu.jpg").convert("RGB")
mask_image = Image.open("mask_landscape_cpu.jpg").convert("RGB")
# mask_image - białe obszary to te, które chcemy zastąpić

prompt = "sun in sunny day"

image_inpainted = inpaint_pipe(
    prompt=prompt,
    image=init_image,
    mask_image=mask_image,
    num_inference_steps=10,
    guidance_scale=7.5
).images[0]

image_inpainted.save("inpainting_result_cpu.png")
