from mcp.server.fastmcp import FastMCP

mcp = FastMCP("math_server")

@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """
    Sečte dvě čísla a vrátí jejich součet. 
    Tento nástroj použij VŽDY, když tě uživatel požádá o sčítání.
    """
    return a + b

if __name__ == "__main__":
    mcp.run()