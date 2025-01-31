import torch
from diffusers import StableDiffusionPipeline

# Ścieżka lub nazwa modelu, np. Stable Diffusion 2.1:
model_id = 'CompVis/stable-diffusion-v1-4'
           #"stabilityai/stable-diffusion-2-1"

# Ładujemy pipeline z wagami modelu.
# Możesz dopisać argument: torch_dtype=torch.float32, aby wymusić 32-bit na CPU.
pipe = StableDiffusionPipeline.from_pretrained(model_id)

# Przenosimy model NA CPU (domyślnie, bez "cuda" i GPU).
pipe.to("cpu")

prompt = "A beautiful landscape with mountains and a lake, sunset light"

# Generowanie obrazu:
image = pipe(prompt, num_inference_Steps=10).images[0]

image.save("landscape_cpu.jpg")