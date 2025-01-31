from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 🔹 Ustawienie ścieżki do WebDrivera
PATH_TO_CHROMEDRIVER = "C:/chromedriver.exe"  # <- ZMIEŃ NA SWOJĄ ŚCIEŻKĘ

# 🔹 Inicjalizacja przeglądarki
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Otwórz w pełnym ekranie
driver = webdriver.Chrome(options=options)

# 🔹 Pobranie nazwy produktu od użytkownika
product_name = input("Podaj nazwę produktu: ")

try:
    # 1️⃣ Otwórz Allegro
    driver.get("https://allegro.pl")
    time.sleep(10)
    # 2️⃣ Akceptacja ciasteczek (jeśli się pojawi)
    try:
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Ok, zgadzam się')]")
        accept_button.click()
    except:
        pass  # Jeśli przycisk nie pojawi się, pomijamy ten krok

    # 3️⃣ Wyszukaj produkt
    search_box = driver.find_element(By.XPATH, "//input[@type='search']")
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)  # Naciśnij Enter
    time.sleep(3)  # Czekaj na załadowanie wyników

    # 4️⃣ Pobierz listę produktów
    products = driver.find_elements(By.XPATH, "//article[@data-analytics-enabled='true']")

    if not products:
        print("Nie znaleziono produktów.")
        driver.quit()
        exit()

    # 5️⃣ Znalezienie najtańszego produktu
    cheapest_product = None
    cheapest_price = float('inf')

    for product in products:
        try:
            price_text = product.find_element(By.XPATH, ".//span[@class='_9c44d_1zemI']").text
            price = float(price_text.replace(" zł", "").replace(",", ".").strip())

            if price < cheapest_price:
                cheapest_price = price
                cheapest_product = product
        except:
            continue  # Jeśli nie uda się pobrać ceny, pomijamy produkt

    if cheapest_product:
        # 6️⃣ Pobranie linku do najtańszego produktu
        product_link = cheapest_product.find_element(By.XPATH, ".//a").get_attribute("href")
        print(f"Najtańszy produkt: {cheapest_price} PLN")
        print(f"Link do produktu: {product_link}")

        # 7️⃣ Przejście na stronę produktu
        driver.get(product_link)
        time.sleep(3)

        # 8️⃣ Automatyczne dodanie do koszyka
        try:
            add_to_cart_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Dodaj do koszyka')]")
            add_to_cart_button.click()
            print("✅ Produkt został dodany do koszyka!")
        except:
            print("❌ Nie udało się automatycznie dodać do koszyka.")

    else:
        print("❌ Nie znaleziono żadnego produktu.")

except Exception as e:
    print(f"❌ Błąd: {e}")

finally:
    time.sleep(5)
    driver.quit()  # Zamknij przeglądarkę

