from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)

devices = ["lamp", "thermostaat"]
last_command = {"status": "geen commando", "time": None}

@app.get("/")
def home():
    return render_template("index.html", devices=devices, last_command=last_command, status="online")

@app.get("/devices")
def get_devices():
    return jsonify({"devices": devices, "status": "online", "last_command": last_command})

@app.post("/command")
def command():
    data = request.get_json(force=True)
    global last_command
    last_command = {
        "status": "ontvangen",
        "data": data,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify({"status": "ok", "received": data, "time": last_command["time"]})

app.run(host="0.0.0.0", port=5000)
