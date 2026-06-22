from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("local_storage_server")

@mcp.tool()
def search_files(start_path: str, search_term: str) -> list:
    """
    Vyhledá konkrétní soubor nebo složku podle jména (nebo části jména).
    Tento nástroj použij VŽDY, když uživatel hledá konkrétní soubor nebo se ptá, jestli nějaký soubor existuje.
    DŮLEŽITÉ: Jako parametry tohoto nástroje vždy vracej POUZE platný JSON (např. {"start_path": "/home/luky/Downloads", "search_term": "test"}).
    """
    matches = []
    MAX_RESULTS = 50
    
    try:
        # Procházení složek do hloubky
        for root, dirs, files in os.walk(start_path):
            # Prohledáváme soubory
            for file in files:
                if search_term.lower() in file.lower():
                    matches.append(os.path.join(root, file))
                    if len(matches) >= MAX_RESULTS:
                        matches.append(f"... [Nalezeno více výsledků, zobrazeno pouze prvních {MAX_RESULTS} pro úsporu paměti.]")
                        return matches
                        
            # Prohledáváme i názvy složek
            for d in dirs:
                if search_term.lower() in d.lower():
                    matches.append(os.path.join(root, d))
                    if len(matches) >= MAX_RESULTS:
                        return matches
                        
    except PermissionError:
        matches.append("[Varování: K některým podsložkám byl odepřen přístup.]")
    except Exception as e:
        return [f"Chyba při vyhledávání: {str(e)}"]

    if not matches:
        return ["Hledaný výraz nebyl v zadané cestě nalezen."]
        
    return matches

# Tady necháme i váš původní nástroj (pro případ, že uživatel chce opravdu vypsat konkrétní malou složku)
@mcp.tool()
def list_all_files(folder_for_analysis: str) -> list:
    """
    Vrátí seznam souborů v jedné konkrétní složce.
    DŮLEŽITÉ: Jako parametry vracej POUZE platný JSON (např. {"folder_for_analysis": "."}).
    """
    try:
        files = os.listdir(folder_for_analysis)
        # OCHRANA PROTI LIMITŮM: Zabrání zkolabování agenta při velké složce
        if len(files) > 100:
            return files[:100] + [f"... [Výpis zkrácen. Složka obsahuje celkem {len(files)} položek. Pokud hledáš něco konkrétního, použij vyhledávání.]"]
        return files
    except Exception as e:
        return [f"Chyba při čtení složky: {str(e)}"]

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Přečte a vrátí kompletní obsah textového nebo zdrojového souboru.
    Tento nástroj použij VŽDY, když tě uživatel požádá o vysvětlení kódu, analýzu logů nebo prozkoumání obsahu souboru.
    DŮLEŽITÉ: Jako parametry vracej POUZE platný JSON (např. {"file_path": "/home/luky/skript.py"}).
    """
    try:
        # Volitelná bezpečnostní pojistka: Zabráníme čtení extrémně velkých souborů (nad 1 MB)
        if os.path.getsize(file_path) > 1_000_000:
            return f"Chyba: Soubor {file_path} je příliš velký. Nelze jej přečíst naráz."
            
        with open(file_path, 'r', encoding='utf-8') as f:
            # Vracíme celý soubor jako jeden dlouhý string
            return f.read()
            
    except UnicodeDecodeError:
        # Záchrana pro případ, že se agent pokusí přečíst obrázek, .pyc nebo datový soubor
        return f"Chyba: Soubor {file_path} je pravděpodobně binární a nelze ho analyzovat jako text."
    except Exception as e:
        return f"Chyba při čtení souboru: {str(e)}"


if __name__ == "__main__":
    mcp.run()