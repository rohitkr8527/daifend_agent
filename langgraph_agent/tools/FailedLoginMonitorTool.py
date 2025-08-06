from typing import Dict, List
from collections import defaultdict
from datetime import datetime, timedelta, timezone


class FailedLoginMonitorTool:
    """
    Detects IPs with excessive failed login attempts within a given time window.
    This is useful for identifying brute-force attack patterns.
    """

    def __init__(self, threshold: int = 5, window_minutes: int = 10):
        """
        :param threshold: Number of failed attempts from an IP to consider it suspicious.
        :param window_minutes: Time window to consider failed attempts.
        """
        self.threshold = threshold
        self.time_window = timedelta(minutes=window_minutes)

    def run(self, context: Dict) -> Dict:
        logs: List[Dict] = context.get("logs", [])
        now = datetime.now(timezone.utc)

        ip_failures = defaultdict(int)

        for entry in logs:
            if entry.get("event_type") != "login_attempt" or entry.get("status") != "failed":
                continue

            try:
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if now - ts <= self.time_window:
                    ip = entry.get("src_ip")
                    if ip:
                        ip_failures[ip] += 1
            except Exception:
                continue  # Skip malformed timestamps

        flagged = [
            {"ip": ip, "failed_attempts": count}
            for ip, count in ip_failures.items()
            if count >= self.threshold
        ]

        return {
            "FailedLoginMonitorTool": flagged,
            "meta": {
                "flagged_count": len(flagged),
                "threshold": self.threshold,
                "window_minutes": self.time_window.total_seconds() / 60
            }
        }
