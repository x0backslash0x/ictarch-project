import socket
import json
import time

PROBE_PORT    = 5000
PROBE_TIMEOUT = 3

DEVICE_HOSTS = [
    'device_lamp',
    'device_sensor',
    'device_lock',
    'device_thermostat',
    'device_speaker'
]

def probe_scan():
    results = {}

    print("\n[HUB] ════════════════════════════════════════")
    print("[HUB]   PROBE SCAN GESTART")
    print(f"[HUB]   {len(DEVICE_HOSTS)} apparaten te scannen")
    print("[HUB] ════════════════════════════════════════\n")

    for host in DEVICE_HOSTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(PROBE_TIMEOUT)

            message = json.dumps({'type': 'DISCOVER'}).encode()
            sock.sendto(message, (host, PROBE_PORT))
            print(f"[HUB] → Probe verstuurd naar {host}...")

            try:
                data, addr = sock.recvfrom(1024)
                device = json.loads(data.decode())
                print(f"[HUB] ✓ Gevonden: {device['name']} | {device['type']} | {device['mac']}")
                results[device['mac']] = {**device, 'ip': addr[0]}
            except socket.timeout:
                print(f"[HUB] ✗ Geen antwoord van {host} — niet aanwezig op netwerk")

            sock.close()

        except Exception as e:
            print(f"[HUB] ✗ {host} niet bereikbaar: {e}")

    print(f"\n[HUB] ════════════════════════════════════════")
    print(f"[HUB]   GEVONDEN APPARATEN ({len(results)} totaal)")
    print(f"[HUB] ════════════════════════════════════════")

    if not results:
        print("[HUB] Geen apparaten gevonden.")
    else:
        print(f"\n  {'Naam':<25} {'Type':<15} {'MAC':<22} {'IP'}")
        print("  " + "─" * 75)
        for mac, device in results.items():
            print(f"  {device['name']:<25} {device['type']:<15} {mac:<22} {device['ip']}")

    print()

if __name__ == '__main__':
    probe_scan()
