import tkinter as tk
from tkinter import scrolledtext, PhotoImage
import openai
from PIL import Image, ImageTk

# 🔹 Klucz API OpenAI
# API_KEY =
openai.api_key = API_KEY

# 🔹 Ścieżka do logo
LOGO_PATH = "converted_image.png"  # Upewnij się, że masz plik PNG


# 🔹 Funkcja do wysyłania zapytań do ChatGPT
def send_to_gpt():
    """Wysyła zapytanie do ChatGPT i wyświetla odpowiedź."""
    user_input = user_input_box.get("1.0", tk.END).strip()

    if user_input:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_input}],
                temperature=0.7
            )
            answer = response['choices'][0]['message']['content']

            chat_history.config(state=tk.NORMAL)
            chat_history.insert(tk.END, f"Ty: {user_input}\n")
            chat_history.insert(tk.END, f"GPT: {answer}\n\n")
            chat_history.config(state=tk.DISABLED)
            chat_history.yview(tk.END)

        except Exception as e:
            chat_history.config(state=tk.NORMAL)
            chat_history.insert(tk.END, f"Błąd: {str(e)}\n")
            chat_history.config(state=tk.DISABLED)

        user_input_box.delete("1.0", tk.END)


# 🔹 Funkcja do zamykania aplikacji
def exit_app():
    root.quit()


# 🔹 Funkcja do ładowania i skalowania logo do wysokości pola historii czatu
def load_resized_logo(path, target_height):
    """Ładuje obraz i skaluje go do określonej wysokości, zachowując proporcje."""
    try:
        image = Image.open(path)
        original_width, original_height = image.size
        new_width = int((target_height / original_height) * original_width)
        resized_image = image.resize((new_width, target_height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image), new_width
    except Exception as e:
        print(f"Błąd ładowania logo: {e}")
        return None, 0


# 🔹 Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Chat GPT")
root.geometry("800x300")  # Rozmiar okna

# 🔹 Wysokość historii rozmów (4 linie x 20 pikseli)
CHAT_HISTORY_HEIGHT = 4 * 20

# 🔹 Wczytaj i zmień rozmiar logo
logo_image, logo_width = load_resized_logo(LOGO_PATH, target_height=CHAT_HISTORY_HEIGHT)

# 📌 **Układ główny: 2 kolumny (Logo | Historia rozmów)**
main_frame = tk.Frame(root)
main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# 📌 **Logo po lewej stronie**
if logo_image:
    logo_label = tk.Label(main_frame, image=logo_image)
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")
else:
    logo_label = tk.Label(main_frame, text="[LOGO]", font=("Arial", 14, "bold"))
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# 📜 **Pole historii rozmowy (wysokość 4 linie)**
chat_history = scrolledtext.ScrolledText(main_frame, state='disabled', width=70, height=4, background="#10FA34",
                                         fg="black")
chat_history.grid(row=0, column=1, padx=10, pady=10)

# 📝 **Pole tekstowe dla użytkownika**
user_input_box = scrolledtext.ScrolledText(root, height=4, width=52)
user_input_box.pack(padx=10, pady=10, fill=tk.X)

# 🎛 **Trzy równe przyciski z odstępem 20px**
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn1 = tk.Button(button_frame, text="Option 1", width=15, command=lambda: None)  # Możesz dodać funkcję
btn1.pack(side=tk.LEFT, padx=10)

send_button = tk.Button(button_frame, text="SEND", width=30, command=send_to_gpt)  # Środkowy przycisk 2x dłuższy
send_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame, text="EXIT", width=15, command=exit_app)  # Zamknięcie aplikacji
exit_button.pack(side=tk.LEFT, padx=10)

# 🔹 Uruchomienie aplikacji
root.mainloop()

