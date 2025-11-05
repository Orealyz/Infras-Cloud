import ast
import yaml

# Nom du service Cloud Run
CLOUD_RUN_URL = "https://flask-api-513126423995.europe-west9.run.app"

# Lecture de main.py
with open("main.py") as f:
    tree = ast.parse(f.read())

routes = []

# Parcours AST pour récupérer toutes les routes Flask
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        for deco in node.decorator_list:
            if isinstance(deco, ast.Call) and getattr(deco.func, "attr", "") == "route":
                # Compatible Python 3.12+
                path = deco.args[0].value  # Chemin de la route
                methods = [kw.value.elts[0].value for kw in deco.keywords if kw.arg == "methods"] if deco.keywords else ["GET"]
                routes.append({
                    "path": path,
                    "methods": methods,
                    "function": node.name
                })

# Génération Swagger
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

    # GET ou autre méthode
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

# Sauvegarde
with open("api.yaml", "w") as f:
    yaml.safe_dump(swagger, f, sort_keys=False)

print("✅ api.yaml généré automatiquement à partir de main.py")
