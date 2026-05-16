#device-listener.py
# Luistert naar apparaat announcements
import socket
import json
import time
import sys

# defaults #
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 4002
TIMEOUT = 10

if sys.argv[1] == "-h":
    print("argumenten: <host> <port> <timeout>")
    sys.exit()
if len(sys.argv) == 4:
    LISTEN_HOST = sys.argv[1]
    LISTEN_PORT = int(sys.argv[2])
    TIMEOUT = float(sys.argv[3])

def format_timestamp(epoch_seconds):
    local_time = time.localtime(epoch_seconds)
    return time.strftime("%M:%S", local_time)

class AnnouncementDiscovery:
    def __init__(self, timeout_seconds=TIMEOUT):
        self.timeout_seconds = timeout_seconds
        self.devices = {}

    def handle_announcement(self, data, addr):
        try:
            payload = json.loads(data.decode("utf-8"))
        except Exception:
            return

        stable_id = payload.get("device_id")
        if not stable_id:
            return

        now = time.time()
        existing = self.devices.get(stable_id)

        if existing:
            existing["last_seen"] = now
            existing["announcement_count"] += 1
            return

        self.devices[stable_id] = {
            "stable_id": stable_id,
            "friendly_name": payload.get("friendly_name"),
            "device_type": payload.get("device_type"),
            "ip": payload.get("ip") or addr[0],
            "port": payload.get("port"),
            "protocol": payload.get("protocol", "demo-announcement"),
            "first_seen": format_timestamp(now),
            "last_seen": now,
            "announcement_count": 1,
        }

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((LISTEN_HOST, LISTEN_PORT))
        sock.settimeout(0.5)

        start = time.time()
        print(f"[{format_timestamp(time.time())}] Listening for announcements on {LISTEN_HOST}:{LISTEN_PORT} for {self.timeout_seconds} seconds...")

        while time.time() - start < self.timeout_seconds:
            try:
                data, addr = sock.recvfrom(4096)
                self.handle_announcement(data, addr)
            except socket.timeout:
                continue

        sock.close()
        return list(self.devices.values())


if __name__ == "__main__":
    discovery = AnnouncementDiscovery(timeout_seconds=TIMEOUT)
    devices = discovery.run()

    print("\nDiscovered devices:")
    for device in devices:
        print(
            f"[{device['first_seen']}] {device['friendly_name']} "
            f"({device['ip']}:{device['port']}) "
            f"[announcements: {device['announcement_count']}]"
        )

    print(f"\n[{format_timestamp(time.time())}] No longer listening for announcements")
    while True:
        time.sleep(3600)

