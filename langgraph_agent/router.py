from typing import Annotated, TypedDict, Optional, Union

class AgentState(TypedDict, total=False):
    threat_type: Optional[str]       # e.g., "ddos", "brute_force", etc.
    anomaly_score: Optional[float]   # used to route unknown threats
    data: dict                       # the actual threat data payload
    result: dict                     # the output from the node

def route_to_node(state: AgentState) -> dict:
    """
    Routes input state to the correct node based on the threat_type or anomaly_score.
    Returns a dict with key 'next' as required by LangGraph conditional routing.
    """
    threat_type = state.get("threat_type")
    anomaly_score = state.get("anomaly_score", 0)

    if anomaly_score > 0.85:
        return {"next": "unknown_threat_node"}

    match threat_type:
        case "ddos":
            return {"next": "ddos_node"}
        case "brute_force":
            return {"next": "brute_force_node"}
        case "ransomware":
            return {"next": "ransomware_node"}
        case "sql_injection" | "sqlin":
            return {"next": "sql_injection_node"}
        case _:
            return {"next": "unknown_threat_node"}
