# Placeholder for nodes/brute_force_node.py
# nodes/brute_force_node.py

from tools.IPAnalyzerTool import IPAnalyzerTool
from tools.LoginAttemptMonitorTool import LoginAttemptMonitorTool
from tools.AuthLockTool import AuthLockTool
from tools.RateLimiterTool import RateLimiterTool
from tools.FirewallBlockerTool import FirewallBlockerTool
from tools.LogTool import LogTool

def brute_force_toolchain(state: dict) -> dict:
    data = state.get("data", {})

    print("[*] Brute Force Toolchain Activated")

    # === Step 1: Analyze Failed Login Sources ===
    ip_result = IPAnalyzerTool().run(data)

    # === Step 2: Monitor Repeated Login Attempts ===
    login_monitor_result = LoginAttemptMonitorTool().run(data)

    # === Step 3: Lock Accounts After Threshold ===
    auth_lock_result = AuthLockTool().run(data)

    # === Step 4: Rate Limit IPs Making Too Many Requests ===
    limiter_result = RateLimiterTool().run(data)

    # === Step 5: Block IPs (optional / mocked) ===
    fw_result = FirewallBlockerTool().run({
        "block_ips": [entry["ip"] for entry in ip_result.get("flagged_ips", [])]
    })

    # === Step 6: Log Everything ===
    log_result = LogTool().run({
        "attack": "brute_force",
        "actions": {
            "ip_analysis": ip_result,
            "login_monitoring": login_monitor_result,
            "auth_lock": auth_lock_result,
            "rate_limiting": limiter_result,
            "firewall_block": fw_result
        }
    })

    # Attach results to state
    state["result"] = {
        "ip_analysis": ip_result,
        "login_monitoring": login_monitor_result,
        "auth_lock": auth_lock_result,
        "rate_limiting": limiter_result,
        "firewall_block": fw_result,
        "log": log_result
    }

    return state
