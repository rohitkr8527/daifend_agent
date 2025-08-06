from tools.FailedLoginMonitorTool import FailedLoginMonitorTool
from tools.IPBlackListTool import IPBlacklistTool
from tools.AuthLockTool import AccountLockTool
from tools.RateLimiterTool import RateLimiterTool


def execute(context: dict) -> dict:
    """
    Executes the brute-force mitigation toolchain.
    Applies multiple layered defenses against credential-stuffing and login-based attacks.
    """
    results = {}

    # Set mode for RateLimiterTool
    context["limit_type"] = "brute_force"

    # Define tool sequence
    tool_chain = [
        FailedLoginMonitorTool(),
        IPBlacklistTool(),
        AccountLockTool(),
        RateLimiterTool()
    ]

    for tool in tool_chain:
        tool_name = tool.__class__.__name__

        try:
            output = tool.run(context)
            context[tool_name] = output  # Save tool output into context
            results[tool_name] = {
                "status": "success",
                "output": output
            }
        except Exception as e:
            results[tool_name] = {
                "status": "failed",
                "error": str(e)
            }

    results["meta"] = {
        "threat_type": "brute_force",
        "status": "completed",
        "tools_executed": [tool.__class__.__name__ for tool in tool_chain]
    }

    return results
