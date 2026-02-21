from flask import Flask, request, jsonify, send_from_directory
import base64, os, time

app = Flask(__name__)
os.makedirs("photos", exist_ok=True)

ALLOWED_ORIGINS = {
    "https://svasidov.github.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
}

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Vary"] = "Origin"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS, GET"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/ping", methods=["GET"])
def ping():
    return "OK"

@app.route("/photos/<filename>", methods=["GET"])
def get_photo(filename):
    return send_from_directory("photos", filename)

@app.route("/upload", methods=["POST", "OPTIONS"])
def upload():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    img_b64 = data.get("image", "")

    if "," in img_b64:
        img_b64 = img_b64.split(",", 1)[1]

    if not img_b64:
        return jsonify({"status": "error", "msg": "no image"}), 400

    try:
        img = base64.b64decode(img_b64)
    except Exception:
        return jsonify({"status": "error", "msg": "bad base64"}), 400

    filename = f"{int(time.time())}.jpg"
    path = os.path.join("photos", filename)

    with open(path, "wb") as f:
        f.write(img)

    # Полная ссылка на фото
    base = request.host_url.rstrip("/")
    photo_url = f"{base}/photos/{filename}"

    return jsonify({"status": "ok", "photo_url": photo_url})
