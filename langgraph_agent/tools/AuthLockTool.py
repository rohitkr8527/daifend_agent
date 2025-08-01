from collections import defaultdict
from tools.tool_interface import ToolInterface

class AuthLockTool(ToolInterface):
    """
    Locks user accounts after repeated failed login attempts.
    """

    def __init__(self, threshold=5):
        self.threshold = threshold

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        failed_users = defaultdict(int)
        locked_accounts = []

        for entry in logs:
            if "Brute Force" in entry.get("alert_message", "") and entry.get("alert", False):
                user = entry.get("user_id")
                if user:
                    failed_users[user] += 1
                    if failed_users[user] == self.threshold:
                        locked_accounts.append({
                            "user_id": user,
                            "action": "Account locked due to failed logins"
                        })

        return {"AuthLockTool": locked_accounts}
