# brute_force_chain.py

from tools.LoginAttemptMonitorTool import LoginAttemptMonitorTool
from tools.AuthLockTool import AuthLockTool
from tools.WAFTool import WAFTool
from tools.ProcessKillerTool import ProcessKillerTool
from tools.AlertTool import AlertTool
from tools.LogTool import LogTool


def handle_brute_force_threat(state):
    """
    Executes the brute-force attack response toolchain using modular tools.
    Args:
        state (AgentState): LangGraph state with threat details
    Returns:
        AgentState: Updated state with results
    """
    data = state.data
    results = {}

    # Tool 1: Monitor failed login attempts
    login_monitor = LoginAttemptMonitorTool()
    results["login_monitoring"] = login_monitor.run(data)

    # Tool 2: Lock user accounts temporarily
    auth_locker = AuthLockTool()
    results["auth_lock"] = auth_locker.run(data)

    # Tool 3: Block attacker via WAF rules
    waf_blocker = WAFTool()
    results["waf_blocking"] = waf_blocker.run(data)

    # Tool 4: Kill suspicious login brute-force process
    process_killer = ProcessKillerTool()
    results["process_killing"] = process_killer.run(data)

    # Tool 5: Trigger alert
    alert = AlertTool()
    results["alerting"] = alert.run(data)

    # Tool 6: Log the response
    logger = LogTool()
    results["logging"] = logger.run({
        "threat_type": "brute_force",
        "details": results
    })

    state.result = results
    return state
