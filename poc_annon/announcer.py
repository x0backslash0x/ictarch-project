#announcer.py
# stuurt periodiek announcements
import socket
import json
import time
import sys

# defaults #
INTERVAL_SECONDS = 3
TARTGET_IP = "127.0.0.1"
TARGET_PORT = 4002

if sys.argv[1] == "-h":
    print("argumenten: <host> <port> <interval>")
    sys.exit()
if len(sys.argv) == 4:
    TARTGET_IP = sys.argv[1]
    TARGET_PORT = int(sys.argv[2])
    INTERVAL_SECONDS = int(sys.argv[3])


devices = [
    {
        "device_id": "device-light-001",
        "friendly_name": "Simulated Smart Lamp",
        "device_type": "light",
        "ip": "192.168.1.50",
        "port": 12345,
    },
    {
        "device_id": "device-thermostat-001",
        "friendly_name": "Simulated Thermostat",
        "device_type": "thermostat",
        "ip": "192.168.1.51",
        "port": 12346,
    },
    {
        "device_id": "device-speaker-001",
        "friendly_name": "Simulated Speaker",
        "device_type": "speaker",
        "ip": "192.168.1.52",
        "port": 12347,
    }
]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

print(f"Sending announcements to {TARTGET_IP}:{TARGET_PORT} at {INTERVAL_SECONDS} second intervals ...")

device_index = 0
announcement_id = 1

while True:
    device = devices[device_index]
    announcement = {
        "announcement_id": announcement_id,
        "device": {
            **device
        }
    }
    payload = json.dumps(announcement).encode("utf-8")
    sock.sendto(payload, (TARTGET_IP, TARGET_PORT))
    print(f"Announcement [{announcement['announcement_id']}] sent: {device['friendly_name']}")
    device_index = (device_index + 1) % len(devices)
    time.sleep(INTERVAL_SECONDS)
    announcement_id += 1
