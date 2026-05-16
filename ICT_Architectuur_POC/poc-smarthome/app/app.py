from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
HUB_URL = os.getenv("HUB_URL", "http://hub:5000")

@app.get("/")
def home():
    try:
        r = requests.get(f"{HUB_URL}/devices", timeout=3)
        data = r.json()
    except Exception as e:
        data = {"error": str(e)}
    return jsonify(data)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})
    
app.run(host="0.0.0.0", port=5001)
