"""
Sample Org REST API using Flask.
Run:
  pip install -r requirements.txt
  python sample_app_flask.py  (starts at http://127.0.0.1:5000)
Endpoints: /employees, /employees/<id>, /employees/search?q=, /projects, /projects/<id>, /org/units, /healthz, /openapi.json
"""
from __future__ import annotations
from flask import Flask, request, jsonify
from typing import List, Dict, Any

app = Flask(__name__)

# ------------------ Data ------------------
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
    # --- appended employees (do not modify or reorder the three above) ---
    {
        "id": "emp_004",
        "name": "Liam O'Connor",
        "title": "Cloud Architect",
        "email": "liam.oconnor@example.com",
        "org_unit": "ou_platform",
        "skills": ["aws", "eks", "vpc", "terraform"],
        "project_ids": ["prj_004", "prj_006"],
    },
    {
        "id": "emp_005",
        "name": "Priya Nair",
        "title": "MLOps Engineer",
        "email": "priya.nair@example.com",
        "org_unit": "ou_data",
        "skills": ["mlops", "sagemaker", "kubeflow", "docker", "python"],
        "project_ids": ["prj_005", "prj_007"],
    },
    {
        "id": "emp_006",
        "name": "Diego Alvarez",
        "title": "Site Reliability Engineer",
        "email": "diego.alvarez@example.com",
        "org_unit": "ou_ops",
        "skills": ["kubernetes", "prometheus", "grafana", "loki", "chaos engineering"],
        "project_ids": ["prj_004", "prj_001"],
    },
    {
        "id": "emp_007",
        "name": "Elena Petrova",
        "title": "Data Scientist",
        "email": "elena.petrova@example.com",
        "org_unit": "ou_data",
        "skills": ["pandas", "sklearn", "pytorch", "ml", "genai"],
        "project_ids": ["prj_005"],
    },
    {
        "id": "emp_008",
        "name": "Yusuf Khan",
        "title": "Security Engineer",
        "email": "yusuf.khan@example.com",
        "org_unit": "ou_sec",
        "skills": ["iam", "kms", "security hub", "kyverno", "opa"],
        "project_ids": ["prj_008"],
    },
    {
        "id": "emp_009",
        "name": "Hannah Lee",
        "title": "QA Automation Engineer",
        "email": "hannah.lee@example.com",
        "org_unit": "ou_qa",
        "skills": ["pytest", "cypress", "k6", "github actions"],
        "project_ids": ["prj_006"],
    },
    {
        "id": "emp_010",
        "name": "Arjun Mehta",
        "title": "Platform Engineer",
        "email": "arjun.mehta@example.com",
        "org_unit": "ou_platform",
        "skills": ["argocd", "gitops", "crossplane", "helm"],
        "project_ids": ["prj_006", "prj_003"],
    },
    {
        "id": "emp_011",
        "name": "Mei Chen",
        "title": "AI Engineer",
        "email": "mei.chen@example.com",
        "org_unit": "ou_research",
        "skills": ["llm", "rag", "bedrock", "langchain", "vector databases"],
        "project_ids": ["prj_007", "prj_009"],
    },
    {
        "id": "emp_012",
        "name": "Oliver Smith",
        "title": "FinOps Analyst",
        "email": "oliver.smith@example.com",
        "org_unit": "ou_ops",
        "skills": ["cost explorer", "rightsizing", "savings plans", "kubecost"],
        "project_ids": ["prj_010"],
    },
    {
        "id": "emp_013",
        "name": "Sofia Rossi",
        "title": "DevSecOps Engineer",
        "email": "sofia.rossi@example.com",
        "org_unit": "ou_sec",
        "skills": ["snyk", "trivy", "kyverno", "opa", "cicd"],
        "project_ids": ["prj_008", "prj_006"],
    },
    {
        "id": "emp_014",
        "name": "Takeshi Yamamoto",
        "title": "Edge/IoT Engineer",
        "email": "takeshi.yamamoto@example.com",
        "org_unit": "ou_eng",
        "skills": ["greengrass", "mqtt", "iot core", "rust"],
        "project_ids": ["prj_011"],
    },
    {
        "id": "emp_015",
        "name": "Zanele Dlamini",
        "title": "Data Engineer",
        "email": "zanele.dlamini@example.com",
        "org_unit": "ou_data",
        "skills": ["glue", "emr", "spark", "lake formation"],
        "project_ids": ["prj_012"],
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
    # --- appended projects (do not modify or reorder the three above) ---
    {
        "id": "prj_004",
        "name": "EKSify",
        "description": "AWS EKS standardization and blue/green upgrades with Argo Rollouts.",
        "owner_id": "emp_006",
        "tags": ["kubernetes", "eks", "gitops", "devops"],
    },
    {
        "id": "prj_005",
        "name": "SageTrail",
        "description": "MLOps pipeline on AWS SageMaker including feature store and model registry.",
        "owner_id": "emp_005",
        "tags": ["mlops", "sagemaker", "ml", "aws"],
    },
    {
        "id": "prj_006",
        "name": "Shipwright",
        "description": "GitOps CD with Argo CD and Crossplane-managed infrastructure for multi-tenant clusters.",
        "owner_id": "emp_010",
        "tags": ["gitops", "argocd", "crossplane", "kubernetes"],
    },
    {
        "id": "prj_007",
        "name": "Atlas-RAG",
        "description": "Retrieval-Augmented Generation platform using Bedrock and OpenSearch vector store.",
        "owner_id": "emp_011",
        "tags": ["genai", "rag", "bedrock", "vector"],
    },
    {
        "id": "prj_008",
        "name": "GuardRail",
        "description": "Policy-as-code and container security with Kyverno, Trivy, and OPA.",
        "owner_id": "emp_008",
        "tags": ["security", "devsecops", "kyverno", "opa"],
    },
    {
        "id": "prj_009",
        "name": "ModelMonitor",
        "description": "LLM evaluation and telemetry using MLflow and custom evaluation suites.",
        "owner_id": "emp_011",
        "tags": ["ai", "llm", "observability", "mlflow"],
    },
    {
        "id": "prj_010",
        "name": "ThriftOps",
        "description": "AWS cost optimization with rightsizing and savings plans automation.",
        "owner_id": "emp_012",
        "tags": ["finops", "aws", "cost-optimization"],
    },
    {
        "id": "prj_011",
        "name": "EdgeLink",
        "description": "IoT edge orchestration using AWS IoT Greengrass and K3s.",
        "owner_id": "emp_014",
        "tags": ["iot", "edge", "aws", "kubernetes"],
    },
    {
        "id": "prj_012",
        "name": "DataLakehouse",
        "description": "ETL to an S3-based lakehouse with Glue, EMR, and Iceberg.",
        "owner_id": "emp_015",
        "tags": ["data", "etl", "aws", "lakehouse"],
    },
]

ORG_UNITS: List[Dict[str, Any]] = [
    {"id": "ou_eng", "name": "Engineering", "parent_id": None},
    {"id": "ou_pm", "name": "Program Management", "parent_id": None},
    # --- appended org units (do not modify or reorder the two above) ---
    {"id": "ou_ops", "name": "SRE/Operations", "parent_id": None},
    {"id": "ou_platform", "name": "Platform Engineering", "parent_id": "ou_eng"},
    {"id": "ou_data", "name": "Data & AI", "parent_id": "ou_eng"},
    {"id": "ou_sec", "name": "Security", "parent_id": None},
    {"id": "ou_research", "name": "AI Research", "parent_id": "ou_data"},
    {"id": "ou_qa", "name": "Quality Engineering", "parent_id": "ou_eng"},
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