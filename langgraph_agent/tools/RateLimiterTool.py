from collections import defaultdict
from datetime import datetime, timedelta, timezone
from tools.tool_interface import ToolInterface

class RateLimiterTool(ToolInterface):
    """
    Recommends throttling IPs with high request rates.
    Applies a decay factor to dynamically suggest limits.
    """

    def __init__(self, decay_factor: float = 0.2, threshold: int = 10):
        self.decay_factor = decay_factor
        self.threshold = threshold  # Minimum count to consider for throttling
        self.time_window = timedelta(minutes=1)

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        now = datetime.now(timezone.utc)
        ip_hits = defaultdict(int)

        for entry in logs:
            try:
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if now - ts <= self.time_window:
                    ip_hits[entry["src_ip"]] += 1
            except Exception:
                continue

        recommendations = []
        for ip, count in ip_hits.items():
            if count >= self.threshold:
                limit = round(count * self.decay_factor, 2)
                recommendations.append({
                    "ip": ip,
                    "observed_rate": count,
                    "recommended_limit": limit,
                    "action": f"Throttle {ip} to {limit} req/min"
                })

        return {
            "RateLimiterTool": recommendations,
            "meta": {
                "flagged_count": len(recommendations),
                "decay_factor": self.decay_factor,
                "threshold": self.threshold
            }
        }
