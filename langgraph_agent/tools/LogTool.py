# tools/LogTool.py

import json
from datetime import datetime

class LogTool:
    def run(self, data: dict) -> dict:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": data
        }

        # For now, print log to console (can be extended to write to file or SIEM system)
        print("[LogTool] Logged Event:")
        print(json.dumps(log_entry, indent=4))

        return {"status": "logged", "log": log_entry}
