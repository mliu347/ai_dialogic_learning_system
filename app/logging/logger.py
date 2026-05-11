import json
import os
from datetime import datetime

LOG_FILE = "logs/dialogue_log.jsonl"


def log_interaction(data: dict):
    os.makedirs("logs", exist_ok=True)

    data["timestamp"] = str(datetime.now())

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")