from typing import Dict, List


class IPBlacklistTool:
    """
    Simulates blacklisting of IPs identified as sources of brute-force attacks.
    Consumes output from tools like FailedLoginMonitorTool.
    """

    def run(self, context: Dict) -> Dict:
        failed_login_data: List[Dict] = context.get("FailedLoginMonitorTool", [])
        blacklisted_ips = []

        for entry in failed_login_data:
            ip = entry.get("ip")
            if ip:
                blacklisted_ips.append({
                    "ip": ip,
                    "status": "Blacklisted due to excessive failed login attempts"
                })

        return {
            "IPBlacklistTool": blacklisted_ips,
            "meta": {
                "blacklisted_count": len(blacklisted_ips)
            }
        }
