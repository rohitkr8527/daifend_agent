from tools.LogTool import LogTool

def log_node(state):
    result_data = state.result
    threat = state.threat_type

    log_data = {
        "threat_type": threat,
        "final_result": result_data
    }

    LogTool().run(log_data)
    print(f"[✓] Final result for '{threat}' logged.")
    return state
