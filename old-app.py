from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

# Azure Blob Storage setup
#CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=case7dfe4yx;AccountKey=n0sxzNZCzr7Clx5EHqDQV6tP6P5RCxyEeRu0mAD+2PGOMLWnh9gJtzyJh/T29j4CIxs219465ZAC+ASt2ZPv4Q==;EndpointSuffix=core.windows.net"
#CONTAINER_NAME = "lanternfly-images"
CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
CONTAINER_NAME = os.environ.get("IMAGES_CONTAINER", "images-demo")

bsc = BlobServiceClient.from_connection_string(CONNECTION_STRING)
cc = bsc.get_container_client(CONTAINER_NAME)

# Flask app setup
app = Flask(__name__)

@app.post("/api/v1/upload")
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    f = request.files["file"]
    
    # Upload file to blob storage
    blob_client = cc.get_blob_client(f.filename)
    blob_client.upload_blob(f, overwrite=True)

    return jsonify(ok=True, url=f"{cc.url}/{f.filename}")

@app.get("/api/v1/health")
def health():
    return jsonify(status="ok")

@app.get("/api/v1/gallery")
def gallery():
    blobs = cc.list_blobs()
    urls = [f"{cc.url}/{blob.name}" for blob in blobs]
    return jsonify(ok=True, gallery=urls)

@app.get("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


