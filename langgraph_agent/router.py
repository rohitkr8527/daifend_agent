def route_to_node(state):
    threat = state.threat_type.lower()
    if threat == "ddos":
        return "ddos_node"
    elif threat == "brute_force":
        return "brute_force_node"
    elif threat == "sql_injection":
        return "sql_injection_node"
    elif threat == "ransomware":
        return "ransomware_node"
    else:
        raise ValueError(f"Unhandled threat type: {threat}")
