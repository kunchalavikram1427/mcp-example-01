# MCP Demo

This project demonstrates how to connect a simple **Flask REST API** with a **FastMCP server**, exposing tools, resources, and prompts.

---

## Files

* **`sample_app_flask.py`** — A Flask REST API serving dummy org/employee/project data
* **`mcp_server.py`** — A FastMCP server that:

  * Exposes tools, resources, and prompts
  * Auto-discovers the API schema via `/openapi.json`
* **`requirements.txt`** — Shared dependencies for both components

---

## Prerequisites

* Python **3+**
* `curl` (optional, for quick testing)
* (Recommended) `jq` for JSON pretty-printing

---

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

---

## Running the Applications

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

### 2. Start the MCP Server

```bash
export SAMPLE_API_BASE=http://127.0.0.1:5000  # optional (default is same)
python3 mcp_server.py stdio
```

### 3. Configure Claude MCP

Add this snippet to your Claude or VS code configuration(For MAC only. Check official documentation for Windows):

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

## Example Prompts

Try these inside Claude/VS Code after connecting the MCP server:

* *Explain `prj_002`*
* *Explain `Who is Maria`* / *Summarize Maria*
* *List all the projects handled by Maria*
* *List all my employees*
* *List all my organizations*

## MCP Inspector
```bash
npx @modelcontextprotocor inspector
```
Command
```bash
/Users/Vikram.Kunchala/Documents/MCP/venv/bin/python3 
```
Argument
```bash
/Users/Vikram.Kunchala/Documents/MCP/mcp_server.py stdio
```

## Common questions

1. `I’ve built an MCP server locally using Python’s fastmcp library. I’ve connected it to both VS Code and Claude Desktop. However, there’s a difference in behavior: Claude Desktop automatically connects to the MCP server without prompting me to start it, but VS Code requires me to manually start the server. Why does this difference exist?`

This difference comes down to how VS Code and Claude Desktop handle MCP server lifecycle management:

**Claude Desktop:**
- Automatically starts and stops MCP servers based on your configuration
- Manages the server process lifecycle behind the scenes
- When you configure an MCP server in Claude Desktop's settings, it will automatically launch the server when needed and terminate it when the session ends
- This is part of Claude Desktop's integrated MCP experience

**VS Code (with MCP extension):**
- Typically requires you to manually start the MCP server process
- The VS Code MCP extension connects to an already-running server rather than managing the server lifecycle itself
- This gives you more control over when servers start/stop, but requires manual intervention
- Some VS Code MCP extensions may have auto-start capabilities, but this varies by extension

**Why the difference:**
1. **Architecture philosophy** - Claude Desktop aims for a more seamless, integrated experience where technical details are abstracted away
2. **Process management** - Claude Desktop has built-in process management for MCP servers, while VS Code extensions often expect external process management
3. **User experience** - Claude Desktop prioritizes ease of use, while VS Code tends to give developers more direct control

If you want VS Code to auto-start your FastMCP server, you might be able to:
- Configure a VS Code task to auto-start the server
- Use a VS Code extension that supports auto-starting MCP servers
- Set up a workspace configuration that launches the server automatically