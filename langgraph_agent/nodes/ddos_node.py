# Placeholder for nodes/ddos_node.py
# nodes/ddos_node.py

from tools.IPAnalyzerTool import IPAnalyzerTool
from tools.RateLimiterTool import RateLimiterTool
from tools.FirewallBlockerTool import FirewallBlockerTool
from tools.MonitorTool import MonitorTool
from tools.LogTool import LogTool

def ddos_toolchain(state: dict) -> dict:
    data = state.get("data", {})

    print("[*] DDoS Toolchain Activated")

    # === Step 1: Identify Malicious IPs ===
    ip_result = IPAnalyzerTool().run(data)

    # === Step 2: Apply Rate Limits ===
    limiter_result = RateLimiterTool().run(data)

    # === Step 3: Firewall Blocking ===
    fw_result = FirewallBlockerTool().run({
        "block_ips": [entry["ip"] for entry in ip_result.get("flagged_ips", [])]
    })

    # === Step 4: Post-Mitigation Monitoring (mocked) ===
    monitor_result = MonitorTool().run(data)

    # === Step 5: Audit Logging ===
    log_result = LogTool().run({
        "attack": "ddos",
        "actions": {
            "ip_analysis": ip_result,
            "rate_limiting": limiter_result,
            "firewall_block": fw_result,
            "monitor": monitor_result
        }
    })

    # Output everything for logging node
    state["result"] = {
        "ip_analysis": ip_result,
        "rate_limiting": limiter_result,
        "firewall_block": fw_result,
        "monitor": monitor_result,
        "log": log_result
    }

    return state
