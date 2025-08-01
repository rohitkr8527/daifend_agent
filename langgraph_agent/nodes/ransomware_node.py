# Placeholder for nodes/ransomware_node.py
# nodes/ransomware_node.py

from tools.FileActivityMonitorTool import FileActivityMonitorTool
from tools.ProcessKillerTool import ProcessKillerTool
from tools.BackupRestoreTool import BackupRestoreTool
from tools.EndpointIsolatorTool import EndpointIsolatorTool
from tools.LogTool import LogTool

def ransomware_toolchain(state: dict) -> dict:
    data = state.get("data", {})

    print("[*] Ransomware Toolchain Activated")

    # === Step 1: Detect Suspicious File Activity ===
    file_activity_result = FileActivityMonitorTool().run(data)

    # === Step 2: Kill Suspected Encryption Scripts ===
    kill_result = ProcessKillerTool().run(data)

    # === Step 3: Restore Affected Directories ===
    restore_result = BackupRestoreTool().run(data)

    # === Step 4: Isolate Infected Endpoint ===
    isolate_result = EndpointIsolatorTool().run({
        "device_id": data.get("device_id")
    })

    # === Step 5: Log Event ===
    log_result = LogTool().run({
        "attack": "ransomware",
        "actions": {
            "file_activity": file_activity_result,
            "process_kill": kill_result,
            "restore": restore_result,
            "isolation": isolate_result
        }
    })

    # Attach results to state
    state["result"] = {
        "file_activity": file_activity_result,
        "process_kill": kill_result,
        "restore": restore_result,
        "isolation": isolate_result,
        "log": log_result
    }

    return state
