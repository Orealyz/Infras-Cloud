import ast
import yaml

# URL de ton service Cloud Run
CLOUD_RUN_URL = "https://flask-api-513126423995.europe-west9.run.app"

# Lecture du fichier main.py
with open("main.py") as f:
    tree = ast.parse(f.read())

routes = []

# Parcours AST pour récupérer toutes les routes Flask
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        for deco in node.decorator_list:
            if isinstance(deco, ast.Call) and getattr(deco.func, "attr", "") == "route":
                # Récupération du chemin
                path = None
                arg0 = deco.args[0]
                if hasattr(arg0, "s"):       # ancien format
                    path = arg0.s
                elif hasattr(arg0, "value"): # Python 3.12+
                    path = arg0.value

                # Récupération des méthodes
                methods = []
                if deco.keywords:
                    for kw in deco.keywords:
                        if kw.arg == "methods":
                            for elt in kw.value.elts:
                                if hasattr(elt, "s"):
                                    methods.append(elt.s)
                                elif hasattr(elt, "value"):
                                    methods.append(elt.value)
                if not methods:
                    methods = ["GET"]

                routes.append({
                    "path": path,
                    "methods": methods,
                    "function": node.name
                })

# Génération du Swagger
swagger = {
    "swagger": "2.0",
    "info": {"title": "Flask API", "version": "1.0.0"},
    "paths": {}
}

for r in routes:
    path_obj = {}

    # OPTIONS pour CORS
    if "OPTIONS" in r["methods"]:
        path_obj["options"] = {
            "summary": "CORS support",
            "operationId": r["function"] + "Options",
            "x-google-backend": {
                "address": CLOUD_RUN_URL,
                "path_translation": "APPEND_PATH_TO_ADDRESS"
            },
            "responses": {
                "204": {
                    "description": "No Content",
                    "headers": {
                        "Access-Control-Allow-Origin": {"type": "string"},
                        "Access-Control-Allow-Methods": {"type": "string"},
                        "Access-Control-Allow-Headers": {"type": "string"}
                    }
                }
            }
        }

    # GET ou autres méthodes
    if "GET" in r["methods"]:
        path_obj["get"] = {
            "summary": f"Route {r['path']}",
            "operationId": r["function"] + "Get",
            "x-google-backend": {
                "address": CLOUD_RUN_URL,
                "path_translation": "APPEND_PATH_TO_ADDRESS"
            },
            "responses": {
                "200": {
                    "description": "Message JSON",
                    "schema": {"type": "object", "properties": {"message": {"type": "string"}}}
                }
            },
            "x-google-extensions": {
                "cors": {
                    "allowOrigins": ["*"],
                    "allowMethods": ["GET", "OPTIONS"],
                    "allowHeaders": ["Content-Type"]
                }
            }
        }

    swagger["paths"][r["path"]] = path_obj

# Sauvegarde dans api.yaml
with open("api.yaml", "w") as f:
    yaml.safe_dump(swagger, f, sort_keys=False)

print("✅ api.yaml généré automatiquement à partir de main.py")
