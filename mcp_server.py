"""
MCP server using FastMCP that discovers and calls the Flask sample app.
Run:
  # in a separate shell (Flask app already running at 127.0.0.1:5000)
  pip install -r requirements.txt
  python mcp_server.py stdio  (attach from an MCP-compatible client like Claude Desktop)
Env:
  SAMPLE_API_BASE (default: http://127.0.0.1:5000)
  SAMPLE_API_KEY  (optional: sent as x-api-key)
Tools exposed:
  list_employees, get_employee, search_employees,
  list_projects, get_project, list_org_units, discover_endpoints
"""
from __future__ import annotations
import os, json
from typing import Any, Optional
import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Org MCP Server")
BASE_URL = os.getenv("SAMPLE_API_BASE", "http://127.0.0.1:5000").rstrip("/")
API_KEY = os.getenv("SAMPLE_API_KEY", "")

HEADERS: dict[str, str] = {"Accept": "application/json"}
if API_KEY:
    HEADERS["x-api-key"] = API_KEY

# -----------------------------
# HTTP helper
# -----------------------------
async def _get_json(path: str, params: Optional[dict[str, Any]] = None) -> Any:
    url = f"{BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=15, headers=HEADERS) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()

# -----------------------------
# Tools: Employees
# -----------------------------
@mcp.tool()
async def list_employees(skip: int = 0, limit: int = 100) -> dict:
    """List employees with pagination."""
    return await _get_json("/employees", {"skip": skip, "limit": limit})

@mcp.tool()
async def get_employee(emp_id: str) -> dict:
    """Get an employee by id (e.g., emp_001)."""
    return await _get_json(f"/employees/{emp_id}")

@mcp.tool()
async def search_employees(q: str) -> dict:
    """Full-text search over name/title/skills."""
    return await _get_json("/employees/search", {"q": q})

# -----------------------------
# Tools: Projects
# -----------------------------
@mcp.tool()
async def list_projects(skip: int = 0, limit: int = 100) -> dict:
    """List projects with pagination."""
    return await _get_json("/projects", {"skip": skip, "limit": limit})

@mcp.tool()
async def get_project(project_id: str) -> dict:
    """Get a project by id (e.g., prj_001)."""
    return await _get_json(f"/projects/{project_id}")

# -----------------------------
# Tools: Org
# -----------------------------
@mcp.tool()
async def list_org_units() -> dict:
    """List organization units."""
    return await _get_json("/org/units")

# -----------------------------
# Discovery tool
# -----------------------------
@mcp.tool()
async def discover_endpoints() -> dict:
    """Return the OpenAPI document from the sample app for client-side inspection."""
    return await _get_json("/openapi.json")


if __name__ == "__main__":
    # Run with stdio transport; attach from an MCP-aware client
    mcp.run()