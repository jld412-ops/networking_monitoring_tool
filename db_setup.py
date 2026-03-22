import sqlite3
conn = sqlite3.connect("network_logs.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    device TEXT,
    latency REAL,
    status TEXT
)
""")


conn.commit()
conn.close()

print("Network Database and Table Created Successfully")
