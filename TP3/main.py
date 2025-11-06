from flask import Flask, jsonify
from google.cloud import storage
import os

app = Flask(__name__)

# Nom du bucket depuis la variable d'environnement
BUCKET_NAME = os.environ.get("BUCKET_NAME")

@app.route("/list", methods=["GET"])
def list_objects():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()
    files = [blob.name for blob in blobs]
    return jsonify(files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
