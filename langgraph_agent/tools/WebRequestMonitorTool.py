from typing import List, Dict
import re
import datetime

class WebRequestMonitorTool:
    """
    Simulates a web request monitor that scans incoming HTTP requests
    for signs of SQL injection or CSRF attacks.
    """

    def __init__(self):
        self.sqli_patterns = [r"(?i)(\bunion\b|\bselect\b|\binsert\b|\bdrop\b|\bdelete\b|' ?or ?'1' ?= ?'1)"]
        self.csrf_token_pattern = r"csrf_token=[^&]*"

    def run(self, context: Dict) -> Dict:
        logs = context.get("logs", [])
        flagged = []

        for entry in logs:
            request = entry.get("payload", "")
            flagged_entry = {"timestamp": str(datetime.datetime.now()), "ip": entry.get("ip"), "payload": request}

            if any(re.search(p, request) for p in self.sqli_patterns):
                flagged_entry["type"] = "SQLi"
                flagged.append(flagged_entry)
            elif "csrf_token" in request and not re.search(self.csrf_token_pattern, request):
                flagged_entry["type"] = "CSRF"
                flagged.append(flagged_entry)

        return {
            "WebRequestMonitorTool": flagged,
            "meta": {"flagged_count": len(flagged)}
        }