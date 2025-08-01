from tools.tool_interface import ToolInterface

class WAFTool(ToolInterface):
    """
    Mocked: Applies WAF-like filtering rules.
    In production, this would push rules to a WAF like AWS WAF or ModSecurity.
    """

    def run(self, context: dict) -> dict:
        return {
            "WAFTool": [{
                "rule": "Sanitize input for SQL keywords",
                "status": "Mocked - Rule applied in simulation"
            }]
        }
