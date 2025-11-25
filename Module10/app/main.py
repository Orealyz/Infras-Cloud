import os
from flask import Flask, request, jsonify

app = Flask(__name__)

APP_MESSAGE = os.getenv("APP_MESSAGE")
UPLOAD_EXT = os.getenv("UPLOAD_ALLOWED_EXT")
UPLOAD_PASSWORD = os.getenv("UPLOAD_PASSWORD")
DATA_FOLDER = "/data"


@app.route("/", methods=["GET"])
def list_files():
    files = os.listdir(DATA_FOLDER)
    return jsonify({"message": APP_MESSAGE, "files": files})


@app.route("/upload", methods=["POST"])
def upload_file():
    password = request.form.get("password")
    file = request.files.get("file")

    if password != UPLOAD_PASSWORD:
        return "Wrong password", 403

    if not file.filename.endswith(UPLOAD_EXT):
        return "Extension not allowed", 400

    file.save(os.path.join(DATA_FOLDER, file.filename))
    return "OK", 200


if __name__ == "__main__":
    os.makedirs(DATA_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=8000)
