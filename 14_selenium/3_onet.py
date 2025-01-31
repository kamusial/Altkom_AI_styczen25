from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    # 1. Uruchomienie przeglądarki Chrome z Selenium
    driver = webdriver.Chrome()  # lub webdriver.Chrome(executable_path="ścieżka/do/chromedriver")
    driver.maximize_window()

    try:
        # 2. Wejdź na stronę onet.pl
        driver.get("https://www.onet.pl/")

        # 3. Akceptuj cookies (jeżeli pojawi się popup)
        #    W zależności od zmian w Onecie może być inny selektor:
        try:
            wait = WebDriverWait(driver, 5)
            accept_cookies_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[starts-with(@id,'onetrust-accept-btn-handler')]"))
            )
            accept_cookies_button.click()
        except:
            print("Nie znaleziono / nie wyświetlił się popup z cookies, przechodzę dalej...")

        time.sleep(2)  # Drobne opóźnienie, aby strona zdążyła się przeładować po kliknięciu

        # 4. Znalezienie sekcji z najważniejszym artykułem
        #    - Onet często ma główne newsy w sekcji topNews.
        #    - Poniżej podany jest przykładowy selektor – może wymagać aktualizacji.
        try:
            # Przykładowo: div o klasie "topNews", a w nim link do artykułu
            top_news_element = driver.find_element(By.CSS_SELECTOR, "div.topNews a")
        except:
            print("Nie udało się znaleźć głównego artykułu w sekcji topNews.")
            return

        # 5. Pobieramy link do artykułu
        article_url = top_news_element.get_attribute("href")

        # 6. Otwieramy ten artykuł w nowej karcie (lub w tej samej)
        driver.execute_script("window.open(arguments[0]);", article_url)
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(3)  # krótka pauza na załadowanie artykułu

        # 7. Pobieramy tytuł artykułu
        #    W zależności od strony artykułu Onet używa różnych struktur HTML,
        #    więc trzeba czasem sprawdzić, co tam jest. Spróbujmy np. <h1>:
        try:
            title_element = driver.find_element(By.CSS_SELECTOR, "h1")
            article_title = title_element.text.strip()
        except:
            article_title = "Brak tytułu (struktura strony jest inna)."

        # 8. Pobieramy lead / krótki opis. To również zależy od layoutu artykułu.
        #    Załóżmy, że jest w tagu <p> (pierwszym paragrafie), lub w tagu .lead
        try:
            # Najpierw spróbujmy znaleźć element z klasą "lead"
            lead_element = driver.find_element(By.CSS_SELECTOR, ".lead")
            article_lead = lead_element.text.strip()
        except:
            # Jeśli nie udało się, spróbujmy wziąć pierwszy paragraf
            try:
                p_element = driver.find_element(By.CSS_SELECTOR, "article p")
                article_lead = p_element.text.strip()
            except:
                article_lead = "Brak krótkiego opisu (nie znaleziono pasującego selektora)."

        # 9. Zapisujemy dane do pliku tekstowego
        filename = "najwazniejszy_artykul.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Tytuł artykułu: {article_title}\n\n")
            f.write(f"Podsumowanie / Lead:\n{article_lead}\n\n")
            f.write("Dlaczego ten artykuł jest najważniejszy?\n")
            f.write("Ponieważ został zidentyfikowany jako główny news (topNews) na stronie Onet.\n")

        print(f"Zapisano podsumowanie w pliku: {filename}")

    finally:
        # 10. Zamykamy przeglądarkę
        driver.quit()


if __name__ == "__main__":
    main()
