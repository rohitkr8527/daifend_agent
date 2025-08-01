# ransomware_chain.py

from tools.FileActivityMonitorTool import FileActivityMonitorTool
from tools.EndpointIsolatorTool import EndpointIsolatorTool
from tools.BackupRestoreTool import BackupRestoreTool
from tools.RestoreSnapshotTool import RestoreSnapshotTool
from tools.AuthLockTool import AuthLockTool
from tools.AlertTool import AlertTool
from tools.LogTool import LogTool


def handle_ransomware_threat(state):
    """
    Executes the ransomware response toolchain using modular tools.
    Args:
        state (AgentState): LangGraph state with threat details
    Returns:
        AgentState: Updated state with results
    """
    data = state.data
    results = {}

    # Tool 1: Monitor abnormal file activities (e.g., mass encryption)
    file_monitor = FileActivityMonitorTool()
    results["file_monitoring"] = file_monitor.run(data)

    # Tool 2: Isolate the infected endpoint
    isolator = EndpointIsolatorTool()
    results["endpoint_isolation"] = isolator.run(data)

    # Tool 3: Lock critical user accounts (mocked or real)
    auth_locker = AuthLockTool()
    results["auth_lock"] = auth_locker.run(data)

    # Tool 4: Restore from backup if available
    backup_restore = BackupRestoreTool()
    results["backup_restore"] = backup_restore.run(data)

    # Tool 5: Restore system snapshot if backup fails
    snapshot_restore = RestoreSnapshotTool()
    results["snapshot_restore"] = snapshot_restore.run(data)

    # Tool 6: Trigger alert to SOC/admin
    alert = AlertTool()
    results["alerting"] = alert.run(data)

    # Tool 7: Log the full response flow
    logger = LogTool()
    results["logging"] = logger.run({
        "threat_type": "ransomware",
        "details": results
    })

    state.result = results
    return state
