from tools.IPAnalyzerTool import IPAnalyzerTool
from tools.GeoBlockTool import GeoBlockTool
from tools.RateLimiterTool import RateLimiterTool
from tools.FirewallBlockerTool import FirewallBlockerTool
from tools.CDNActivator import CDNActivatorTool


def ddos_node(state: dict) -> dict:
    """
    LangGraph node to handle DDoS threats using layered tools.
    Accepts incoming context, applies defense tools, and updates state.
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
            state[tool_name] = output  # Save to shared context
            results[tool_name] = {
                "status": "success",
                "output": output
            }
        except Exception as e:
            results[tool_name] = {
                "status": "failed",
                "error": str(e)
            }

    # Add result metadata
    state["ddos_response"] = {
        "tools_executed": [tool.__class__.__name__ for tool in tool_chain],
        "status": "completed",
        "threat_type": "DDoS",
        "results": results
    }

    return state
