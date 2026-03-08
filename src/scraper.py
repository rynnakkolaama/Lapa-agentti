import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/145.0.7632.159 Safari/537.36"
}

BASE_URL = "https://www.lausuntopalvelu.fi"

def get_lausunto_links():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(f"{BASE_URL}/FI/Proposal/List")
    time.sleep(3)  # odota että sivu latautuu

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/FI/Proposal/Details" in href:
            links.append(BASE_URL + href)
    return links

def fetch_lausunto_text(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def find_relevant_lausunnot():
    links = get_lausunto_links()
    lausunnot = []
    for link in links:
        text = fetch_lausunto_text(link)
        if "AI" in text or "tekoäly" in text.lower():
            lausunnot.append({"url": link, "text": text})
    return lausunnot
