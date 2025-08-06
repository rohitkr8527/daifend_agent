from typing import Dict, List
from datetime import datetime


class ProcessKillerTool:
    """
    Simulates killing ransomware-related processes.
    """
    def run(self, context: Dict) -> Dict:
        suspicious_procs: List[Dict] = context.get("suspicious_processes", [])
        killed = [
            proc for proc in suspicious_procs
            if proc.get("entropy", 0) > 7.5 or "encrypt" in proc.get("name", "").lower()
        ]

        return {
            "ProcessKillerTool": {
                "killed_processes": killed,
                "timestamp": datetime.now(datetime.timezone.utc).isoformat()
            }
        }
