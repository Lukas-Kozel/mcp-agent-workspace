# Local AI Agent Workspace with FastMCP

This repository contains a fully functional local AI agent architecture built using the **Google Agent Development Kit (ADK)** and the **Model Context Protocol (MCP)**. 

The agent utilizes Groq's high-speed inference API (Llama 3.3 70B) as its reasoning engine and securely communicates with a custom local FastMCP server to execute precise mathematical operations, demonstrating a complete "Tool Calling" loop.

## 📂 Project Structure

```text
.
├── agent_app.py             # CLI version of the agent with an explicit Runner
├── math_server.py           # Custom FastMCP server (provides math tools via stdio)
├── kalkulacka_app/          # Directory structured specifically for the ADK Web Server
│   └── agent.py             # Web version of the agent (exposes `root_agent`)
├── .env                     # Environment variables (NOT tracked in Git)
├── .gitignore               # Git ignore rules (excludes venv and .env)
└── README.md                # Project documentation