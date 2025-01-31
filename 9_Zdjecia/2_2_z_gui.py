import tkinter as tk
from tkinter import ttk, scrolledtext
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageTk
import threading


class StableDiffusionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stable Diffusion Interface")

        # Dostępne modele
        self.models = {
            "Stable Diffusion 1.4": "CompVis/stable-diffusion-v1-4",
            "Stable Diffusion 1.5": "runwayml/stable-diffusion-v1-5",
            "Stable Diffusion 2.0": "stabilityai/stable-diffusion-2",
            "Stable Diffusion 2.1": "stabilityai/stable-diffusion-2-1",
            "Stable Diffusion XL": "stabilityai/stable-diffusion-xl"
        }

        self.create_widgets()
        self.pipe = None

    def create_widgets(self):
        # Główny kontener
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Lewa strona - kontrolki
        controls_frame = ttk.LabelFrame(main_frame, text="Parametry", padding="5")
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Model selection
        ttk.Label(controls_frame, text="Model:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.model_var = tk.StringVar(value="Stable Diffusion 1.5")
        model_combo = ttk.Combobox(controls_frame, textvariable=self.model_var, values=list(self.models.keys()))
        model_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        # Prompt
        ttk.Label(controls_frame, text="Prompt:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.prompt_text = scrolledtext.ScrolledText(controls_frame, height=4, width=40)
        self.prompt_text.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        self.prompt_text.insert('1.0', "A futuristic city skyline at night, neon lights, ultra-detailed")

        # Negative prompt
        ttk.Label(controls_frame, text="Negative Prompt:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.neg_prompt_text = scrolledtext.ScrolledText(controls_frame, height=4, width=40)
        self.neg_prompt_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        self.neg_prompt_text.insert('1.0', "ugly, deformed, low quality, blurry")

        # Inference steps
        ttk.Label(controls_frame, text="Inference Steps:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.steps_var = tk.StringVar(value="10")
        steps_entry = ttk.Entry(controls_frame, textvariable=self.steps_var)
        steps_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)

        # Guidance scale
        ttk.Label(controls_frame, text="Guidance Scale:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.guidance_var = tk.StringVar(value="4.5")
        guidance_entry = ttk.Entry(controls_frame, textvariable=self.guidance_var)
        guidance_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)

        # Wymiary
        dims_frame = ttk.Frame(controls_frame)
        dims_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(dims_frame, text="Width:").grid(row=0, column=0, sticky=tk.W)
        self.width_var = tk.StringVar(value="512")
        width_entry = ttk.Entry(dims_frame, textvariable=self.width_var, width=10)
        width_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(dims_frame, text="Height:").grid(row=0, column=2, sticky=tk.W)
        self.height_var = tk.StringVar(value="512")
        height_entry = ttk.Entry(dims_frame, textvariable=self.height_var, width=10)
        height_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5)

        # Seed
        ttk.Label(controls_frame, text="Seed (optional):").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.seed_var = tk.StringVar(value="")
        seed_entry = ttk.Entry(controls_frame, textvariable=self.seed_var)
        seed_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=2)

        # Generate button
        self.generate_btn = ttk.Button(controls_frame, text="Generuj obraz", command=self.generate_image)
        self.generate_btn.grid(row=7, column=0, columnspan=2, pady=10)

        # Status
        self.status_var = tk.StringVar(value="Gotowy")
        status_label = ttk.Label(controls_frame, textvariable=self.status_var)
        status_label.grid(row=8, column=0, columnspan=2)

        # Prawa strona - podgląd obrazu
        preview_frame = ttk.LabelFrame(main_frame, text="Podgląd", padding="5")
        preview_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Przycisk zapisu
        self.save_btn = ttk.Button(preview_frame, text="Zapisz obraz", command=self.save_image)
        self.save_btn.grid(row=1, column=0, pady=10)
        self.save_btn.state(['disabled'])

    def generate_image(self):
        # Wyłącz przycisk podczas generowania
        self.generate_btn.state(['disabled'])
        self.status_var.set("Ładowanie modelu...")

        # Uruchom generowanie w osobnym wątku
        thread = threading.Thread(target=self._generate_image_thread)
        thread.start()

    def _generate_image_thread(self):
        try:
            # Pobierz parametry
            model_id = self.models[self.model_var.get()]

            # Załaduj model jeśli potrzeba
            if self.pipe is None or self.pipe.model_id != model_id:
                self.status_var.set("Ładowanie modelu...")
                device = "cuda" if torch.cuda.is_available() else "cpu"
                self.pipe = StableDiffusionPipeline.from_pretrained(model_id)
                self.pipe.to(device)

            # Przygotuj generator jeśli podano seed
            generator = None
            if self.seed_var.get():
                generator = torch.manual_seed(int(self.seed_var.get()))

            self.status_var.set("Generowanie obrazu...")

            # Generuj obraz
            with torch.autocast(self.pipe.device):
                output = self.pipe(
                    prompt=self.prompt_text.get('1.0', tk.END).strip(),
                    negative_prompt=self.neg_prompt_text.get('1.0', tk.END).strip(),
                    num_inference_steps=int(self.steps_var.get()),
                    guidance_scale=float(self.guidance_var.get()),
                    height=int(self.height_var.get()),
                    width=int(self.width_var.get()),
                    generator=generator
                )

            self.current_image = output.images[0]

            # Przygotuj podgląd
            preview = self.current_image.copy()
            preview.thumbnail((400, 400))  # Zmniejsz do rozmiaru podglądu
            photo = ImageTk.PhotoImage(preview)

            # Aktualizuj GUI w głównym wątku
            self.root.after(0, lambda: self._update_preview(photo))

        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Błąd: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.generate_btn.state(['!disabled']))

    def _update_preview(self, photo):
        self.preview_label.configure(image=photo)
        self.preview_label.image = photo  # Zachowaj referencję
        self.save_btn.state(['!disabled'])
        self.status_var.set("Gotowy")

    def save_image(self):
        if hasattr(self, 'current_image'):
            self.current_image.save("generated_image.png")
            self.status_var.set("Obraz zapisany jako 'generated_image.png'")


if __name__ == "__main__":
    root = tk.Tk()
    app = StableDiffusionGUI(root)
    root.mainloop()