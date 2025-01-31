import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam


def wczytaj_dane_i_spradz_bledy(filepath):
    """
    Funkcja wczytuje dane z pliku CSV, sprawdza braki w danych
    i zwraca przetworzone dane (X, y) oraz informację o tym,
    czy napotkano puste wartości.
    Tutaj używamy: sep=';', on_bad_lines='skip'.
    """
    try:
        # Wczytanie danych z pliku CSV do obiektu DataFrame
        # z pomijaniem błędnych wierszy:
        df = pd.read_csv(filepath, sep=';', on_bad_lines='skip', comment='#')

        # Sprawdź, czy są jakiekolwiek braki w danych
        brakujace = df.isnull().sum()
        print("Informacja o brakach (liczba braków w każdej kolumnie):")
        print(brakujace)

        # Usuwamy wiersze, które zawierają puste wartości
        # (można użyć np. imputacji zamiast usuwania)
        df.dropna(inplace=True)

        # Zakładamy, że ostatnia kolumna to etykieta:
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values

        return X, y, brakujace
    except Exception as e:
        print(f"Wystąpił błąd podczas wczytywania danych: {e}")
        return None, None, None


def zbuduj_i_trenuj_model(X, y):
    """
    Funkcja buduje prostą sieć neuronową do klasyfikacji binarnej
    i zwraca wytrenowany model.
    """
    input_dim = X.shape[1]

    model = Sequential()
    model.add(Dense(16, input_dim=input_dim, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Trenowanie modelu
    model.fit(X, y, epochs=10, batch_size=4, verbose=1)

    return model


def uruchom_klasyfikacje(filepath_entry):
    """
    Funkcja pobiera ścieżkę z pola tekstowego,
    wczytuje dane, sprawdza braki i uruchamia trenowanie.
    """
    filepath = filepath_entry.get()
    if not filepath:
        messagebox.showerror("Błąd", "Nie podano ścieżki do pliku CSV!")
        return

    # Wczytanie danych i analiza braków
    X, y, brakujace = wczytaj_dane_i_spradz_bledy(filepath)

    if X is None or y is None:
        messagebox.showerror("Błąd", "Wystąpił problem przy przetwarzaniu danych.")
        return

    # Sprawdź, czy w ogóle mamy dane po usunięciu braków
    if len(X) == 0:
        messagebox.showwarning("Uwaga", "Po usunięciu braków nie pozostały żadne dane!")
        return

    # Zbuduj i wytrenuj model
    model = zbuduj_i_trenuj_model(X, y)
    messagebox.showinfo("Sukces", "Model został wytrenowany!")

    # Przykładowa ewaluacja na tych samych danych (tylko pokazuje ideę)
    loss, acc = model.evaluate(X, y, verbose=0)
    print(f"Wyniki na danych treningowych: loss = {loss:.4f}, accuracy = {acc:.4f}")


def wybierz_plik(filepath_entry):
    """
    Funkcja otwiera okno wyboru pliku i ustawia ścieżkę w polu tekstowym.
    """
    filepath = filedialog.askopenfilename(
        title="Wybierz plik CSV",
        filetypes=[("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
    )
    filepath_entry.delete(0, tk.END)
    filepath_entry.insert(0, filepath)


def main():
    root = tk.Tk()
    root.title("Prosta klasyfikacja binarna z użyciem sieci neuronowej")

    tk.Label(root, text="Ścieżka do pliku CSV:").grid(row=0, column=0, padx=5, pady=5)
    filepath_entry = tk.Entry(root, width=50)
    filepath_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(root, text="Wybierz...",
              command=lambda: wybierz_plik(filepath_entry)).grid(row=0, column=2, padx=5, pady=5)

    tk.Button(root, text="Uruchom klasyfikację",
              command=lambda: uruchom_klasyfikacje(filepath_entry)).grid(row=1, column=0, columnspan=3, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
