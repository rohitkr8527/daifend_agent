def unknown_threat_node(state: dict) -> dict:
    print("🚨 High anomaly score detected. Potential unknown threat.")
    
    # You can add custom logic here for handling unknown threats
    state["unknown_threat_response"] = {
        "status": "alerted",
        "message": "Unknown threat encountered",
        "action_taken": "Logged and flagged for manual review"
    }

    return state
