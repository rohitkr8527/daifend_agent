from collections import defaultdict
from datetime import datetime, timedelta, timezone
from tools.tool_interface import ToolInterface


class IPAnalyzerTool(ToolInterface):
    """
    Analyzes incoming log data to detect IPs exhibiting high request frequency
    within a defined time window.
    """

    def __init__(self, threshold_per_minute=10, time_window_minutes=1, time_field="timestamp", ip_field="src_ip"):
        """
        :param threshold_per_minute: Request threshold per IP per time window.
        :param time_window_minutes: Time window in minutes for sliding analysis.
        :param time_field: Field in log representing ISO 8601 timestamp.
        :param ip_field: Field in log representing source IP address.
        """
        self.threshold = threshold_per_minute
        self.window = timedelta(minutes=time_window_minutes)
        self.time_field = time_field
        self.ip_field = ip_field

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        now = datetime.now(timezone.utc)
        ip_activity = defaultdict(list)

        for entry in logs:
            try:
                timestamp = self._parse_timestamp(entry.get(self.time_field))
                if not timestamp or (now - timestamp > self.window):
                    continue

                ip = entry.get(self.ip_field)
                if ip:
                    ip_activity[ip].append(timestamp)
            except Exception:
                continue

        flagged_ips = []
        for ip, times in ip_activity.items():
            if len(times) > self.threshold:
                flagged_ips.append({
                    "ip": ip,
                    "request_count": len(times),
                    "window_minutes": self.window.total_seconds() / 60,
                    "reason": f"Exceeded threshold ({len(times)}/{self.threshold} req/min)"
                })

        return {
            "IPAnalyzerTool": flagged_ips,
            "meta": {
                "threshold_per_minute": self.threshold,
                "window_minutes": self.window.total_seconds() / 60,
                "total_unique_ips": len(ip_activity),
                "flagged_count": len(flagged_ips)
            }
        }

    @staticmethod
    def _parse_timestamp(ts: str) -> datetime | None:
        try:
            if ts.endswith("Z"):
                ts = ts.replace("Z", "+00:00")
            return datetime.fromisoformat(ts)
        except Exception:
            return None
