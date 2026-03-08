import os
from anthropic import Anthropic

def analyze_lausunto(text):
    """
    Analysoi yksittäisen lausuntopyynnön tekstin AI:lla.
    """

    client = Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    prompt = f"""
Analysoi seuraava lausuntopyyntö.

Tunnista erityisesti viittaukset:

- laki työvoimapalveluiden järjestämisestä
- laki 380/2023

Teksti:

{text}

Kirjoita:

1. lyhyt yhteenveto
2. keskeinen sisältö
3. vaikutukset kunnille
4. vaikutukset työvoimapalveluihin
"""

    msg = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=600,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return msg.content[0].text


if __name__ == "__main__":
    sample_text = "Laki 380/2023 koskee digitaalisten palveluiden saavutettavuutta ja velvoittaa viranomaisia parantamaan verkkopalveluiden käytettävyyttä."
    result = analyze_lausunto(sample_text)
    print(result)
