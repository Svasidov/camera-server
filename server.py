from flask import Flask, request, jsonify
import base64, os, time

app = Flask(__name__)
os.makedirs("photos", exist_ok=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS, GET"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/ping", methods=["GET"])
def ping():
    return "OK"

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

    img = base64.b64decode(img_b64)
    name = f"photos/{int(time.time())}.jpg"
    with open(name, "wb") as f:
        f.write(img)

    return jsonify({"status": "ok", "file": name})
