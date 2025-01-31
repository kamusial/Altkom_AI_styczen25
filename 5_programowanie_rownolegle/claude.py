import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
from pygments.styles.dracula import comment
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CSVAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizator CSV")
        self.root.geometry("900x700")

        # Elementy interfejsu
        self.create_widgets()

        # Zmienne do przechowywania danych
        self.df = None
        self.model = None
        self.scaler = StandardScaler()

    def create_widgets(self):
        # Frame główny
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sekcja wczytywania pliku
        file_frame = tk.LabelFrame(main_frame, text="Wczytywanie pliku", padx=5, pady=5)
        file_frame.pack(fill=tk.X, pady=5)

        # Ścieżka do pliku
        path_frame = tk.Frame(file_frame)
        path_frame.pack(fill=tk.X, pady=5)

        self.path_var = tk.StringVar()
        path_entry = tk.Entry(path_frame, textvariable=self.path_var, width=50)
        path_entry.pack(side=tk.LEFT, padx=5)

        browse_btn = tk.Button(path_frame, text="Przeglądaj", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT, padx=5)

        # Opcje wczytywania
        options_frame = tk.Frame(file_frame)
        options_frame.pack(fill=tk.X, pady=5)

        # Separator
        tk.Label(options_frame, text="Separator:").pack(side=tk.LEFT, padx=5)
        self.separator_var = tk.StringVar(value=',')
        separator_entry = tk.Entry(options_frame, textvariable=self.separator_var, width=3)
        separator_entry.pack(side=tk.LEFT, padx=5)

        # Kodowanie
        tk.Label(options_frame, text="Kodowanie:").pack(side=tk.LEFT, padx=5)
        self.encoding_var = tk.StringVar(value='utf-8')
        encoding_choices = ['utf-8', 'latin1', 'ascii', 'iso-8859-1']
        encoding_menu = ttk.Combobox(options_frame, textvariable=self.encoding_var, values=encoding_choices, width=10)
        encoding_menu.pack(side=tk.LEFT, padx=5)

        # Przycisk wczytywania
        load_btn = tk.Button(file_frame, text="Wczytaj", command=self.load_data)
        load_btn.pack(pady=5)

        # Sekcja analizy
        analysis_frame = tk.LabelFrame(main_frame, text="Analiza danych", padx=5, pady=5)
        analysis_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Dodanie scrollbara do tekstu
        text_frame = tk.Frame(analysis_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.info_text = tk.Text(text_frame, height=15, width=70, yscrollcommand=scrollbar.set)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.info_text.yview)

        # Sekcja konfiguracji modelu
        model_frame = tk.LabelFrame(main_frame, text="Konfiguracja modelu", padx=5, pady=5)
        model_frame.pack(fill=tk.X, pady=5)

        # Wybór kolumny z etykietami
        label_frame = tk.Frame(model_frame)
        label_frame.pack(fill=tk.X, pady=5)

        tk.Label(label_frame, text="Kolumna z etykietami:").pack(side=tk.LEFT, padx=5)
        self.target_column_var = tk.StringVar()
        self.target_column_menu = ttk.Combobox(label_frame, textvariable=self.target_column_var, width=20)
        self.target_column_menu.pack(side=tk.LEFT, padx=5)

        # Przycisk trenowania
        train_btn = tk.Button(model_frame, text="Trenuj model", command=self.train_model)
        train_btn.pack(pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
        )
        if filename:
            self.path_var.set(filename)

    def load_data(self):
        try:
            file_path = self.path_var.get()
            if not file_path:
                raise ValueError("Wybierz plik CSV!")

            # Próba wczytania pliku z różnymi opcjami
            try:
                self.df = pd.read_csv(
                    file_path,
                    sep=self.separator_var.get(),
                    encoding=self.encoding_var.get(),
                    comment='#'
                )
            except UnicodeDecodeError:
                # Jeśli nie udało się z wybranym kodowaniem, próbujemy innych
                for encoding in ['utf-8', 'latin1', 'iso-8859-1', 'cp1250']:
                    try:
                        self.df = pd.read_csv(file_path, sep=self.separator_var.get(), encoding=encoding)
                        self.encoding_var.set(encoding)
                        break
                    except UnicodeDecodeError:
                        continue

            if self.df is None:
                raise ValueError("Nie udało się wczytać pliku z żadnym kodowaniem!")

            # Aktualizacja listy kolumn
            self.update_column_list()

            # Analiza danych
            self.analyze_data()

            messagebox.showinfo("Sukces", "Plik został wczytany pomyślnie!")

        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd wczytywania pliku: {str(e)}")

    def update_column_list(self):
        if self.df is not None:
            self.target_column_menu['values'] = list(self.df.columns)
            if len(self.df.columns) > 0:
                self.target_column_var.set(self.df.columns[-1])

    def analyze_data(self):
        if self.df is None:
            return

        # Analiza brakujących danych
        missing_data = self.df.isnull().sum()
        total_rows = len(self.df)

        # Podstawowe informacje o danych
        info = f"Analiza danych:\n\n"
        info += f"Liczba wierszy: {total_rows}\n"
        info += f"Liczba kolumn: {len(self.df.columns)}\n"
        info += f"Kolumny: {', '.join(self.df.columns)}\n\n"

        # Informacje o typach danych
        info += "Typy danych:\n"
        for column, dtype in self.df.dtypes.items():
            info += f"{column}: {dtype}\n"

        info += "\nBrakujące dane:\n"
        for column, missing in missing_data.items():
            if missing > 0:
                percentage = (missing / total_rows) * 100
                info += f"{column}: {missing} ({percentage:.2f}%)\n"

        # Podstawowe statystyki
        info += "\nPodstawowe statystyki:\n"
        stats = self.df.describe()
        info += str(stats)

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)

    def train_model(self):
        if self.df is None:
            messagebox.showwarning("Ostrzeżenie", "Najpierw wczytaj dane!")
            return

        try:
            target_column = self.target_column_var.get()
            if not target_column:
                raise ValueError("Wybierz kolumnę z etykietami!")

            # Przygotowanie danych
            X = self.df.drop(columns=[target_column])
            y = self.df[target_column]

            # Konwersja kolumn na typ numeryczny
            for column in X.columns:
                if X[column].dtype == 'object':
                    try:
                        X[column] = pd.to_numeric(X[column], errors='coerce')
                    except:
                        messagebox.showwarning("Ostrzeżenie", f"Kolumna {column} zawiera nietypowe dane!")

            # Obsługa brakujących danych
            X = X.fillna(X.mean())

            # Podział danych
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Skalowanie danych
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Tworzenie i trenowanie modelu
            self.model = MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=1000,
                random_state=42
            )

            self.model.fit(X_train_scaled, y_train)

            # Ocena modelu
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)

            # Wyświetlenie wyników
            result_info = f"\nWyniki uczenia:\n"
            result_info += f"Dokładność na zbiorze treningowym: {train_score:.4f}\n"
            result_info += f"Dokładność na zbiorze testowym: {test_score:.4f}\n"

            self.info_text.insert(tk.END, result_info)

            messagebox.showinfo("Sukces", "Model został wytrenowany pomyślnie!")

        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas trenowania modelu: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVAnalyzer(root)
    root.mainloop()