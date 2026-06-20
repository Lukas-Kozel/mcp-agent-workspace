import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def verify_groq_connection():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("API klíč nebyl nalezen v prostředí!")

    client = Groq(api_key=api_key)
    
    print("Odesílám testovací ping na model Llama 3.3 70B...")
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Jsi systémový asistent. Odpověz jedním slovem."},
                {"role": "user", "content": "Je připojení k API funkční?"}
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=20
        )
        
        print("\n✅ Spojení úspěšné! Odpověď modelu:")
        print(f"> {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"\n❌ Chyba při spojení: {e}")

if __name__ == "__main__":
    verify_groq_connection()