import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

# Käyttäjäagentti headerit, jotta serveri ei blokkaa
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/112.0.0.0 Safari/537.36"
}

def get_lausunto_links():
    """Hakee kaikki lausuntojen linkit headless-Seleniumilla."""
    options = Options()
    options.add_argument("--headless")  # Pakollinen GitHub Actionsissa
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.lausuntopalvelu.fi/FI/AllLausuntoRequests")
    time.sleep(2)  # Odotetaan sivun latautumista

    links = [a.get_attribute("href") for a in driver.find_elements("tag name", "a")]
    driver.quit()
    return links

def fetch_lausunto_text(url):
    """Hakee lausunnon sisällön."""
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def find_relevant_lausunnot():
    """Esimerkkifunktio: kerää lausunnot ja palauttaa listan dict-muodossa."""
    links = get_lausunto_links()
    lausunnot = []
    for link in links:
        try:
            text = fetch_lausunto_text(link)
            lausunnot.append({"url": link, "text": text})
        except Exception as e:
            print(f"Error fetching {link}: {e}")
    return lausunnot
