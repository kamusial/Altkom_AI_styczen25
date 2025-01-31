import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AdamW
import numpy as np

# Przykładowe dane treningowe (pary pytanie-odpowiedź)
training_data = [
    {
        "question": "Jaka jest stolica Polski?",
        "answer": "Stolica Polski to Warszawa."
    },
    {
        "question": "Kto napisał 'Pan Tadeusz'?",
        "answer": "'Pan Tadeusz' został napisany przez Adama Mickiewicza."
    },
    {
        "question": "Ile wynosi pierwiastek z 16?",
        "answer": "Pierwiastek z 16 wynosi 4."
    },
    {
        "question": "Jaki jest największy ssak na świecie?",
        "answer": "Największym ssakiem na świecie jest płetwal błękitny."
    }
]


def prepare_data(data, tokenizer, max_length=512):
    """Przygotowuje dane do treningu"""
    prepared_data = []

    for item in data:
        # Formatowanie tekstu: pytanie + odpowiedź
        text = f"Pytanie: {item['question']}\nOdpowiedź: {item['answer']}\n"

        # Tokenizacja tekstu
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


def train_model(training_data, num_epochs=3, batch_size=2, learning_rate=5e-5):
    """Trenuje model na podanych danych"""
    # Inicjalizacja tokenizera i modelu
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    # Dodanie tokenu paddingu
    tokenizer.pad_token = tokenizer.eos_token

    # Przygotowanie danych
    prepared_data = prepare_data(training_data, tokenizer)

    # Inicjalizacja optymalizatora
    optimizer = AdamW(model.parameters(), lr=learning_rate)

    # Przejście w tryb treningu
    model.train()

    # Główna pętla treningowa
    for epoch in range(num_epochs):
        print(f"\nEpoka {epoch + 1}/{num_epochs}")
        total_loss = 0

        # Przetwarzanie danych w mini-batche
        for i in range(0, len(prepared_data), batch_size):
            batch_data = prepared_data[i:i + batch_size]

            # Przygotowanie batcha
            input_ids = torch.stack([item['input_ids'] for item in batch_data])
            attention_mask = torch.stack([item['attention_mask'] for item in batch_data])

            # Obliczenie straty
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=input_ids
            )
            loss = outputs.loss

            # Propagacja wsteczna
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            total_loss += loss.item()
            print(f"Batch {i // batch_size + 1}, Loss: {loss.item():.4f}")

        avg_loss = total_loss / (len(prepared_data) // batch_size)
        print(f"Średnia strata w epoce {epoch + 1}: {avg_loss:.4f}")

    return model, tokenizer


def generate_response(model, tokenizer, question, max_length=100):
    """Generuje odpowiedź na pytanie"""
    # Przygotowanie promptu
    prompt = f"Pytanie: {question}\nOdpowiedź:"

    # Tokenizacja
    inputs = tokenizer(prompt, return_tensors='pt')

    # Generowanie odpowiedzi
    outputs = model.generate(
        inputs['input_ids'],
        max_length=max_length,
        num_return_sequences=1,
        temperature=0.7,
        pad_token_id=tokenizer.pad_token_id
    )

    # Dekodowanie odpowiedzi
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


def save_trained_model(model, tokenizer, path):
    """Zapisuje model i tokenizer"""
    model.save_pretrained(path)
    tokenizer.save_pretrained(path)


def load_trained_model(path):
    """Wczytuje zapisany model i tokenizer"""
    model = GPT2LMHeadModel.from_pretrained(path)
    tokenizer = GPT2Tokenizer.from_pretrained(path)
    return model, tokenizer


# Przykład użycia
if __name__ == "__main__":
    # Trenowanie modelu
    print("Rozpoczynam trenowanie modelu...")
    model, tokenizer = train_model(training_data)

    # Zapisanie modelu
    save_trained_model(model, tokenizer, 'finetuned_model')
    print("\nModel został zapisany")

    # Test generowania odpowiedzi
    print("\nTestowanie modelu:")
    test_questions = [
        "Jaka jest stolica Polski?",
        "Kto napisał 'Pan Tadeusz'?",
        "Ile wynosi pierwiastek z 16?"
    ]

    for question in test_questions:
        response = generate_response(model, tokenizer, question)
        print(f"\nPytanie: {question}")
        print(f"Odpowiedź: {response}")