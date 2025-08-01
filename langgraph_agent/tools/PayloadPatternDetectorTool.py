# Placeholder for tools/PayloadPatternDetectorTool.py
import re
from tools.tool_interface import ToolInterface

class PayloadDetectorTool(ToolInterface):
    """
    Detects common SQL injection payloads in the request body or query.
    """

    def __init__(self):
        self.patterns = [
            r"(?i)(\bUNION\b|\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b)",
            r"(?i)(\bOR\b\s+\d+=\d+)", 
            r"(?i)(--|#)",  # SQL comments
            r"(?i)('|\")\s*or\s*('|\")?\d+('|\")?\s*=\s*\d+"  # tautologies
        ]

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        flagged = []

        for entry in logs:
            payload = entry.get("alert_message", "")
            for pattern in self.patterns:
                if re.search(pattern, payload):
                    flagged.append({
                        "ip": entry.get("src_ip"),
                        "pattern": pattern,
                        "detected": payload
                    })
                    break

        return {"PayloadDetectorTool": flagged}
