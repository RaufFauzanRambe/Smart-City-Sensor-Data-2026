import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# =========================
# CONFIG
# =========================
START_TIME = datetime(2026, 1, 1, 0, 0, 0)
END_TIME = datetime(2026, 1, 2, 0, 0, 0)  # 🔥 NEW (1 day range)

OUTPUT_PATH = "data/raw/smart_city_raw.csv"

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# =========================
# SENSOR CONFIG
# =========================
locations = ["Zone_A", "Zone_B", "Zone_C", "Zone_D"]
statuses = ["OK", "OK", "OK", "ERROR"]

# =========================
# GENERATE DATA
# =========================
current_time = START_TIME
data = []

while current_time <= END_TIME:

    row = {
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "device_id": f"SENSOR_{random.randint(1, 10):03d}",
        "location": random.choice(locations),
        "traffic_count": random.randint(50, 200),
        "pm25": round(random.uniform(10, 80), 2),
        "temperature": round(random.uniform(25, 35), 2),
        "humidity": random.randint(60, 90),
        "energy_usage": random.randint(400, 800),
        "noise_level": random.randint(50, 90),
        "status": random.choice(statuses)
    }

    # =========================
    # REALISTIC IMPERFECTIONS
    # =========================
    if random.random() < 0.1:
        row["traffic_count"] = np.nan

    if random.random() < 0.1:
        row["pm25"] = np.nan

    if random.random() < 0.05:
        row["temperature"] = np.nan

    if random.random() < 0.05:
        row["status"] = "ERROR"

    data.append(row)

    # =========================
    # TIME STEP (irregular intervals)
    # =========================
    current_time += timedelta(seconds=random.randint(30, 120))

# =========================
# SAVE CSV
# =========================
df = pd.DataFrame(data)
df.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Dataset generated from {START_TIME} to {END_TIME}")
print(f"📁 Saved at: {OUTPUT_PATH}")
print(df.head())