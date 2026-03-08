import requests
import pdfplumber
import io

BASE_API = "https://www.lausuntopalvelu.fi/api/v1/Lausuntopalvelu.svc"
KEYWORDS = [
    "380/2023",
    "laki työvoimapalveluiden järjestämisestä"
]

def fetch_all_proposals():
    url = f"{BASE_API}/Proposals"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def fetch_proposal_pdf(pdf_url):
    r = requests.get(pdf_url)
    r.raise_for_status()
    with pdfplumber.open(io.BytesIO(r.content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def find_relevant_lausunnot():
    data = fetch_all_proposals()
    results = []

    for item in data:
        title = item.get("Title", "")
        description = item.get("Description", "")
        text = f"{title}\n{description}"

        # Tarkista avainsanat
        for keyword in KEYWORDS:
            if keyword.lower() in text.lower():
                # Jos PDF-liite löytyy, hae teksti
                pdf_url = item.get("PdfUrl")
                if pdf_url:
                    text += "\n" + fetch_proposal_pdf(pdf_url)

                results.append({
                    "url": item.get("Url", ""),
                    "text": text[:5000]
                })
                break

    return results

if __name__ == "__main__":
    lausunnot = find_relevant_lausunnot()
    for l in lausunnot:
        print(l["url"], "\n", l["text"][:200], "...\n")
