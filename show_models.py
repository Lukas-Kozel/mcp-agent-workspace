# ukaz_modely.py
import os
from dotenv import load_dotenv
from google import genai

# Načte váš GEMINI_API_KEY ze souboru .env
load_dotenv()

# Inicializace Google klienta
client = genai.Client()

print("Dostupné modely pro generování textu a práci s Agenty:\n")
for m in client.models.list():
    # Vyfiltrujeme jen ty modely, které umí klasicky odpovídat (generateContent)
    if "generateContent" in m.supported_actions:
        print(f"- {m.name} (Popis: {m.display_name})")