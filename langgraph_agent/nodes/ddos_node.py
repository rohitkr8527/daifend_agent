from tools.IPAnalyzerTool import IPAnalyzerTool
from tools.GeoBlockTool import GeoBlockTool
from tools.RateLimiterTool import RateLimiterTool
from tools.FirewallBlockerTool import FirewallBlockerTool
from tools.CDNActivator import CDNActivatorTool


def ddos_node(state: dict) -> dict:
    """
    LangGraph node to handle DDoS threats using layered tools.
    Accepts shared state, applies tools, updates state in-place.
    """
    results = {}

    tool_chain = [
        IPAnalyzerTool(),
        GeoBlockTool(),
        RateLimiterTool(),
        FirewallBlockerTool(),
        CDNActivatorTool()
    ]

    for tool in tool_chain:
        tool_name = tool.__class__.__name__
        try:
            output = tool.run(state)
            state[tool_name] = output
            results[tool_name] = {
                "status": "success",
                "output": output
            }
        except Exception as e:
            results[tool_name] = {
                "status": "failed",
                "error": str(e)
            }

    state["ddos_response"] = {
        "tools_executed": [tool.__class__.__name__ for tool in tool_chain],
        "status": "completed",
        "threat_type": "DDoS",
        "results": results
    }

    return state
