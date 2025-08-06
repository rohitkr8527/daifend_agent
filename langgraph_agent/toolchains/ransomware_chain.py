from tools.HostIsolationTool import HostIsolationTool
from tools.SnapShotRecoveryTool import SnapshotRecoveryTool
from tools.ProcessKillerTool import ProcessKillerTool

def execute(context: dict) -> dict:
    """
    Executes the ransomware mitigation toolchain.
    """
    results = {}
    tool_chain = [
        HostIsolationTool(),
        ProcessKillerTool(),          
        SnapshotRecoveryTool()
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
        "threat_type": "ransomware",
        "status": "completed",
        "tools_executed": [tool.__class__.__name__ for tool in tool_chain]
    }

    return results
