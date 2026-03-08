# src/scraper.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.lausuntopalvelu.fi"

# Avainsanat, joita etsitään
KEYWORDS = [
    "380/2023",
    "laki työvoimapalveluiden järjestämisestä"
]

# Käytetään User-Agentia, jotta palvelin ei blokkaa pyyntöjä
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.5993.90 Safari/537.36"
}

def get_lausunto_links():
    """
    Hakee kaikki lausuntopyyntöjen linkit AllLausuntoRequests-sivulta.
    """
    url = BASE_URL + "/FI/AllLausuntoRequests"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()  # nostaa poikkeuksen, jos ei 200 OK

    soup = BeautifulSoup(r.text, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/FI/Proposal/" in href:
            links.append(BASE_URL + href)

    return list(set(links))


def fetch_lausunto_text(url):
    """
    Hakee yksittäisen lausuntosivun tekstin analysoitavaksi.
    """
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return text


def find_relevant_lausunnot():
    """
    Hakee kaikki lausunnot, jotka sisältävät KEYWORDS-listan avainsanoja.
    Palauttaa listan dictejä: {"url": ..., "text": ...}
    """
    links = get_lausunto_links()
    results = []

    for link in links:
        try:
            text = fetch_lausunto_text(link)
        except requests.HTTPError as e:
            print(f"Virhe haettaessa {link}: {e}")
            continue

        for keyword in KEYWORDS:
            if keyword.lower() in text.lower():
                results.append({
                    "url": link,
                    "text": text[:5000]  # rajataan analysoitava osuus
                })
                break

    return results


if __name__ == "__main__":
    lausunnot = find_relevant_lausunnot()
    for l in lausunnot:
        print(f"{l['url']}\n{l['text'][:200]}...\n")
