# ddos_chain.py

from tools.IPAnalyzerTool import IPAnalyzerTool
from tools.RateLimiterTool import RateLimiterTool
from tools.GeoBlockTool import GeoBlockTool
from tools.MonitorTool import MonitorTool
from tools.AlertTool import AlertTool
from tools.FirewallBlockerTool import FirewallBlockerTool
from tools.LogTool import LogTool


def handle_ddos_threat(state):
    """
    Executes the DDoS response toolchain using modular tools.
    Args:
        state (AgentState): LangGraph state with threat details
    Returns:
        AgentState: Updated state with results
    """
    data = state.data
    results = {}

    # Tool 1: Analyze source IPs for abnormal patterns
    ip_analyzer = IPAnalyzerTool()
    results["ip_analysis"] = ip_analyzer.run(data)

    # Tool 2: Enforce adaptive rate limiting
    rate_limiter = RateLimiterTool()
    results["rate_limiting"] = rate_limiter.run(data)

    # Tool 3: Block requests from malicious geolocations
    geo_block = GeoBlockTool()
    results["geo_blocking"] = geo_block.run(data)

    # Tool 4: Enable firewall rules to block abnormal traffic
    firewall = FirewallBlockerTool()
    results["firewall_blocking"] = firewall.run(data)

    # Tool 5: Enable network monitoring for continued observation
    monitor = MonitorTool()
    results["monitoring"] = monitor.run(data)

    # Tool 6: Raise an alert to admins
    alert = AlertTool()
    results["alerting"] = alert.run(data)

    # Tool 7: Log everything
    logger = LogTool()
    results["logging"] = logger.run({
        "threat_type": "ddos",
        "details": results
    })

    state.result = results
    return state
