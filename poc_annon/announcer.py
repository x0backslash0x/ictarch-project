#announcer.py
# stuurt periodiek announcements
import socket
import json
import time

TARTGET_IP = "127.0.0.1"
TARGET_PORT = 4002
INTERVAL_SECONDS = 3

device = [
    {
        "device_id": "device-light-001",
        "friendly_name": "Simulated Smart Lamp",
        "device_type": "light",
        "ip": "192.168.1.50",
        "port": 12345,
        "protocol": "demo-announcement"
    },
]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

print("Starting announcement sender...")

while True:
    payload = json.dumps(device).encode("utf-8")
    #sock.sendto(payload, (MULTICAST_GROUP, PORT))
    sock.sendto(payload, (TARTGET_IP, TARGET_PORT))
    print(f"Announcement sent: {device['friendly_name']}")
    time.sleep(INTERVAL_SECONDS)
