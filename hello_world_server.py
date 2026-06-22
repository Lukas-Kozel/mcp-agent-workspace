from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hello_world_server")

@mcp.tool()
def hello_world(name: str) -> str:
    """
    Vrátí pozdrav uživateli.
    Tento nástroj použij VŽDY, když tě uživatel požádá o pozdrav.
    """
    return f"Ahoj, {name}! Vítej v našem systému."

if __name__ == "__main__":
    mcp.run()