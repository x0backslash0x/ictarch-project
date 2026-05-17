# app/app.py
import os
import time
import requests

HUB_URL = os.environ.get("HUB_URL", "http://localhost:5000")

def main():
    print("Simpele client die de hub status controleert.")
    while True:
        try:
            r = requests.get(f"{HUB_URL}/status", timeout=5)
            print("Hub status:", r.json())
        except Exception as e:
            print("Kan hub niet bereiken:", e)
        time.sleep(30)

if __name__ == "__main__":
    main()