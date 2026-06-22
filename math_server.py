from mcp.server.fastmcp import FastMCP

mcp = FastMCP("math_server")

@mcp.tool()
def add_numbers(a: any, b: any) -> float:
    """
    Sečte dvě čísla, která mohou být zadána libovolně, převede je na float a vrátí jejich součet. 
    Tento nástroj použij VŽDY, když tě uživatel požádá o sčítání.
    """
    return float(a) + float(b)

if __name__ == "__main__":
    mcp.run()