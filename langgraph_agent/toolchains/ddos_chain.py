from tools.IPAnalyzerTool import IPAnalyzerTool
from tools.GeoBlockTool import GeoBlockTool
from tools.RateLimiterTool import RateLimiterTool
from tools.FirewallBlockerTool import FirewallBlockerTool
from tools.CDNActivator import CDNActivatorTool


def execute(context: dict) -> dict:
    """
    Executes the full DDoS mitigation chain in order.
    Updates the context with tool outputs and returns final result.
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
            output = tool.run(context)
            context.update({tool_name: output})
            results[tool_name] = output
        except Exception as e:
            results[tool_name] = {
                "error": str(e),
                "status": "failed"
            }

    results["meta"] = {
        "threat_type": "DDoS",
        "status": "completed",
        "tools_executed": [tool.__class__.__name__ for tool in tool_chain]
    }

    return results
