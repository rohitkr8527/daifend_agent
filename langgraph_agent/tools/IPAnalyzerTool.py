from collections import defaultdict
from datetime import datetime, timedelta
from tools.tool_interface import ToolInterface

class IPAnalyzerTool(ToolInterface):
    """
    Identifies high-frequency IPs within a short time window.
    Useful for detecting DDoS or Brute Force attacks.
    """

    def __init__(self, threshold_per_min=15):
        self.threshold_per_min = threshold_per_min

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        now = datetime.utcnow()
        time_window = timedelta(minutes=1)
        ip_counts = defaultdict(int)

        # === Inline Feature Extraction: IP frequency in last 60 seconds ===
        for entry in logs:
            try:
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if now - ts <= time_window:
                    ip = entry["src_ip"]
                    ip_counts[ip] += 1
            except Exception:
                continue

        # === Scoring and Filtering ===
        flagged = []
        for ip, count in ip_counts.items():
            if count > self.threshold_per_min:
                flagged.append({
                    "ip": ip,
                    "request_count": count,
                    "reason": f"High request rate: {count}/min"
                })

        return {"IPAnalyzerTool": flagged}
