import socket
import json
import os

# ─────────────────────────────────────────────
# Simuleert een slim apparaat dat reageert op probe.
# Start automatisch en luistert continu.
# ─────────────────────────────────────────────

DEVICE_NAME = os.environ.get('DEVICE_NAME', 'Onbekend Apparaat')
DEVICE_MAC  = os.environ.get('DEVICE_MAC',  'AA:BB:CC:00:00:00')
DEVICE_TYPE = os.environ.get('DEVICE_TYPE', 'onbekend')
PROBE_PORT  = 5000

print(f"[{DEVICE_NAME}] Gestart")
print(f"[{DEVICE_NAME}] Type: {DEVICE_TYPE} | MAC: {DEVICE_MAC}")
print(f"[{DEVICE_NAME}] Luistert op poort {PROBE_PORT} voor probe requests...")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', PROBE_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    try:
        msg = json.loads(data.decode())
        if msg.get('type') == 'DISCOVER':
            print(f"[{DEVICE_NAME}] Probe ontvangen van {addr[0]} — stuur antwoord")
            response = json.dumps({
                'name': DEVICE_NAME,
                'mac':  DEVICE_MAC,
                'type': DEVICE_TYPE
            })
            sock.sendto(response.encode(), addr)
    except json.JSONDecodeError:
        pass
