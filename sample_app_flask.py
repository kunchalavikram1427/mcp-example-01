"""
Sample Org REST API using Flask.
Run:  
  pip install flask httpx python-dotenv fastmcp  
  python sample_app_flask.py  (starts at http://127.0.0.1:5000)
Endpoints: /employees, /employees/<id>, /employees/search?q=, /projects, /projects/<id>, /org/units, /healthz, /openapi.json
"""
from __future__ import annotations
from flask import Flask, request, jsonify
from typing import List, Dict, Any

app = Flask(__name__)

# ------------------ Dummy Data ------------------
EMPLOYEES: List[Dict[str, Any]] = [
    {
        "id": "emp_001",
        "name": "Asha Rao",
        "title": "Senior DevOps Engineer",
        "email": "asha.rao@example.com",
        "org_unit": "ou_eng",
        "skills": ["kubernetes", "terraform", "aws"],
        "project_ids": ["prj_001", "prj_003"],
    },
    {
        "id": "emp_002",
        "name": "Kenji Tanaka",
        "title": "Backend Developer",
        "email": "kenji.tanaka@example.com",
        "org_unit": "ou_eng",
        "skills": ["python", "flask", "postgres"],
        "project_ids": ["prj_002"],
    },
    {
        "id": "emp_003",
        "name": "Maria Garcia",
        "title": "Project Manager",
        "email": "maria.garcia@example.com",
        "org_unit": "ou_pm",
        "skills": ["scrum", "kanban"],
        "project_ids": ["prj_001", "prj_002"],
    },
]

PROJECTS: List[Dict[str, Any]] = [
    {
        "id": "prj_001",
        "name": "Orion",
        "description": "Next-gen CI/CD observability.",
        "owner_id": "emp_003",
        "tags": ["devops", "observability"],
    },
    {
        "id": "prj_002",
        "name": "Kitsune",
        "description": "Payments gateway refactor.",
        "owner_id": "emp_002",
        "tags": ["backend", "payments"],
    },
    {
        "id": "prj_003",
        "name": "Nimbus",
        "description": "Internal developer platform.",
        "owner_id": "emp_001",
        "tags": ["platform", "idp"],
    },
]

ORG_UNITS: List[Dict[str, Any]] = [
    {"id": "ou_eng", "name": "Engineering", "parent_id": None},
    {"id": "ou_pm", "name": "Program Management", "parent_id": None},
]

# ------------------ Routes ------------------
@app.get("/employees")
def list_employees():
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 100))
    except ValueError:
        skip, limit = 0, 100
    return {"total": len(EMPLOYEES), "items": EMPLOYEES[skip: skip + limit]}

@app.get("/employees/<emp_id>")
def get_employee(emp_id: str):
    for e in EMPLOYEES:
        if e["id"] == emp_id:
            return e
    return jsonify({"detail": "Employee not found"}), 404

@app.get("/employees/search")
def search_employees():
    q = (request.args.get("q") or "").strip().lower()
    if not q:
        return {"total": 0, "items": []}
    matched = [
        e for e in EMPLOYEES
        if q in e["name"].lower() or q in e["title"].lower() or any(q in s.lower() for s in e.get("skills", []))
    ]
    return {"total": len(matched), "items": matched}

@app.get("/projects")
def list_projects():
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 100))
    except ValueError:
        skip, limit = 0, 100
    return {"total": len(PROJECTS), "items": PROJECTS[skip: skip + limit]}

@app.get("/projects/<project_id>")
def get_project(project_id: str):
    for p in PROJECTS:
        if p["id"] == project_id:
            return p
    return jsonify({"detail": "Project not found"}), 404

@app.get("/org/units")
def list_org_units():
    return {"total": len(ORG_UNITS), "items": ORG_UNITS}

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/openapi.json")
def openapi():
    # Minimal OpenAPI 3.0 document for discovery by the MCP server
    spec = {
        "openapi": "3.0.0",
        "info": {"title": "Sample Org API", "version": "1.0.0"},
        "paths": {
            "/employees": {
                "get": {
                    "summary": "List employees",
                    "parameters": [
                        {"name": "skip", "in": "query", "schema": {"type": "integer"}},
                        {"name": "limit", "in": "query", "schema": {"type": "integer"}},
                    ],
                    "responses": {"200": {"description": "OK"}},
                }
            },
            "/employees/{emp_id}": {
                "get": {
                    "summary": "Get employee",
                    "parameters": [
                        {"name": "emp_id", "in": "path", "required": True, "schema": {"type": "string"}},
                    ],
                    "responses": {"200": {"description": "OK"}, "404": {"description": "Not Found"}},
                }
            },
            "/employees/search": {
                "get": {
                    "summary": "Search employees",
                    "parameters": [
                        {"name": "q", "in": "query", "required": True, "schema": {"type": "string"}},
                    ],
                    "responses": {"200": {"description": "OK"}},
                }
            },
            "/projects": {
                "get": {
                    "summary": "List projects",
                    "parameters": [
                        {"name": "skip", "in": "query", "schema": {"type": "integer"}},
                        {"name": "limit", "in": "query", "schema": {"type": "integer"}},
                    ],
                    "responses": {"200": {"description": "OK"}},
                }
            },
            "/projects/{project_id}": {
                "get": {
                    "summary": "Get project",
                    "parameters": [
                        {"name": "project_id", "in": "path", "required": True, "schema": {"type": "string"}},
                    ],
                    "responses": {"200": {"description": "OK"}, "404": {"description": "Not Found"}},
                }
            },
            "/org/units": {
                "get": {"summary": "List org units", "responses": {"200": {"description": "OK"}}}
            },
            "/healthz": {"get": {"summary": "Health", "responses": {"200": {"description": "OK"}}}},
        },
    }
    return jsonify(spec)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)