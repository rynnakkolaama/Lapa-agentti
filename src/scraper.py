import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.lausuntopalvelu.fi"

KEYWORDS = [
    "380/2023",
    "laki työvoimapalveluiden järjestämisestä"
]

def get_lausunto_links():
    url = BASE_URL + "/FI/AllLausuntoRequests"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/FI/Proposal/" in href:
            links.append(BASE_URL + href)

    return list(set(links))

def fetch_lausunto_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
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
                    "text": text[:5000]  # rajaa pitkä teksti analysointia varten
                })
                break

    return results

if __name__ == "__main__":
    lausunnot = find_relevant_lausunnot()
    for l in lausunnot:
        print(l)
