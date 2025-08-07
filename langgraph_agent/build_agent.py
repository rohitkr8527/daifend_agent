from langgraph.graph import END, StateGraph

# === Import shared state and routing ===
from router import route_to_node, AgentState

# === Import toolchain nodes ===
from nodes.ddos_node import ddos_node
from nodes.brute_force_node import brute_force_node
from nodes.ransomware_node import ransomware_node
from nodes.sql_injection_node import sqlin_node

# === Unknown threats (anomaly) ===
from nodes.unknown_threat_node import unknown_threat_node


def build_graph():
    """
    Constructs a LangGraph agent that routes threat data to the correct toolchain.
    Handles known threats and unknown anomalies based on routing logic.
    """

    graph = StateGraph(AgentState)

    # === Register all processing nodes ===
    graph.add_node("router", route_to_node)
    graph.add_node("ddos_node", ddos_node)
    graph.add_node("brute_force_node", brute_force_node)
    graph.add_node("ransomware_node", ransomware_node)
    graph.add_node("sql_injection_node", sqlin_node)
    graph.add_node("unknown_threat_node", unknown_threat_node)

    # === Set Entry Point ===
    graph.set_entry_point("router")

    # === Dynamic Routing using the 'next' field from router ===
    graph.add_conditional_edges("router", lambda state: state["next"])

    # === Connect each processing node to END ===
    graph.add_edge("ddos_node", END)
    graph.add_edge("brute_force_node", END)
    graph.add_edge("ransomware_node", END)
    graph.add_edge("sql_injection_node", END)
    graph.add_edge("unknown_threat_node", END)

    return graph.compile()
