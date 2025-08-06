from tools.FailedLoginMonitorTool import FailedLoginMonitorTool
from tools.IPBlackListTool import IPBlacklistTool
from tools.AuthLockTool import AccountLockTool
from tools.RateLimiterTool import RateLimiterTool


def brute_force_node(state: dict) -> dict:
    """
    LangGraph node to handle brute-force threats using a predefined toolchain.
    Input: Layer 3 context from upstream graph
    Output: Updated context including mitigation results
    """
    results = {}

    # Set mode for RateLimiterTool
    state["limit_type"] = "brute_force"

    # Define tool execution sequence
    tool_chain = [
        FailedLoginMonitorTool(),
        IPBlacklistTool(),
        AccountLockTool(),
        RateLimiterTool()
    ]

    for tool in tool_chain:
        tool_name = tool.__class__.__name__

        try:
            output = tool.run(state)
            state[tool_name] = output  # Update shared state for chaining
            results[tool_name] = {
                "status": "success",
                "output": output
            }
        except Exception as e:
            results[tool_name] = {
                "status": "failed",
                "error": str(e)
            }

    # Add toolchain metadata
    state["brute_force_response"] = {
        "tools_executed": [tool.__class__.__name__ for tool in tool_chain],
        "status": "completed",
        "threat_type": "brute_force",
        "results": results
    }

    return state
