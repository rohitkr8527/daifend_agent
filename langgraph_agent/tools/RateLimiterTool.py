# Placeholder for tools/RateLimiterTool.py
from collections import defaultdict
from datetime import datetime, timedelta
from tools.tool_interface import ToolInterface

class RateLimiterTool(ToolInterface):
    """
    Recommends per-IP throttling based on observed request rate.
    Uses a fixed decay factor to suggest adaptive rate limits.
    """

    def __init__(self, decay_factor=0.2):
        self.decay_factor = decay_factor  # Throttle to 20% of observed rate

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        now = datetime.now(datetime.timezone.utc)
        time_window = timedelta(minutes=1)
        ip_hits = defaultdict(int)

        # === Extract request counts per IP in the last 60 seconds ===
        for entry in logs:
            try:
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if now - ts <= time_window:
                    ip = entry["src_ip"]
                    ip_hits[ip] += 1
            except Exception:
                continue

        # === Generate adaptive throttling recommendations ===
        recommendations = []
        for ip, count in ip_hits.items():
            if count >= 10:  # Only throttle high-volume IPs
                limit = round(count * self.decay_factor, 2)
                recommendations.append({
                    "ip": ip,
                    "observed_rate": count,
                    "recommended_limit": limit,
                    "action": f"Throttle to {limit} req/sec"
                })

        return {"RateLimiterTool": recommendations}
