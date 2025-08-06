def router_node(state: dict) -> str:
    """
    Routes the threat to the correct node based on 'threat_type' in the state.

    Returns the name of the next node.
    """
    threat_type = state.get("threat_type", "").lower()

    if threat_type == "ddos":
        return "ddos_response"
    elif threat_type == "brute_force":
        return "brute_force_response"
    elif threat_type == "sqlin":
        return "sqlin_response"
    elif threat_type == "ransomware":
        return "ransomware_response"
    else:
        return "unknown_threat_handler"
