import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QComboBox, QTextEdit, QSpinBox,
                             QDoubleSpinBox, QPushButton, QLineEdit, QGroupBox,
                             QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import io


class ImageGenerationThread(QThread):
    finished = pyqtSignal(Image.Image)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, params):
        super().__init__()
        self.params = params
        self.pipe = None

    def run(self):
        try:
            # Załaduj model jeśli potrzeba
            if self.pipe is None or self.pipe.model_id != self.params['model_id']:
                self.progress.emit("Ładowanie modelu...")
                device = "cuda" if torch.cuda.is_available() else "cpu"
                self.pipe = StableDiffusionPipeline.from_pretrained(self.params['model_id'])
                self.pipe.to(device)

            # Przygotuj generator jeśli podano seed
            generator = None
            if self.params['seed']:
                generator = torch.manual_seed(int(self.params['seed']))

            self.progress.emit("Generowanie obrazu...")

            # Generuj obraz
            with torch.autocast(self.pipe.device):
                output = self.pipe(
                    prompt=self.params['prompt'],
                    negative_prompt=self.params['negative_prompt'],
                    num_inference_steps=self.params['steps'],
                    guidance_scale=self.params['guidance_scale'],
                    height=self.params['height'],
                    width=self.params['width'],
                    generator=generator
                )

            self.finished.emit(output.images[0])

        except Exception as e:
            self.error.emit(str(e))


class StableDiffusionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stable Diffusion Interface")
        self.current_image = None
        self.initUI()

    def initUI(self):
        # Główny widget i layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Kontrolki (lewa strona)
        controls_group = QGroupBox("Parametry")
        controls_layout = QVBoxLayout()

        # Modele
        self.models = {
            "Stable Diffusion 1.4": "CompVis/stable-diffusion-v1-4",
            "Stable Diffusion 1.5": "runwayml/stable-diffusion-v1-5",
            "Stable Diffusion 2.0": "stabilityai/stable-diffusion-2",
            "Stable Diffusion 2.1": "stabilityai/stable-diffusion-2-1",
            "Stable Diffusion XL": "stabilityai/stable-diffusion-xl"
        }

        controls_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.models.keys())
        self.model_combo.setCurrentText("Stable Diffusion 1.5")
        controls_layout.addWidget(self.model_combo)

        # Prompt
        controls_layout.addWidget(QLabel("Prompt:"))
        self.prompt_text = QTextEdit()
        self.prompt_text.setPlaceholderText("Wpisz prompt...")
        self.prompt_text.setText("A futuristic city skyline at night, neon lights, ultra-detailed")
        self.prompt_text.setMaximumHeight(100)
        controls_layout.addWidget(self.prompt_text)

        # Negative prompt
        controls_layout.addWidget(QLabel("Negative Prompt:"))
        self.neg_prompt_text = QTextEdit()
        self.neg_prompt_text.setPlaceholderText("Wpisz negative prompt...")
        self.neg_prompt_text.setText("ugly, deformed, low quality, blurry")
        self.neg_prompt_text.setMaximumHeight(100)
        controls_layout.addWidget(self.neg_prompt_text)

        # Parametry numeryczne
        params_layout = QVBoxLayout()

        # Inference steps
        steps_layout = QHBoxLayout()
        steps_layout.addWidget(QLabel("Inference Steps:"))
        self.steps_spin = QSpinBox()
        self.steps_spin.setRange(1, 150)
        self.steps_spin.setValue(10)
        steps_layout.addWidget(self.steps_spin)
        params_layout.addLayout(steps_layout)

        # Guidance scale
        guidance_layout = QHBoxLayout()
        guidance_layout.addWidget(QLabel("Guidance Scale:"))
        self.guidance_spin = QDoubleSpinBox()
        self.guidance_spin.setRange(1.0, 20.0)
        self.guidance_spin.setValue(4.5)
        self.guidance_spin.setSingleStep(0.5)
        guidance_layout.addWidget(self.guidance_spin)
        params_layout.addLayout(guidance_layout)

        # Wymiary
        dims_layout = QHBoxLayout()
        dims_layout.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(128, 1024)
        self.width_spin.setValue(512)
        self.width_spin.setSingleStep(64)
        dims_layout.addWidget(self.width_spin)

        dims_layout.addWidget(QLabel("Height:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(128, 1024)
        self.height_spin.setValue(512)
        self.height_spin.setSingleStep(64)
        dims_layout.addWidget(self.height_spin)
        params_layout.addLayout(dims_layout)

        # Seed
        seed_layout = QHBoxLayout()
        seed_layout.addWidget(QLabel("Seed:"))
        self.seed_input = QLineEdit()
        self.seed_input.setPlaceholderText("Optional")
        seed_layout.addWidget(self.seed_input)
        params_layout.addLayout(seed_layout)

        controls_layout.addLayout(params_layout)

        # Przyciski
        self.generate_btn = QPushButton("Generuj")
        self.generate_btn.clicked.connect(self.generate_image)
        controls_layout.addWidget(self.generate_btn)

        self.save_btn = QPushButton("Zapisz")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        controls_layout.addWidget(self.save_btn)

        # Status
        self.status_label = QLabel("Gotowy")
        controls_layout.addWidget(self.status_label)

        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)

        # Podgląd (prawa strona)
        preview_group = QGroupBox("Podgląd")
        preview_layout = QVBoxLayout()
        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(512, 512)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.preview_label)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        self.setMinimumSize(1200, 800)

    def generate_image(self):
        self.generate_btn.setEnabled(False)
        self.status_label.setText("Przygotowanie...")

        # Zbierz parametry
        params = {
            'model_id': self.models[self.model_combo.currentText()],
            'prompt': self.prompt_text.toPlainText(),
            'negative_prompt': self.neg_prompt_text.toPlainText(),
            'steps': self.steps_spin.value(),
            'guidance_scale': self.guidance_spin.value(),
            'width': self.width_spin.value(),
            'height': self.height_spin.value(),
            'seed': self.seed_input.text()
        }

        # Utwórz i uruchom wątek
        self.thread = ImageGenerationThread(params)
        self.thread.finished.connect(self.handle_generation_finished)
        self.thread.error.connect(self.handle_generation_error)
        self.thread.progress.connect(self.status_label.setText)
        self.thread.start()

    def handle_generation_finished(self, image):
        self.current_image = image

        # Konwertuj PIL Image na QPixmap
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        qt_img = QImage.fromData(buffer.getvalue())
        pixmap = QPixmap.fromImage(qt_img)

        # Przeskaluj zachowując proporcje
        scaled_pixmap = pixmap.scaled(512, 512, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)

        self.preview_label.setPixmap(scaled_pixmap)
        self.save_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.status_label.setText("Gotowy")

    def handle_generation_error(self, error_msg):
        self.generate_btn.setEnabled(True)
        self.status_label.setText("Błąd")
        QMessageBox.critical(self, "Błąd", str(error_msg))

    def save_image(self):
        if self.current_image:
            try:
                self.current_image.save("generated_image.png")
                self.status_label.setText("Zapisano jako 'generated_image.png'")
            except Exception as e:
                QMessageBox.critical(self, "Błąd zapisu", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StableDiffusionGUI()
    window.show()
    sys.exit(app.exec())