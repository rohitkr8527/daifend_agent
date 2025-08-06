from collections import defaultdict
from datetime import datetime, timedelta, timezone
from tools.tool_interface import ToolInterface


class RateLimiterTool(ToolInterface):
    """
    Identifies and simulates throttling of IPs with high request or login failure rates.
    Can handle both DDoS and Brute Force use cases based on context['limit_type'].
    """

    def __init__(self, ddos_threshold: int = 10, brute_threshold: int = 5, decay_factor: float = 0.2):
        self.ddos_threshold = ddos_threshold
        self.brute_threshold = brute_threshold
        self.decay_factor = decay_factor
        self.time_window = timedelta(minutes=1)
        self.throttled_ips = {}

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        limit_type = context.get("limit_type", "ddos").lower()
        now = datetime.now(timezone.utc)

        ip_hits = defaultdict(int)
        for entry in logs:
            try:
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if now - ts > self.time_window:
                    continue

                ip = entry.get("src_ip")
                if not ip:
                    continue

                # Brute force mode: count failed logins
                if limit_type == "brute_force":
                    if entry.get("event_type") == "login_failure":
                        ip_hits[ip] += 1

                # DDoS mode: count all requests
                else:
                    ip_hits[ip] += 1

            except Exception:
                continue

        recommendations = []
        for ip, count in ip_hits.items():
            threshold = self.brute_threshold if limit_type == "brute_force" else self.ddos_threshold
            if count >= threshold:
                limit = round(count * self.decay_factor, 2)
                self._simulate_throttle(ip, limit, limit_type)
                recommendations.append({
                    "ip": ip,
                    "observed_count": count,
                    "recommended_limit": limit,
                    "limit_type": limit_type,
                    "throttle_status": self.throttled_ips[ip]
                })

        return {
            "RateLimiterTool": recommendations,
            "meta": {
                "flagged_count": len(recommendations),
                "decay_factor": self.decay_factor,
                "threshold": self.brute_threshold if limit_type == "brute_force" else self.ddos_threshold,
                "mode": limit_type
            }
        }

    def _simulate_throttle(self, ip: str, limit: float, limit_type: str):
        """
        Simulates throttling logic.
        """
        if limit_type == "brute_force":
            self.throttled_ips[ip] = f"Simulated: Throttle login attempts to {limit} tries/min"
        else:
            self.throttled_ips[ip] = f"Simulated: Throttle requests to {limit} req/min"
