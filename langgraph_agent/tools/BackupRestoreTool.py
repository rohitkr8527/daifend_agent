from tools.tool_interface import ToolInterface

class BackupRestoreTool(ToolInterface):
    """
    Mocked: Simulates restoring infected directories from backup.
    In production, this would call the enterprise backup service API.
    """

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        restored = []

        for entry in logs:
            if entry.get("attack_type") == "Ransomware":
                restored.append({
                    "device_id": entry.get("device_id"),
                    "status": "Mocked - Restore triggered"
                })

        return {"BackupRestoreTool": restored}
