from typing import List, Dict
import re
import datetime

class WAFMonitorTool:
    """
    Simulates a Web Application Firewall (WAF) that enforces simple security policies
    like blocking known SQL keywords or missing CSRF tokens.
    """

    def __init__(self):
        self.block_keywords = ["select", "drop", "union", "insert", "--"]
        self.csrf_required_paths = ["/submit", "/update"]

    def run(self, context: Dict) -> Dict:
        logs = context.get("logs", [])
        rejected = []

        for entry in logs:
            ip = entry.get("ip")
            path = entry.get("path", "")
            payload = entry.get("payload", "")
            rejection_reason = None

            if any(kw in payload.lower() for kw in self.block_keywords):
                rejection_reason = "Contains SQL keyword"
            elif path in self.csrf_required_paths and "csrf_token=" not in payload:
                rejection_reason = "Missing CSRF token"

            if rejection_reason:
                rejected.append({
                    "timestamp": str(datetime.datetime.now()),
                    "ip": ip,
                    "path": path,
                    "reason": rejection_reason
                })

        return {
            "WAFMonitorTool": rejected,
            "meta": {"rejected_count": len(rejected)}
        }