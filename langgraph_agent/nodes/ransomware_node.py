from tools.ProcessKillerTool import ProcessKillerTool
from tools.HostIsolationTool import HostIsolationTool
from tools.SnapShotRecoveryTool import SnapshotRecoveryTool
from tools.TemporaryFirewallTool import TemporaryFirewallTool


def ransomware_node(state: dict) -> dict:
    """
    LangGraph node to handle ransomware threats using a mitigation toolchain.
    Accepts context (state), applies sequential mitigation tools, and returns updated state.
    """
    results = {}

    tool_chain = [
        ProcessKillerTool(),
        HostIsolationTool(),
        SnapshotRecoveryTool(),
        TemporaryFirewallTool()
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

    state["ransomware_response"] = {
        "tools_executed": [tool.__class__.__name__ for tool in tool_chain],
        "status": "completed",
        "threat_type": "ransomware",
        "results": results
    }

    return state
