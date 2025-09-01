# MCP + Flask Sample (Two-file Demo)

This project demonstrates how to connect a simple **Flask REST API** with a **FastMCP server**, exposing tools, resources, and prompts. It also includes an example Claude MCP client configuration.

---

## 📂 Files

* **`sample_app_flask.py`** — A Flask REST API serving dummy org/employee/project data
* **`mcp_server.py`** — A FastMCP server that:

  * Exposes tools, resources, and prompts
  * Auto-discovers the API schema via `/openapi.json`
* **`requirements.txt`** — Shared dependencies for both components

---

## ✅ Prerequisites

* Python **3.11+**
* `curl` (optional, for quick testing)
* (Recommended) `jq` for JSON pretty-printing

---

## ⚙️ Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

---

## 🚀 Running the Applications

### 1. Start the Flask Sample App

```bash
python3 sample_app_flask.py
```

Verify endpoints:

```bash
curl -s http://127.0.0.1:5000/healthz
curl -s http://127.0.0.1:5000/employees | jq
curl -s "http://127.0.0.1:5000/employees/search?q=dev" | jq
```

---

### 2. Start the MCP Server

```bash
export SAMPLE_API_BASE=http://127.0.0.1:5000  # optional (default is same)
python3 mcp_server.py stdio
```

---

### 3. Configure Claude MCP

Add this snippet to your Claude or VS code configuration:

- For Claude(`~/Library/Application\ Support/Claude/claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "org_mcp": {
      "type": "stdio",
      "command": "/Users/Vikram.Kunchala/Documents/MCP/venv/bin/python3",
      "args": [
        "/Users/Vikram.Kunchala/Documents/MCP/mcp_server.py",
        "stdio"
      ],
      "env": {
        "SAMPLE_API_BASE": "http://127.0.0.1:5000"
      }
    }
  }
}
```

- For VS Code(`~/Library/Application\ Support/Code/User/mcp.json`)

```json
{
  "mcpServers": {
    "org_mcp": {
      "type": "stdio",
      "command": "/Users/Vikram.Kunchala/Documents/MCP/venv/bin/python3",
      "args": [
        "/Users/Vikram.Kunchala/Documents/MCP/mcp_server.py",
        "stdio"
      ],
      "env": {
        "SAMPLE_API_BASE": "http://127.0.0.1:5000"
      }
    }
  }
}
```

---

## 💬 Example Prompts

Try these inside Claude after connecting the MCP server:

* *Explain `prj_002`*
* *Explain `Who is Maria`* / *Summarize Maria*
* *List all the projects handled by Maria*
* *List all my employees*
* *List all my organizations*

## MCP Inspector

```bash
npx @modelcontextprotocor inspector
```
```bash
/Users/Vikram.Kunchala/Documents/MCP/venv/bin/python3 

/Users/Vikram.Kunchala/Documents/MCP/mcp_server.py stdio
```