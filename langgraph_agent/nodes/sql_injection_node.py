from tools.WebRequestMonitorTool import WebRequestMonitorTool
from tools.WAFMonitorTool import WAFMonitorTool


def sqlin_node(state: dict) -> dict:
    """
    LangGraph node to handle SQL Injection & CSRF threats.
    Executes a simplified two-tool mitigation chain.
    """
    results = {}

    tool_chain = [
        WebRequestMonitorTool(),
        WAFMonitorTool()
    ]

    for tool in tool_chain:
        tool_name = tool.__class__.__name__

        try:
            output = tool.run(state)
            results[tool_name] = {
                "status": "success",
                "output": output
            }
        except Exception as e:
            results[tool_name] = {
                "status": "failed",
                "error": str(e)
            }

    return {
        "sqlin_response": {
            "tools_executed": [tool.__class__.__name__ for tool in tool_chain],
            "status": "completed",
            "threat_type": "sqlin",
            "results": results
        }
    }
