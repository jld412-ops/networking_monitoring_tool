import sqlite3
import subprocess
from datetime import datetime
import re
import time   # <-- NEW

devices = ["8.8.8.8", "1.1.1.1"]

def ping_device(device):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", device],  
            capture_output=True,
            text=True
        )

        output = result.stdout

        if "TTL=" in output or "ttl=" in output:
            match = re.search(r"time[=<]\s*(\d+)\s*ms", output, re.IGNORECASE)
            latency = float(match.group(1)) if match else None
            return latency, "UP"
        else:
            return None, "DOWN"

    except Exception as e:
        print(f"Error pinging {device}: {e}")
        return None, "DOWN"

def log_result(timestamp, device, latency, status):
    conn = sqlite3.connect("network_logs.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (timestamp, device, latency, status)
        VALUES (?, ?, ?, ?)
    """, (timestamp, device, latency, status))

    conn.commit()
    conn.close()

while True:
    for device in devices:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latency, status = ping_device(device)
        log_result(timestamp, device, latency, status)
        print(f"{timestamp} | {device} | {latency} ms | {status}")

    print("wait 10 seconds... until next check\n")
    time.sleep(10) 