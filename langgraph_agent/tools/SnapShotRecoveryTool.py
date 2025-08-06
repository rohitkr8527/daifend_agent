from typing import Dict
from datetime import datetime


class SnapshotRecoveryTool:
    """
    Simulates system restoration from a backup snapshot.
    """
    def run(self, context: Dict) -> Dict:
        host = context.get("infected_host")
        return {
            "SnapshotRecoveryTool": {
                "host": host,
                "restored": bool(host),
                "method": "snapshot" if host else None,
                "timestamp": datetime.now(datetime.timezone.utc).isoformat()
            }
        }
