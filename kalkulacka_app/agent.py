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
server_path = os.path.join(BASE_DIR, "math_server.py")

# 3. Připojení lokálního FastMCP serveru
server_params = StdioServerParameters(
    command="python",
    args=[server_path]
)

math_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=server_params,
        timeout=30
    )
)

# 4. Inicializace LLM
llm_provider = LiteLlm(
    model="groq/llama-3.3-70b-versatile"
)

# 5. Samotný Agent (MUSÍ se jmenovat root_agent)
root_agent = Agent(
    name="Kalkulacka",
    instruction=(
        "Jsi precizní matematický asistent. Tvojí jedinou úlohou je řešit "
        "matematické požadavky uživatele. Pro výpočty NESMÍŠ hádat výsledky "
        "sám, ale musíš VŽDY striktně použít dostupné nástroje (tools)."
    ),
    model=llm_provider,
    tools=[math_tools]
)