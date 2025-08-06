from typing import Dict, List, Optional
import time


class AccountLockTool:
    """
    Locks user accounts temporarily after repeated failed login attempts.
    Useful against brute-force attacks targeting usernames.

    Example Policy:
        - 5 failed attempts within 10 minutes → lock for 15 minutes.
    """

    def __init__(self, max_attempts: int = 5, window_seconds: int = 600, lock_duration: int = 900):
        self.max_attempts = max_attempts          # e.g., 5 failures
        self.window_seconds = window_seconds      # e.g., 10 minutes
        self.lock_duration = lock_duration        # e.g., 15 minutes

        self.failed_attempts = {}  # {username: [timestamps]}
        self.locked_accounts = {}  # {username: unlock_timestamp}

    def run(self, context: Dict) -> Dict:
        logs = context.get("logs", [])

        now = time.time()
        locked_users = []
        just_locked = []

        for entry in logs:
            username = entry.get("username")
            success = entry.get("success", True)

            if not username or success:
                continue

            # Check if account is already locked
            unlock_time = self.locked_accounts.get(username)
            if unlock_time and now < unlock_time:
                locked_users.append({
                    "username": username,
                    "status": "still locked",
                    "unlocks_at": unlock_time
                })
                continue

            # If unlocked, reset status
            if unlock_time and now >= unlock_time:
                self.locked_accounts.pop(username, None)
                self.failed_attempts.pop(username, None)

            # Track failed attempt
            self.failed_attempts.setdefault(username, []).append(now)
            self._prune_old_attempts(username, now)

            # Check if it exceeds threshold
            if len(self.failed_attempts[username]) >= self.max_attempts:
                self.locked_accounts[username] = now + self.lock_duration
                just_locked.append({
                    "username": username,
                    "status": "locked",
                    "unlocks_at": self.locked_accounts[username]
                })
                self.failed_attempts.pop(username, None)

        return {
            "locked_accounts": locked_users + just_locked,
            "meta": {
                "just_locked_count": len(just_locked),
                "total_locked": len(self.locked_accounts)
            }
        }

    def _prune_old_attempts(self, username: str, now: float):
        timestamps = self.failed_attempts.get(username, [])
        self.failed_attempts[username] = [
            t for t in timestamps if now - t <= self.window_seconds
        ]
