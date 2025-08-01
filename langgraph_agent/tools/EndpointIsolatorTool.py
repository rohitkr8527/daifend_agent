from tools.tool_interface import ToolInterface

class EndpointIsolatorTool(ToolInterface):
    """
    Simulates isolating a vulnerable endpoint (e.g., /search).
    """

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        isolated = []

        for entry in logs:
            if entry.get("attack_type") == "SQL Injection":
                endpoint = entry.get("alert_message", "").split("on")[-1].strip()
                isolated.append({
                    "endpoint": endpoint,
                    "action": "Isolated endpoint temporarily due to SQLi"
                })

        return {"EndpointIsolatorTool": isolated}
