from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route("/hello", methods=["GET", "OPTIONS"])
def hello():
    if request.method == "OPTIONS":
        # Réponse pour les requêtes préflight CORS
        response = make_response("", 204)
    else:
        # Réponse GET normale
        response = make_response(jsonify({"message": "Hello from Cloud Run!"}))
    
    # Headers CORS nécessaires
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# --- Nouvelle route de test ---
@app.route("/test", methods=["GET", "OPTIONS"])
def test_route():
    if request.method == "OPTIONS":
        response = make_response("", 204)
    else:
        response = make_response(jsonify({"message": "Test route working!"}))
    
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response
@app.route('/test2', methods=['GET'])
def test():
    return jsonify({"message": "Test OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
