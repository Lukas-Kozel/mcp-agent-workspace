# agent_app.py
import asyncio
import os
from dotenv import load_dotenv

# Nové importy pro orchestraci (Runner) a paměť (Session)
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.models.lite_llm import LiteLlm

async def main():
    load_dotenv()
    
    print("1. Konfigurace MCP Toolsetu (Vlastní Math Server)...")
    server_params = StdioServerParameters(
        command="python",
        args=["math_server.py"]
    )
    
    math_tools = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=server_params,
            timeout=30
        )
    )

    print("2. Inicializace modelu Groq přes LiteLLM...")
    llm_provider = LiteLlm(
        model="groq/llama-3.3-70b-versatile"
    )

    print("3. Sestavení Agenta...")
    agent = Agent(
        name="Kalkulacka",
        instruction=(
            "Jsi precizní matematický asistent. Tvojí jedinou úlohou je řešit "
            "matematické požadavky uživatele. Pro výpočty NESMÍŠ hádat výsledky "
            "sám, ale musíš VŽDY striktně použít dostupné nástroje (tools)."
        ),
        model=llm_provider,
        tools=[math_tools]
    )

    print("4. Inicializace Runneru a lokální paměti (Session)...")
    # Vytvoření služby pro ukládání historie zpráv v paměti RAM
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name="KalkulackaApp", user_id="user_lokalni")
    
    # Injektáž agenta a paměti do Runneru
    runner = Runner(
        app_name="KalkulackaApp", 
        agent=agent, 
        session_service=session_service
    )

    print("\n--- Start konverzace s Agentem ---\n")
    user_prompt = "Ahoj, můžeš mi prosím sečíst přesně 2 a 1?"
    print(f"Uživatel: {user_prompt}")
    
    # 5. Zabalení textu do formátu, kterému ADK rozumí
    content = types.Content(role="user", parts=[types.Part(text=user_prompt)])
    
    print("\nAgent:")
    # Spuštění Runneru. Ten se automaticky postará o Context a Tool Calling.
    async for event in runner.run_async(
        user_id="user_lokalni", 
        session_id=session.id, 
        new_message=content
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)
        else:
            print(f"[Debug] Interní krok agenta: {type(event).__name__}")

    # --- PŘIDÁNO: Korektní ukončení IPC a síťových spojení ---
    print("\n[Ukončování] Úklid procesů a spojení...")
    await math_tools.close()
    
    # Krátká pauza, aby event loop stihl zpracovat všechny pending tasky (např. SSL teardown)
    await asyncio.sleep(0.1) 
    print("[Ukončování] Hotovo.")

if __name__ == "__main__":
    asyncio.run(main())