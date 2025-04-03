from flask import Flask, request
import requests
import os

app = Flask(__name__)

# === Настройки ===
VERIFY_TOKEN = "nn88nn"
FORWARD_URL = os.getenv("FORWARD_URL")  # адрес твоего n8n вебхука

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    mode = request.args.get("hub.mode")

    if token == VERIFY_TOKEN and mode == "subscribe":
        return challenge, 200, {"Content-Type": "text/plain"}
    return "Unauthorized", 403

@app.route("/webhook", methods=["POST"])
def forward():
    try:
        resp = requests.post(FORWARD_URL, json=request.json, timeout=10)
        return "OK", resp.status_code
    except Exception as e:
        print("Ошибка при пересылке:", str(e))
        return "Internal Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
