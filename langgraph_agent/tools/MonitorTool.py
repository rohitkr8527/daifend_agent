from datetime import datetime, timedelta
from tools.tool_interface import ToolInterface

class MonitorTool(ToolInterface):
    """
    Monitors post-mitigation traffic for recurring anomalies or spikes.
    Triggers escalation if traffic doesn't stabilize.
    """

    def __init__(self, threshold_per_min=15):
        self.threshold = threshold_per_min  # Safe volume

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        now = datetime.utcnow()
        time_window = timedelta(minutes=1)
        ip_counts = {}

        # Count requests per IP in the last 1 minute
        for entry in logs:
            try:
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if now - ts <= time_window:
                    ip = entry.get("src_ip")
                    ip_counts[ip] = ip_counts.get(ip, 0) + 1
            except Exception:
                continue

        flagged = []
        for ip, count in ip_counts.items():
            if count > self.threshold:
                flagged.append({
                    "ip": ip,
                    "current_rate": count,
                    "status": "Unstable",
                    "action": f"Escalate monitoring - {count} req/min"
                })

        return {"MonitorTool": flagged}
