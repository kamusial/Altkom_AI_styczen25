import torch
from diffusers import StableDiffusionPipeline

# ------------------------------------------------------
# 1. Konfiguracja modelu
# ------------------------------------------------------
model_id = "runwayml/stable-diffusion-v1-5"

# CompVis/stable-diffusion-v1-4
# CompVis/stable-diffusion-v1-5
# stabilityai/stable-diffusion-2
# stabilityai/stable-diffusion-2-1
# stabilityai/stable-diffusion-xl

# Ładujemy pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    # torch_dtype=torch.float16  # Wymaga GPU obsługującego FP16
    # Można pominąć torch_dtype, jeśli działasz na CPU lub w float32
)

# Wybór CPU albo GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe.to(device)

# ------------------------------------------------------
# 2. Definicja parametrów generowania
# ------------------------------------------------------
prompt = "A futuristic city skyline at night, neon lights, ultra-detailed"
negative_prompt = "ugly, deformed, low quality, blurry"

num_inference_steps = 10      # Liczba kroków próbkowania (domyślnie ~50)
guidance_scale = 4.5          # Siła powiązania z promptem
height = 512               # Wysokość wyjściowego obrazu
width = 512              # Szerokość wyjściowego obrazu

# Generator ustawia seed (opcjonalnie, dla powtarzalności)
# generator = torch.manual_seed(42)

# ------------------------------------------------------
# 3. Generowanie obrazu z użyciem pipeline
# ------------------------------------------------------
with torch.autocast(device):  # automatyczne zarządzanie precyzją (FP16)
    output = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        height=height,
        width=width,
        # generator=generator,  # odkomentuj, jeśli chcesz powtarzalny wynik
    )

# Z wyniku pipeline otrzymujemy listę obrazów
image = output.images[0]

# ------------------------------------------------------
# 4. Zapis obrazu
# ------------------------------------------------------
image.save("generated_city_neon.png")

print("Obraz został zapisany.")

