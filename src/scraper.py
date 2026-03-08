import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.lausuntopalvelu.fi"

KEYWORDS = [
    "380/2023",
    "laki työvoimapalveluiden järjestämisestä"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "fi-FI,fi;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.lausuntopalvelu.fi/"
}


def get_lausunto_links():
    url = BASE_URL + "/FI/AllLausuntoRequests"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/FI/Proposal/" in href:
            links.append(BASE_URL + href)

    return list(set(links))


def fetch_lausunto_text(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def find_relevant_lausunnot():
    links = get_lausunto_links()
    results = []

    for link in links:
        text = fetch_lausunto_text(link)
        for keyword in KEYWORDS:
            if keyword.lower() in text.lower():
                results.append({
                    "url": link,
                    "text": text[:5000]
                })
                break

    return results


if __name__ == "__main__":
    lausunnot = find_relevant_lausunnot()
    for l in lausunnot:
        print(l["url"])
