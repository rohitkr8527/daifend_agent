# Placeholder for nodes/sql_injection_node.py
# nodes/sql_injection_node.py

from tools.PayloadPatternDetectorTool import PayloadDetectorTool
from tools.WAFTool import WAFTool
from tools.EndpointIsolatorTool import EndpointIsolatorTool
from tools.DBQueryMonitorTool import DBQueryMonitorTool
from tools.LogTool import LogTool

def sql_injection_toolchain(state: dict) -> dict:
    data = state.get("data", {})

    print("[*] SQL Injection Toolchain Activated")

    # === Step 1: Detect Known SQLi Payloads ===
    payload_result = PayloadDetectorTool().run(data)

    # === Step 2: Apply WAF-Like Input Sanitization ===
    waf_result = WAFTool().run(data)

    # === Step 3: Isolate Vulnerable Endpoint (Mocked) ===
    isolation_result = EndpointIsolatorTool().run({
        "endpoint": data.get("url", "/unknown")  # optional key if URL exists
    })

    # === Step 4: Monitor DB Query Behavior ===
    db_monitor_result = DBQueryMonitorTool().run(data)

    # === Step 5: Log Incident ===
    log_result = LogTool().run({
        "attack": "sql_injection",
        "actions": {
            "payload_detection": payload_result,
            "waf": waf_result,
            "endpoint_isolation": isolation_result,
            "db_monitor": db_monitor_result
        }
    })

    # Attach results to state
    state["result"] = {
        "payload_detection": payload_result,
        "waf": waf_result,
        "endpoint_isolation": isolation_result,
        "db_monitor": db_monitor_result,
        "log": log_result
    }

    return state
