import json
import os

from scraper import find_relevant_lausunnot
from analyzer import analyze_lausunto
from github_issue_creator import create_issue

PROCESSED_FILE = "data/processed.json"

def load_processed():
    """Lataa jo käsitellyt lausunnot."""
    if not os.path.exists(PROCESSED_FILE):
        return []
    with open(PROCESSED_FILE) as f:
        return json.load(f)

def save_processed(data):
    """Tallentaa käsitellyt lausunnot tiedostoon."""
    with open(PROCESSED_FILE, "w") as f:
        json.dump(data, f, indent=2)

def run():
    processed = load_processed()
    lausunnot = find_relevant_lausunnot()

    for item in lausunnot:
        url = item["url"]

        if url in processed:
            continue  # Älä tee duplikaattia

        text = item["text"]
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

if __name__ == "__main__":
    run()
