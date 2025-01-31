from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# ---------------------------------------
# Pobranie danych od użytkownika
# ---------------------------------------
username = input("Podaj nazwę użytkownika (login) do Wikipedii: ")
password = input("Podaj hasło do Wikipedii: ")
search_phrase = input("Podaj frazę, którą chcesz wyszukać: ")

# ---------------------------------------
# Inicjalizacja przeglądarki Chrome
# ---------------------------------------
driver = webdriver.Chrome()  # lub driver = webdriver.Chrome(executable_path="ścieżka/do/chromedriver")
driver.maximize_window()

try:
    # 1. Wejdź na stronę główną polskiej Wikipedii
    driver.get("https://pl.wikipedia.org/")

    # 2. Kliknij w link "Zaloguj się" (prawy górny róg)
    zaloguj_sie_link = driver.find_element(By.LINK_TEXT, "Zaloguj się")
    zaloguj_sie_link.click()

    # Dajemy krótką pauzę, aby upewnić się, że strona logowania się załadowała
    time.sleep(2)

    # 3. Wpisujemy login
    driver.find_element(By.ID, "wpName1").send_keys(username)
    # 4. Wpisujemy hasło
    driver.find_element(By.ID, "wpPassword1").send_keys(password)
    # 5. Klikamy przycisk "Zaloguj się"
    driver.find_element(By.ID, "wpLoginAttempt").click()

    # Czekamy kilka sekund na zalogowanie
    time.sleep(3)

    # 6. Wyszukanie frazy (pole wyszukiwania ma name="search")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(search_phrase)
    search_box.submit()

    # Dajemy kilka sekund na załadowanie wyników
    time.sleep(3)

    # ---------------------------------------
    # 7. Pobierz podstawowe informacje ze strony
    # ---------------------------------------
    # Na ogół Wikipedia w treści artykułu ma:
    # - Nagłówek w elemencie #firstHeading
    # - Główna treść w divie .mw-parser-output
    #   Pierwszy akapit: .mw-parser-output > p
    #
    # Jednak czasem (np. strony ujednoznaczniające) struktura może się różnić.
    # Warto dodać try/except, aby uniknąć błędów.

    try:
        # Pobranie tytułu artykułu
        heading = driver.find_element(By.ID, "firstHeading").text
    except:
        heading = "Brak tytułu (strona może nie być artykułem)."

    try:
        # Pobranie pierwszego akapitu
        # Szukamy pierwszego <p> bezpośrednio w .mw-parser-output
        first_paragraph = driver.find_element(
            By.CSS_SELECTOR,
            "div.mw-parser-output > p"
        ).text
    except:
        first_paragraph = "Brak treści (być może jest to strona ujednoznaczniająca lub inny typ strony)."

    # ---------------------------------------
    # 8. Zapisz dane do pliku tekstowego
    # ---------------------------------------
    filename = "wikipedia_info.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Tytuł artykułu: {heading}\n\n")
        f.write(f"Pierwszy akapit:\n{first_paragraph}\n")

    print(f"Zapisano informacje w pliku: {filename}")

finally:
    # 9. Zamknij przeglądarkę
    driver.quit()
