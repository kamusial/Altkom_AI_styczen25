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
# (upewnij się, że chromedriver jest w PATH
# lub wskaż pełną ścieżkę w parametrze executable_path)
# ---------------------------------------
driver = webdriver.Chrome()
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

    print(f"Zakończono wyszukiwanie frazy: '{search_phrase}'.")

finally:
    # 7. Zamykamy przeglądarkę
    driver.quit()
