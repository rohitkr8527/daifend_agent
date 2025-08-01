# Placeholder for tools/LoginAttemptMonitorTool.py
from collections import defaultdict
from tools.tool_interface import ToolInterface

class LoginAttemptMonitorTool(ToolInterface):
    """
    Flags IPs with excessive failed login attempts (Brute Force indicator).
    """

    def __init__(self, threshold=5):
        self.threshold = threshold

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        failed_logins = defaultdict(int)
        flagged_ips = []

        for entry in logs:
            if "Brute Force" in entry.get("alert_message", "") and entry.get("alert", False):
                ip = entry.get("src_ip")
                failed_logins[ip] += 1
                if failed_logins[ip] == self.threshold:
                    flagged_ips.append({
                        "ip": ip,
                        "reason": f"{self.threshold} failed logins detected"
                    })

        return {"LoginAttemptMonitorTool": flagged_ips}

