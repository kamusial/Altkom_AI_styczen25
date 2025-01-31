import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AdamW
import json
import os

# Zmienne globalne
training_data = []
model = None
tokenizer = None


def create_gui():
    root = tk.Tk()
    root.title("Fine-tuning AI - trenowanie modelu")
    root.geometry("800x600")

    # Funkcje pomocnicze dla GUI
    def add_qa_pair():
        global training_data
        question = question_entry.get()
        answer = answer_text.get("1.0", tk.END).strip()

        if not question or not answer:
            messagebox.showwarning("Ostrzeżenie", "Wypełnij oba pola!")
            return

        training_data.append({
            "question": question,
            "answer": answer
        })

        # Aktualizacja listy pytań
        update_qa_list()

        # Wyczyszczenie pól
        question_entry.delete(0, tk.END)
        answer_text.delete("1.0", tk.END)

    def update_qa_list():
        qa_list.delete(0, tk.END)
        for i, item in enumerate(training_data):
            qa_list.insert(tk.END, f"Q{i + 1}: {item['question'][:50]}...")

    def show_selected_qa(event):
        selection = qa_list.curselection()
        if selection:
            idx = selection[0]
            question_entry.delete(0, tk.END)
            answer_text.delete("1.0", tk.END)
            question_entry.insert(0, training_data[idx]["question"])
            answer_text.insert("1.0", training_data[idx]["answer"])

    def save_training_data():
        if not training_data:
            messagebox.showwarning("Ostrzeżenie", "Brak danych do zapisania!")
            return

        with open("training_data.json", "w", encoding="utf-8") as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Sukces", "Dane zostały zapisane!")

    def load_training_data():
        global training_data
        try:
            with open("training_data.json", "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                training_data.clear()
                training_data.extend(loaded_data)
                update_qa_list()
                messagebox.showinfo("Sukces", "Dane zostały wczytane!")
        except FileNotFoundError:
            messagebox.showwarning("Ostrzeżenie", "Nie znaleziono pliku z danymi!")

    def start_training():
        global model, tokenizer

        if not training_data:
            messagebox.showwarning("Ostrzeżenie", "Dodaj najpierw dane treningowe!")
            return

        progress_var.set(0)
        status_label.config(text="Inicjalizacja modelu...")
        root.update()

        try:
            # Inicjalizacja modelu i tokenizera
            tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
            model = GPT2LMHeadModel.from_pretrained('gpt2')
            tokenizer.pad_token = tokenizer.eos_token

            # Parametry treningu
            num_epochs = int(epochs_var.get())
            learning_rate = float(lr_var.get())

            # Przygotowanie danych
            prepared_data = prepare_data(training_data, tokenizer)

            # Trening
            optimizer = AdamW(model.parameters(), lr=learning_rate)
            model.train()

            total_steps = num_epochs * len(prepared_data)
            current_step = 0

            for epoch in range(num_epochs):
                status_label.config(text=f"Epoka {epoch + 1}/{num_epochs}")

                for i, batch in enumerate(prepared_data):
                    input_ids = batch['input_ids'].unsqueeze(0)
                    attention_mask = batch['attention_mask'].unsqueeze(0)

                    outputs = model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        labels=input_ids
                    )

                    loss = outputs.loss
                    loss.backward()
                    optimizer.step()
                    optimizer.zero_grad()

                    # Aktualizacja paska postępu
                    current_step += 1
                    progress = (current_step / total_steps) * 100
                    progress_var.set(progress)
                    root.update()

            # Zapisanie modelu
            save_trained_model(model, tokenizer)
            status_label.config(text="Trening zakończony!")
            messagebox.showinfo("Sukces", "Model został wytrenowany i zapisany!")

        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas treningu: {str(e)}")

    def test_model():
        global model, tokenizer
        if model is None or tokenizer is None:
            try:
                model, tokenizer = load_trained_model()
            except:
                messagebox.showerror("Błąd", "Najpierw wytrenuj model!")
                return

        question = question_entry.get()
        if not question:
            messagebox.showwarning("Ostrzeżenie", "Wpisz pytanie!")
            return

        try:
            response = generate_response(model, tokenizer, question)
            answer_text.delete("1.0", tk.END)
            answer_text.insert("1.0", response)
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd generowania odpowiedzi: {str(e)}")

    # Tworzenie interfejsu
    # Frame dla wprowadzania danych
    input_frame = ttk.LabelFrame(root, text="Wprowadzanie danych", padding=10)
    input_frame.pack(fill=tk.X, padx=5, pady=5)

    ttk.Label(input_frame, text="Pytanie:").pack(fill=tk.X)
    question_entry = ttk.Entry(input_frame)
    question_entry.pack(fill=tk.X, pady=2)

    ttk.Label(input_frame, text="Odpowiedź:").pack(fill=tk.X)
    answer_text = scrolledtext.ScrolledText(input_frame, height=4)
    answer_text.pack(fill=tk.X, pady=2)

    button_frame = ttk.Frame(input_frame)
    button_frame.pack(fill=tk.X, pady=5)
    ttk.Button(button_frame, text="Dodaj", command=add_qa_pair).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Testuj", command=test_model).pack(side=tk.LEFT, padx=5)

    # Frame dla listy pytań i odpowiedzi
    list_frame = ttk.LabelFrame(root, text="Lista pytań i odpowiedzi", padding=10)
    list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    qa_list = tk.Listbox(list_frame)
    qa_list.pack(fill=tk.BOTH, expand=True)
    qa_list.bind('<<ListboxSelect>>', show_selected_qa)

    # Frame dla opcji treningu
    training_frame = ttk.LabelFrame(root, text="Opcje treningu", padding=10)
    training_frame.pack(fill=tk.X, padx=5, pady=5)

    ttk.Label(training_frame, text="Liczba epok:").pack(side=tk.LEFT, padx=5)
    epochs_var = tk.StringVar(value="3")
    ttk.Entry(training_frame, textvariable=epochs_var, width=5).pack(side=tk.LEFT, padx=5)

    ttk.Label(training_frame, text="Learning rate:").pack(side=tk.LEFT, padx=5)
    lr_var = tk.StringVar(value="5e-5")
    ttk.Entry(training_frame, textvariable=lr_var, width=8).pack(side=tk.LEFT, padx=5)

    # Frame dla kontrolek
    control_frame = ttk.Frame(root)
    control_frame.pack(fill=tk.X, padx=5, pady=5)

    ttk.Button(control_frame, text="Zapisz dane", command=save_training_data).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame, text="Wczytaj dane", command=load_training_data).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame, text="Trenuj model", command=start_training).pack(side=tk.LEFT, padx=5)

    # Pasek postępu i status
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(fill=tk.X, padx=5, pady=5)

    status_label = ttk.Label(root, text="Gotowy")
    status_label.pack(pady=5)

    return root


# Funkcje pomocnicze z poprzedniego kodu
def prepare_data(data, tokenizer, max_length=512):
    prepared_data = []
    for item in data:
        text = f"Pytanie: {item['question']}\nOdpowiedź: {item['answer']}\n"
        encodings = tokenizer(
            text,
            truncation=True,
            max_length=max_length,
            padding='max_length',
            return_tensors='pt'
        )
        prepared_data.append({
            'input_ids': encodings['input_ids'].squeeze(),
            'attention_mask': encodings['attention_mask'].squeeze()
        })
    return prepared_data


def generate_response(model, tokenizer, question, max_length=100):
    prompt = f"Pytanie: {question}\nOdpowiedź:"
    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = model.generate(
        inputs['input_ids'],
        max_length=max_length,
        num_return_sequences=1,
        temperature=0.7,
        pad_token_id=tokenizer.pad_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


def save_trained_model(model, tokenizer, path='trained_model'):
    model.save_pretrained(path)
    tokenizer.save_pretrained(path)


def load_trained_model(path='trained_model'):
    model = GPT2LMHeadModel.from_pretrained(path)
    tokenizer = GPT2Tokenizer.from_pretrained(path)
    return model, tokenizer


if __name__ == "__main__":
    root = create_gui()
    root.mainloop()