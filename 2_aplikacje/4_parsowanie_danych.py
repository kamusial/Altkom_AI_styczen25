import sys
import pandas as pd
import matplotlib.pyplot as plt

def wczytaj_dane(nazwa_pliku):
    try:
        # Wczytanie danych z pliku CSV, pomijając błędne wiersze, zakładając kodowanie utf-8
        df = pd.read_csv(nazwa_pliku, encoding='utf-8', on_bad_lines='skip')
        print("Dane wczytane pomyślnie. Niektóre wiersze mogły zostać pominięte z powodu błędów.")
        return df
    except Exception as e:
        print(f"Błąd podczas wczytywania pliku: {e}")
        sys.exit(1)

def analizuj_dane(df):
    report = []

    # Sprawdzenie brakujących wartości
    brakujace_wartosci = df.isnull().sum()
    report.append(f"Brakujące wartości w poszczególnych kolumnach:\n{brakujace_wartosci}\n")

    # Sprawdzenie duplikatów
    duplikaty = df.duplicated().sum()
    report.append(f"Liczba zduplikowanych rekordów: {duplikaty}\n")

    # Analiza typów danych
    typy_danych = df.dtypes
    report.append(f"Typy danych w poszczególnych kolumnach:\n{typy_danych}\n")

    # Sugerowanie naprawy danych
    sugestie_naprawy = []
    if brakujace_wartosci.any():
        sugestie_naprawy.append("Rozważ uzupełnienie brakujących wartości lub usunięcie wierszy/kolumn z zbyt wieloma brakującymi wartościami.")
    if duplikaty > 0:
        sugestie_naprawy.append("Rozważ usunięcie zduplikowanych wpisów.")
    report.append("Sugestie naprawy danych:\n" + "\n".join(sugestie_naprawy) + "\n")

    # Generowanie wykresów
    for column in df.select_dtypes(include=['number']).columns:
        plt.figure()
        df[column].dropna().hist()
        plt.title(f'Rozkład wartości dla {column}')
        plt.xlabel(column)
        plt.ylabel('Liczba wystąpień')
        plt.savefig(f'{column}_distribution.png')
        plt.close()

    return "\n".join(report)

def main():
    if len(sys.argv) != 3:
        print("Użycie: python analyze_csv.py <plik_wejsciowy_csv> <plik_wyjsciowy_txt>")
        sys.exit(1)

    plik_wejsciowy = sys.argv[1]
    plik_wyjsciowy = sys.argv[2]

    # Wczytanie danych
    dane = wczytaj_dane(plik_wejsciowy)

    # Analiza danych
    raport_analizy = analizuj_dane(dane)

    # Zapis do pliku z kodowaniem utf-8
    with open(plik_wyjsciowy, 'w', encoding='utf-8') as plik:
        plik.write(raport_analizy)

    print(f"Analiza zakończona. Raport został zapisany w pliku {plik_wyjsciowy}")

if __name__ == "__main__":
    main()
