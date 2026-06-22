# Local AI Coding Assistant with FastMCP

This repository contains a fully functional, local AI coding assistant built using the **Google Agent Development Kit (ADK)** and the **Model Context Protocol (MCP)**. 

Moving beyond simple tool execution, this architecture acts as a powerful development companion. It utilizes Google's **Gemini Flash (via LiteLLM)** to leverage its massive context window (1M+ tokens), allowing the agent to recursively search local directories, read source code, analyze logic, and perform precise mathematical operations—all through a secure, local Tool Calling loop.

## ✨ Features

* **Advanced Context Handling:** Powered by Google Gemini API to seamlessly process large codebases and multiple files at once.
* **Local File System Access:** Securely searches for files and reads source code directly from the local machine using defensive programming techniques (preventing token overflow).
* **Multi-Tool Orchestration:** Simultaneously manages multiple independent FastMCP servers (Math, Greetings, Local Storage).
* **Visual Debugging:** Fully integrated with Google ADK Web UI for real-time trace inspection and latency monitoring.

## 📂 Project Structure

```text
.
├── math_server.py           # FastMCP server: Provides exact math operations
├── hello_world_server.py    # FastMCP server: Handles localized user greetings
├── local_storage_server.py  # FastMCP server: Directory search and safe file reading
├── kalkulacka_app/          # ADK Web Server application directory
│   └── agent.py             # The core Agent definition, instructions, and tool routing
├── agent_app.py             # (Legacy) CLI version of the agent with an explicit Runner
├── .env                     # Environment variables (NOT tracked in Git)
├── .gitignore               # Git ignore rules (excludes venv and .env)
└── README.md                # Project documentation