from flask import Flask, request, jsonify, send_from_directory, abort
import base64, os, time

app = Flask(__name__)
os.makedirs("photos", exist_ok=True)

ALLOWED_ORIGINS = {"https://svasidov.github.io"}
ADMIN_KEY = os.environ.get("ADMIN_KEY", "12345")  # поменяешь в Render

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

    # Пользователю НЕ даём ссылку
    return jsonify({"status": "ok"})

@app.route("/admin", methods=["GET"])
def admin():
    key = request.args.get("key", "")
    if key != ADMIN_KEY:
        abort(403)

    files = sorted(
        (f for f in os.listdir("photos") if f.lower().endswith(".jpg")),
        reverse=True
    )

    base = request.host_url.rstrip("/")
    items = "\n".join(
        f'<li><a target="_blank" rel="noopener" href="{base}/photos/{f}">{f}</a></li>'
        for f in files
    ) or "<li>Пока нет фото</li>"

    return f"""
    <!doctype html>
    <html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Admin</title></head>
    <body style="font-family:system-ui;background:#0b0f14;color:#e8eef6;padding:16px">
      <h2>📸 Фото ({len(files)})</h2>
      <p>Открывай файлы по ссылкам ниже.</p>
      <ol>{items}</ol>
    </body></html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
