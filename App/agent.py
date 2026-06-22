# kalkulacka_app/agent.py
import os
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.models.lite_llm import LiteLlm

# 1. Načtení prostředí (načte .env z nadřazené složky)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# 2. Bezpečné určení cesty k math_server.py (o složku výš)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
math_server_path = os.path.join(BASE_DIR, "math_server.py")
hello_world_server_path = os.path.join(BASE_DIR, "hello_world_server.py")
local_storage_server_path = os.path.join(BASE_DIR, "local_storage_server.py")

math_params = StdioServerParameters(command="python", args=[math_server_path])
math_tools = McpToolset(
    connection_params=StdioConnectionParams(server_params=math_params, timeout=30)
)

# 3B. Připojení DRUHÉHO FastMCP serveru (Hello World)
hello_params = StdioServerParameters(command="python", args=[hello_world_server_path])
hello_tools = McpToolset(
    connection_params=StdioConnectionParams(server_params=hello_params, timeout=30)
)

local_storage_params = StdioServerParameters(command="python", args=[local_storage_server_path])
local_storage_tools = McpToolset(
    connection_params=StdioConnectionParams(server_params=local_storage_params, timeout=30)
)

# 4. Inicializace LLM - 12 000 tokens per minute limit
# llm_provider = LiteLlm(
#     model="groq/llama-3.3-70b-versatile"
# )

# for simple tasks
# llm_provider = LiteLlm(
#     model="gemini/gemini-3.5-flash"
# )
# for more complex tasks
# llm_provider = LiteLlm(
#     model="gemini/gemini-3.5-pro"
# )

# older version:
llm_provider = LiteLlm(
    model="gemini/gemini-3.5-flash"
)

root_agent = Agent(
    name="App",
    instruction=(
        "Jsi inteligentní systémový asistent. Postupuj přesně podle těchto pravidel:\n"
        "1. OBECNÁ KONVERZACE: Pokud ti uživatel napíše zprávu, která není konkrétním požadavkem na nástroj, normálně mu odpověz a zeptej se, s čím potřebuje pomoci. Nepoužívej k tomu žádné nástroje.\n"
        "2. MATEMATIKA: Pro výpočty vždy použij matematické nástroje. Nikdy nehádej výsledek.\n"
        "3. POZDRAVY: Pokud tě uživatel požádá o pozdrav pro konkrétní jméno, použij nástroj 'hello_world'. Text, který ti nástroj vrátí, předej uživateli přesně tak, jak je, bez vlastních komentářů.\n"
        "4. SOUBORY A VYHLEDÁVÁNÍ:\n"
        "   - Pokud se uživatel ptá NA EXISTENCI konkrétního souboru nebo něco HLEDÁ (např. 'mám tu test.pdf?'), POUŽIJ NÁSTROJ 'search_files'. Parametr 'start_path' nastav na vhodnou cestu (pro Downloads např. '/home/luky/Downloads') a 'search_term' na hledaný název.\n"
        "   - Pokud uživatel vysloveně chce VYPSAT obsah konkrétního adresáře, použij nástroj 'list_all_files'.\n"
        "   - Pokud uživatel zadá relativní cestu (např. 'Downloads'), automaticky jí předřaď '/home/luky/'.\n"
        "   - Uživatel používá Ubuntu 22.04, tedy veškerá adresářová struktura je Linuxová.\n"
        "5. ČTENÍ A ANALÝZA KÓDU:\n"
        "   - Pokud tě uživatel požádá o přečtení souboru, vysvětlení zdrojového kódu, hledání chyb v implementaci nebo kontrolu konfigurace, POUŽIJ NÁSTROJ 'read_file'.\n"
        "   - DŮLEŽITÉ: Nástroj 'read_file' vyžaduje přesnou cestu k souboru. Pokud tě uživatel požádá o přečtení souboru, ale ty neznáš jeho přesnou absolutní cestu, použij NEJDŘÍVE nástroj 'search_files' k jejímu zjištění, a teprve poté zavolej 'read_file'."
    ),
    model=llm_provider,
    tools=[math_tools, hello_tools, local_storage_tools]
)