# src/main.py
import json
import os

from scraper import find_relevant_lausunnot
from analyzer import analyze_lausunto
from github_issue_creator import create_issue

PROCESSED_FILE = "data/processed.json"


def load_processed():
    """
    Lataa listan jo käsitellyistä lausunnoista.
    """
    if not os.path.exists(PROCESSED_FILE):
        return []

    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_processed(data):
    """
    Tallentaa käsitellyt lausunnot tiedostoon.
    """
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def run():
    processed = load_processed()
    lausunnot = find_relevant_lausunnot()

    if not lausunnot:
        print("Ei uusia lausuntoja löydetty.")
        return

    for item in lausunnot:
        url = item["url"]

        if url in processed:
            # Jo käsitelty → ohitetaan
            continue

        text = item["text"]

        print(f"Analysoidaan lausunto: {url}")
        analysis = analyze_lausunto(text)

        body = f"""
## Lausuntopyyntö havaittu

URL:
{url}

---

## AI-analyysi

{analysis}
"""

        create_issue(
            title="Lausunto liittyen lakiin 380/2023",
            body=body
        )

        processed.append(url)

    save_processed(processed)
    print(f"{len(lausunnot)} lausuntoa käsitelty ja tallennettu.")


if __name__ == "__main__":
    run()
