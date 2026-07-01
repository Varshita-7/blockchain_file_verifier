import json
import os
from datetime import datetime

LOG_FILE = "action_logs.json"

def log_action(username, action):

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    logs.append({
        "user": username,
        "action": action,
        "time": str(datetime.now())
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)