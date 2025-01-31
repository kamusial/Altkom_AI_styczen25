import torch
from diffusers import StableDiffusionPipeline

# Ścieżka lub nazwa modelu, np. Stable Diffusion 2.1:
model_id = 'CompVis/stable-diffusion-v1-4'
           #"stabilityai/stable-diffusion-2-1"

pipe = StableDiffusionPipeline.from_pretrained(model_id,
                                               torch_dtype=torch.float16)
pipe.to("cpu")
prompt = 'small dog eating chips'

image = pipe(prompt, num_inference_Steps=10,
             height = 256,
             width = 256).images[0]

image.save('small_dog.png')




