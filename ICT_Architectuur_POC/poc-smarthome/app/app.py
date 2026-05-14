import requests
import time

for i in range(3):
    r = requests.get("http://hub:5000/devices")
    print(f"Poll {i+1}:", r.json())
    time.sleep(2)

command = {
    "device": "lamp",
    "action": "on"
}

r = requests.post("http://hub:5000/command", json=command)
print("POST response:", r.json())
