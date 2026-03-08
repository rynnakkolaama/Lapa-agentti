# src/scraper.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.lausuntopalvelu.fi"
KEYWORDS = [
    "380/2023",
    "laki työvoimapalveluiden järjestämisestä"
]

def get_lausunto_links():
    """
    Hakee kaikki lausuntolinkit julkiselta listaukselta.
    """
    url = BASE_URL + "/FI/AllLausuntoRequests"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Lapa-Agent/1.0)"
    }

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/FI/Proposal/" in href:
            links.append(BASE_URL + href)

    return list(set(links))


def fetch_lausunto_text(url):
    """
    Hakee yksittäisen lausunnon tekstin.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Lapa-Agent/1.0)"
    }

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    return text


def find_relevant_lausunnot():
    """
    Suodattaa lausunnot, joissa esiintyy KEYWORDS-listan avainsanat.
    """
    links = get_lausunto_links()
    results = []

    for link in links:
        text = fetch_lausunto_text(link)

        for keyword in KEYWORDS:
            if keyword.lower() in text.lower():
                results.append({
                    "url": link,
                    "text": text[:5000]  # rajoitetaan pituus analyysiä varten
                })
                break

    return results


if __name__ == "__main__":
    # nopea testaus
    lausunnot = find_relevant_lausunnot()
    for l in lausunnot:
        print(l["url"])
        print(l["text"][:200], "...\n")
