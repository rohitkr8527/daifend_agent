# toolchains/sqlin_chain.py

from tools.WebRequestMonitorTool import WebRequestMonitorTool
from tools.WAFMonitorTool import WAFMonitorTool

def execute(context: dict) -> dict:
    """
    Executes the SQL Injection and CSRF mitigation toolchain.
    """
    results = {}
    tool_chain = [
        WebRequestMonitorTool(),
        WAFMonitorTool()
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
        "threat_type": "sqlin",
        "status": "completed",
        "tools_executed": [tool.__class__.__name__ for tool in tool_chain]
    }

    return results
