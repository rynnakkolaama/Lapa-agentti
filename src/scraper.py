import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = "https://www.lausuntopalvelu.fi"

KEYWORDS = [
    "380/2023",
    "laki työvoimapalveluiden järjestämisestä"
]

def get_lausunto_links():
    # Headless Chrome setup
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=options)

    driver.get(BASE_URL + "/FI/AllLausuntoRequests")
    time.sleep(3)  # odota että sivu latautuu

    links = set()
    for a in driver.find_elements(By.TAG_NAME, "a"):
        href = a.get_attribute("href")
        if href and "/FI/Proposal/" in href:
            links.add(href)

    driver.quit()
    return list(links)


def fetch_lausunto_text(url):
    # Headless Chrome setup
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)  # odota että sivu latautuu

    text = driver.find_element(By.TAG_NAME, "body").text

    driver.quit()
    return text


def find_relevant_lausunnot():
    links = get_lausunto_links()
    results = []

    for link in links:
        text = fetch_lausunto_text(link)
        for keyword in KEYWORDS:
            if keyword.lower() in text.lower():
                results.append({
                    "url": link,
                    "text": text[:5000]  # rajaa analyysi 5000 merkkiin
                })
                break

    return results


if __name__ == "__main__":
    lausunnot = find_relevant_lausunnot()
    for l in lausunnot:
        print(l["url"])
