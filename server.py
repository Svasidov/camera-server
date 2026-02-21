from flask import Flask, request
import base64, os, time

app = Flask(__name__)
os.makedirs("photos", exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json["image"]
    img = base64.b64decode(data.split(",")[1])
    name = f"photos/{int(time.time())}.jpg"
    with open(name, "wb") as f:
        f.write(img)
    return "OK"

app.run(host="0.0.0.0", port=10000)
