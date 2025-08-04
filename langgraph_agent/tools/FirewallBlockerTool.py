import subprocess
import platform
from tools.tool_interface import ToolInterface

class FirewallBlockerTool(ToolInterface):
    """
    Blocks high-risk IPs at the OS-level firewall, skipping those already throttled.
    """

    def __init__(self):
        self.system = platform.system()

    def block_ip(self, ip):
        try:
            if self.system == "Windows":
                # Block inbound traffic from IP
                cmd = ["netsh", "advfirewall", "firewall", "add", "rule",
                       "name=Block_IP_" + ip,
                       "dir=in", "action=block", f"remoteip={ip}"]
            elif self.system == "Linux":
                # Block with iptables (requires sudo)
                cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
            else:
                return False, f"Unsupported OS: {self.system}"

            subprocess.run(cmd, check=True)
            return True, f"Blocked IP {ip} on {self.system}"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to block IP {ip}: {e}"

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        throttled_ips = set()
        rate_limit_data = context.get("RateLimiterTool", [])
        for rec in rate_limit_data:
            throttled_ips.add(rec["ip"])

        suspicious_ips = context.get("IPAnalyzerTool", {}).get("suspicious_ips", [])
        blocked = []

        for ip in suspicious_ips:
            if ip in throttled_ips:
                continue  # Skip IPs already handled by rate limiting

            success, message = self.block_ip(ip)
            blocked.append({
                "ip": ip,
                "action": "Blocked via firewall",
                "status": "Success" if success else "Failed",
                "message": message
            })

        return {"FirewallBlockerTool": blocked}
