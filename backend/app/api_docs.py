import re
from flask import jsonify, render_template_string


_PATH_PARAM_RE = re.compile(r"<(?:[^:<>]+:)?([^<>]+)>")
_JSON_SCHEMA_OBJECT = {
    "type": "object",
    "additionalProperties": True,
}

_COMPONENT_SCHEMAS = {
    "GoogleAuthRequest": {
        "type": "object",
        "required": ["token"],
        "properties": {
            "token": {"type": "string"},
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "screenName": {"type": "string"},
        },
    },
    "SignupRequest": {
        "type": "object",
        "required": ["email", "password", "screenName"],
        "properties": {
            "email": {"type": "string", "format": "email"},
            "password": {"type": "string", "minLength": 6},
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "screenName": {"type": "string"},
        },
    },
    "LoginRequest": {
        "type": "object",
        "required": ["email", "password"],
        "properties": {
            "email": {"type": "string", "format": "email"},
            "password": {"type": "string"},
        },
    },
    "UpdateProfileRequest": {
        "type": "object",
        "required": ["firstName", "lastName", "screenName"],
        "properties": {
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "screenName": {"type": "string"},
        },
    },
    "ProblemSelectionRequest": {
        "type": "object",
        "required": ["total"],
        "properties": {
            "total": {"type": "integer", "minimum": 1},
            "tags": {"type": "array", "items": {"type": "string"}},
            "ignoreSlugs": {"type": "array", "items": {"type": "string"}},
            "difficultyCounts": {
                "type": "object",
                "properties": {
                    "easy": {"type": "integer", "minimum": 0},
                    "medium": {"type": "integer", "minimum": 0},
                    "hard": {"type": "integer", "minimum": 0},
                },
            },
        },
    },
    "ProblemCreateRequest": {
        "type": "object",
        "required": ["slug", "title", "difficulty", "description", "starterCode", "examples", "testCases"],
        "properties": {
            "slug": {"type": "string"},
            "title": {"type": "string"},
            "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
            "description": {"type": "string"},
            "starterCode": {"type": "string"},
            "comparisonStrategy": {
                "type": "string",
                "enum": ["exact", "unordered", "unordered_nested", "float", "set"],
            },
            "examples": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "input": {"type": "string"},
                        "output": {"type": "string"},
                        "explanation": {"type": "string"},
                    },
                },
            },
            "testCases": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "function": {"type": "string"},
                        "input": {},
                        "expectedOutput": {},
                        "isActive": {"type": "boolean"},
                    },
                },
            },
            "tags": {"type": "array", "items": {"type": "string"}},
            "ingestKey": {"type": "string"},
        },
    },
    "CreateProjectRequest": {
        "type": "object",
        "required": ["name"],
        "properties": {
            "name": {"type": "string", "maxLength": 25},
        },
    },
    "SubmitCodeRequest": {
        "type": "object",
        "required": ["problemSlug", "code"],
        "properties": {
            "problemSlug": {"type": "string"},
            "projectId": {"type": "string"},
            "code": {"type": "string"},
        },
    },
    "SubmissionRequest": {
        "type": "object",
        "required": ["problemSlug", "projectId", "code"],
        "properties": {
            "problemSlug": {"type": "string"},
            "projectId": {"type": "string"},
            "code": {"type": "string"},
        },
    },
    "FavoriteCreateRequest": {
        "type": "object",
        "required": ["problemId"],
        "properties": {
            "problemId": {"type": "string"},
        },
    },
    "ContactCreateRequest": {
        "type": "object",
        "required": ["name", "email", "subject", "message"],
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "subject": {"type": "string"},
            "message": {"type": "string"},
        },
    },
    "ContactStatusUpdateRequest": {
        "type": "object",
        "required": ["status"],
        "properties": {
            "status": {"type": "string", "enum": ["pending", "read", "responded"]},
        },
    },
    "CheckoutSessionRequest": {
        "type": "object",
        "properties": {
            "redirect": {"type": "string", "description": "Safe frontend relative redirect path"},
        },
    },
}


def _schema_ref(name: str):
    return {"$ref": f"#/components/schemas/{name}"}


_REQUEST_SCHEMA_BY_OPERATION = {
    ("POST", "/auth/google"): _schema_ref("GoogleAuthRequest"),
    ("POST", "/auth/signup"): _schema_ref("SignupRequest"),
    ("POST", "/auth/login"): _schema_ref("LoginRequest"),
    ("POST", "/auth/profile"): _schema_ref("UpdateProfileRequest"),
    ("POST", "/problems/select"): _schema_ref("ProblemSelectionRequest"),
    ("POST", "/problems/public-ingest"): _schema_ref("ProblemCreateRequest"),
    ("POST", "/problems/"): _schema_ref("ProblemCreateRequest"),
    ("POST", "/projects/"): _schema_ref("CreateProjectRequest"),
    ("POST", "/projects/{project_id}/submit"): _schema_ref("SubmitCodeRequest"),
    ("POST", "/submissions/run"): _schema_ref("SubmitCodeRequest"),
    ("POST", "/submissions/"): _schema_ref("SubmissionRequest"),
    ("POST", "/favorites/"): _schema_ref("FavoriteCreateRequest"),
    ("POST", "/contact/"): _schema_ref("ContactCreateRequest"),
    ("PUT", "/contact/{contact_id}"): _schema_ref("ContactStatusUpdateRequest"),
    ("POST", "/billing/checkout-session"): _schema_ref("CheckoutSessionRequest"),
    ("POST", "/billing/webhook"): _JSON_SCHEMA_OBJECT,
}

_QUERY_PARAMS_BY_OPERATION = {
    ("GET", "/problems/"): [
        {"name": "difficulty", "in": "query", "schema": {"type": "string", "enum": ["easy", "medium", "hard"]}},
        {"name": "tag", "in": "query", "schema": {"type": "string"}},
        {"name": "search", "in": "query", "schema": {"type": "string"}},
        {"name": "sort", "in": "query", "schema": {"type": "string", "enum": ["id", "difficulty", "created_at"]}},
        {"name": "order", "in": "query", "schema": {"type": "string", "enum": ["asc", "desc"]}},
        {"name": "page", "in": "query", "schema": {"type": "integer", "minimum": 1}},
        {"name": "per_page", "in": "query", "schema": {"type": "integer", "minimum": 1, "maximum": 50}},
    ],
    ("GET", "/auth/screen-name-availability"): [
        {"name": "screenName", "in": "query", "required": True, "schema": {"type": "string"}},
        {"name": "excludeUserId", "in": "query", "schema": {"type": "string"}},
    ],
    ("GET", "/submissions/all"): [
        {"name": "projectId", "in": "query", "schema": {"type": "string"}},
    ],
    ("GET", "/submissions/problem/{slug}"): [
        {"name": "projectId", "in": "query", "schema": {"type": "string"}},
    ],
    ("GET", "/submissions/difficulty-stats"): [
        {"name": "userId", "in": "query", "schema": {"type": "string"}},
    ],
}

_JWT_PROTECTED_OPERATIONS = {
    ("GET", "/auth/me"),
    ("GET", "/auth/profile"),
    ("POST", "/auth/profile"),
    ("POST", "/problems/"),
    ("GET", "/projects/"),
    ("POST", "/projects/"),
    ("POST", "/projects/{project_id}/set-default"),
    ("DELETE", "/projects/{project_id}"),
    ("POST", "/projects/{project_id}/submit"),
    ("POST", "/submissions/run"),
    ("POST", "/submissions/"),
    ("GET", "/submissions/{sub_id}"),
    ("GET", "/submissions/all"),
    ("GET", "/submissions/accepted"),
    ("GET", "/submissions/problem/{slug}"),
    ("GET", "/submissions/difficulty-stats"),
    ("GET", "/favorites/"),
    ("POST", "/favorites/"),
    ("DELETE", "/favorites/{problem_id}"),
    ("GET", "/favorites/check/{problem_id}"),
    ("GET", "/billing/subscription"),
    ("GET", "/billing/access-status"),
    ("POST", "/billing/start-trial"),
    ("POST", "/billing/checkout-session"),
}
_SWAGGER_UI_HTML = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>PyPyCode API Docs</title>
    <link
      rel=\"stylesheet\"
      href=\"https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css\"
    />
    <style>
      html { box-sizing: border-box; overflow-y: scroll; }
      *, *:before, *:after { box-sizing: inherit; }
      body { margin: 0; background: #fafafa; }
    </style>
  </head>
  <body>
    <div id=\"swagger-ui\"></div>
    <script src=\"https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js\"></script>
    <script src=\"https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js\"></script>
    <script>
      window.ui = SwaggerUIBundle({
        url: "{{ spec_url }}",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset,
        ],
        layout: "StandaloneLayout",
      });
    </script>
  </body>
</html>
"""


def _to_openapi_path(rule: str) -> str:
    return _PATH_PARAM_RE.sub(r"{\1}", rule)


def _path_tag(path: str) -> str:
    parts = [part for part in path.split("/") if part]
    return parts[0] if parts else "misc"


def _operation_overrides(method: str, openapi_path: str):
    op_key = (method, openapi_path)
    return {
        "request_schema": _REQUEST_SCHEMA_BY_OPERATION.get(op_key),
        "query_parameters": _QUERY_PARAMS_BY_OPERATION.get(op_key, []),
        "requires_jwt": op_key in _JWT_PROTECTED_OPERATIONS,
    }


def _operation_for(app, rule, method: str, openapi_path: str):
    view_func = app.view_functions.get(rule.endpoint)
    doc = (view_func.__doc__ or "").strip() if view_func else ""
    summary = doc.splitlines()[0] if doc else f"{method} {rule.rule}"
    overrides = _operation_overrides(method, openapi_path)

    op = {
        "tags": [_path_tag(rule.rule)],
        "summary": summary,
        "operationId": f"{rule.endpoint}_{method.lower()}",
        "responses": {
            "200": {"description": "Success"},
        },
    }

    if rule.arguments:
        op["parameters"] = [
            {
                "name": arg,
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            }
            for arg in sorted(rule.arguments)
        ]
    else:
        op["parameters"] = []

    if overrides["query_parameters"]:
        op["parameters"].extend(overrides["query_parameters"])

    if not op["parameters"]:
        op.pop("parameters")

    if overrides["request_schema"] is not None:
        op["requestBody"] = {
            "required": False,
            "content": {
                "application/json": {
                    "schema": overrides["request_schema"]
                }
            },
        }

    if overrides["requires_jwt"]:
        op["security"] = [{"BearerAuth": []}]

    return op


def _build_openapi_spec(app):
    paths = {}

    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        if rule.endpoint == "static":
            continue

        methods = sorted((rule.methods or set()) - {"HEAD", "OPTIONS"})
        if not methods:
            continue

        openapi_path = _to_openapi_path(rule.rule)
        path_item = paths.setdefault(openapi_path, {})

        for method in methods:
            path_item[method.lower()] = _operation_for(app, rule, method, openapi_path)

    return {
        "openapi": "3.0.3",
        "info": {
            "title": "PyPyCode API",
            "version": "1.0.0",
            "description": "Auto-generated OpenAPI docs from Flask routes.",
        },
        "servers": [
            {"url": "/api", "description": "Nginx proxied API"},
            {"url": "/", "description": "Direct backend API"},
        ],
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
            "schemas": _COMPONENT_SCHEMAS,
        },
        "paths": paths,
    }


def register_api_docs(app):
    @app.get("/openapi.json")
    def openapi_json():
        return jsonify(_build_openapi_spec(app))

    @app.get("/docs")
    def docs_ui():
        return render_template_string(_SWAGGER_UI_HTML, spec_url="openapi.json")
