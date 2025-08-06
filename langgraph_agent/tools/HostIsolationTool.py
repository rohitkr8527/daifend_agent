from typing import Dict
from datetime import datetime


class HostIsolationTool:
    """
    Simulates quarantining the infected host from the network.
    """
    def run(self, context: Dict) -> Dict:
        host = context.get("infected_host")
        return {
            "HostIsolationTool": {
                "host": host,
                "status": "isolated" if host else "no host specified",
                "timestamp": datetime.now(datetime.timezone.utc).isoformat()
            }
        }
