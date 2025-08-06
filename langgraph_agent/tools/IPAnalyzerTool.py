from collections import defaultdict
from tools.tool_interface import ToolInterface


class IPAnalyzerTool(ToolInterface):
    """
    Identifies IPs that may be involved in DDoS attacks by analyzing connection behavior.
    Flags IPs with:
    - High number of connections
    - Suspicious connection states
    - Low average connection duration
    - Low average payload size
    """

    def __init__(
        self,
        min_connection_count: int = 3,
        max_avg_duration: float = 2.0,
        max_avg_payload: int = 300,
        suspicious_conn_states: list = None
    ):
        self.min_connection_count = min_connection_count
        self.max_avg_duration = max_avg_duration
        self.max_avg_payload = max_avg_payload
        self.suspicious_conn_states = suspicious_conn_states or ["S0", "S1", "REJ"]

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        ip_stats = defaultdict(lambda: {"count": 0, "duration_sum": 0.0, "payload_sum": 0, "conn_state_match": 0})

        for entry in logs:
            ip = entry.get("src_ip")
            conn_state = entry.get("conn_state", "")
            duration = float(entry.get("duration", 0.0))
            payload = int(entry.get("payload_bytes", 0))

            ip_stats[ip]["count"] += 1
            ip_stats[ip]["duration_sum"] += duration
            ip_stats[ip]["payload_sum"] += payload

            if conn_state in self.suspicious_conn_states:
                ip_stats[ip]["conn_state_match"] += 1

        suspicious_ips = {}

        for ip, stats in ip_stats.items():
            count = stats["count"]
            avg_duration = stats["duration_sum"] / count
            avg_payload = stats["payload_sum"] / count
            conn_state_hits = stats["conn_state_match"]

            if (
                count >= self.min_connection_count
                and conn_state_hits > 0
                and avg_duration <= self.max_avg_duration
                and avg_payload <= self.max_avg_payload
            ):
                suspicious_ips[ip] = {
                    "ip": ip,
                    "connection_count": count,
                    "avg_payload": round(avg_payload, 2),
                    "avg_duration": round(avg_duration, 2)
                }

        return {
            "IPAnalyzerTool": list(suspicious_ips.values()),
            "meta": {
                "flagged_count": len(suspicious_ips)
            }
        }
