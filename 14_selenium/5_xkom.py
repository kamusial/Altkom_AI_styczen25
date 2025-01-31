from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 🔹 Ustawienie ścieżki do WebDrivera
PATH_TO_CHROMEDRIVER = "C:/chromedriver.exe"  # ← ZMIEŃ NA SWOJĄ ŚCIEŻKĘ!

# 🔹 Inicjalizacja przeglądarki
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Otwórz na pełnym ekranie
driver = webdriver.Chrome(options=options)

# 🔹 Pobranie nazwy produktu od użytkownika
product_name = input("Podaj nazwę produktu: ")

try:
    # 1️⃣ Otwórz x-kom.pl
    driver.get("https://www.x-kom.pl/")

    # 2️⃣ Akceptacja ciasteczek (jeśli się pojawi)
    try:
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Wszystkie zgody')]")
        accept_button.click()
    except:
        pass  # Jeśli przycisk nie pojawi się, pomijamy ten krok
    time.sleep(5)
    # 3️⃣ Wyszukaj produkt
    search_box = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/header/div[2]/div/div[2]/div/div/div/div/div[1]/input")
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)  # Naciśnij Enter
    time.sleep(3)  # Czekaj na załadowanie wyników

    # 4️⃣ Pobierz listę produktów
    products = driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-1yu46qn-7')]")

    if not products:
        print("❌ Nie znaleziono produktów.")
        driver.quit()
        exit()

    # 5️⃣ Znalezienie najtańszego produktu
    cheapest_product = None
    cheapest_price = float('inf')

    for product in products:
        try:
            # Pobierz nazwę produktu
            product_name = product.find_element(By.XPATH, ".//h3").text

            # Pobierz cenę produktu
            price_text = product.find_element(By.XPATH, ".//span[contains(@class, 'sc-6n68ef-0')]").text
            price = float(price_text.replace(" zł", "").replace(",", ".").strip())

            if price < cheapest_price:
                cheapest_price = price
                cheapest_product = product
        except:
            continue  # Jeśli nie uda się pobrać ceny, pomijamy produkt

    if cheapest_product:
        # 6️⃣ Pobranie linku do najtańszego produktu
        product_link = cheapest_product.find_element(By.XPATH, ".//a").get_attribute("href")
        print(f"✅ Najtańszy produkt: {cheapest_price} PLN")
        print(f"🔗 Link do produktu: {product_link}")

        # 7️⃣ Przejście na stronę produktu
        driver.get(product_link)
        time.sleep(3)

        # 8️⃣ Automatyczne dodanie do koszyka (jeśli przycisk istnieje)
        try:
            add_to_cart_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Dodaj do koszyka')]")
            add_to_cart_button.click()
            print("🛒 Produkt został dodany do koszyka!")
        except:
            print("❌ Nie udało się automatycznie dodać do koszyka.")

    else:
        print("❌ Nie znaleziono żadnego produktu.")

except Exception as e:
    print(f"❌ Błąd: {e}")

finally:
    time.sleep(5)
    driver.quit()  # Zamknij przeglądarkę
