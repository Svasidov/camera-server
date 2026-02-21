from flask import Flask, request, jsonify
import base64, os, time

app = Flask(__name__)
os.makedirs("photos", exist_ok=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://svasidov.github.io"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/upload", methods=["POST", "OPTIONS"])
def upload():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.json["image"]
    img = base64.b64decode(data.split(",")[1])

    name = f"photos/{int(time.time())}.jpg"
    with open(name, "wb") as f:
        f.write(img)

    return jsonify({"status": "ok", "file": name})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
