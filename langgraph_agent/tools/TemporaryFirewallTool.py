from typing import Dict
from datetime import datetime


class TemporaryFirewallTool:
    """
    Simulates applying temporary rules to block lateral movement.
    """
    def run(self, context: Dict) -> Dict:
        return {
            "TemporaryFirewallTool": {
                "rules_applied": ["Block SMB", "Block RDP", "Block PsExec"],
                "duration": "1 hour",
                "timestamp": datetime.now(datetime.timezone.utc).isoformat()
            }
        }