import tkinter as tk
from tkinter import PhotoImage

class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Chat z GPT")

        # Ustawienie logo
        self.logo_image = PhotoImage(file="converted_image.png")  # Zakładamy, że logo.png jest w tym samym katalogu co skrypt
        self.logo_label = tk.Label(master, image=self.logo_image)
        self.logo_label.grid(row=0, column=0, sticky="nw")

        # Pole tekstowe do wpisywania wiadomości
        self.message_entry = tk.Entry(master, width=100)
        self.message_entry.grid(row=1, column=0, columnspan=3)

        # Pole tekstowe dla odpowiedzi, z wysokością 4 linii
        self.response_text = tk.Text(master, height=4, width=100)
        self.response_text.grid(row=2, column=0, columnspan=3)
        self.logo_label.config(height=4*self.response_text.cget("height"))

        # Przyciski
        self.send_button = tk.Button(master, text="SEND", command=self.send_message)
        self.send_button.grid(row=3, column=1)

        self.exit_button = tk.Button(master, text="EXIT", command=master.quit)
        self.exit_button.grid(row=3, column=2)

        # Spacing
        self.space_label = tk.Label(master, text=" ")
        self.space_label.grid(row=3, column=0)

    def send_message(self):
        # Tu można dodać kod do wysyłania wiadomości do API OpenAI lub innego backendu
        message = self.message_entry.get()
        self.response_text.insert(tk.END, f"Odpowiedź: {message}\n")
        self.message_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()