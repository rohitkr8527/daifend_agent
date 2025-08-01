# Placeholder for tools/FileActivityMonitorTool.py
from tools.tool_interface import ToolInterface

class FileActivityMonitorTool(ToolInterface):
    """
    Detects suspicious file activity indicative of ransomware (mass renames, .encrypted extensions).
    """

    def __init__(self, rename_threshold: int = 1000):
        self.rename_threshold = rename_threshold
        self.suspicious_extensions = [".encrypted", ".locky", ".crypto", ".locked"]

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        flagged = []

        for entry in logs:
            if entry.get("attack_type") == "Ransomware":
                file_count = entry.get("file_rename_count", 0)
                alert_msg = entry.get("alert_message", "").lower()

                if file_count > self.rename_threshold or any(ext in alert_msg for ext in self.suspicious_extensions):
                    flagged.append({
                        "device_id": entry.get("device_id"),
                        "renamed_files": file_count,
                        "match_reason": "bulk_renames" if file_count > self.rename_threshold else "extension_pattern",
                        "action": "Suspected ransomware behavior"
                    })

        return {"FileActivityMonitorTool": flagged}
