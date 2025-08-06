from langgraph.graph import END, StateGraph

# === Agent state and routing logic ===
from router import route_to_node, AgentState

# === Toolchain nodes ===
from toolchains import ddos_chain
from toolchains import brute_force_chain
from toolchains import sql_injection_chain
from toolchains import ransomware_chain

# === Unknown threat (anomaly) node ===
from nodes.unknown_threat_node import unknown_threat_node

# === Final log node ===
from nodes.log_node import log_node


def build_graph():
    """
    Constructs the LangGraph-based cybersecurity agent.
    Routes incoming threat logs to the appropriate toolchain or anomaly handler.
    """

    graph = StateGraph(AgentState)

    # === Add processing nodes ===
    graph.add_node("router", route_to_node)
    graph.add_node("ddos_node", ddos_chain)
    graph.add_node("brute_force_node", brute_force_chain)
    graph.add_node("sql_injection_node", sql_injection_chain)
    graph.add_node("ransomware_node", ransomware_chain)
    graph.add_node("unknown_threat_node", unknown_threat_node)
    graph.add_node("log_node", log_node)

    # === Entry point ===
    graph.set_entry_point("router")

    # === Conditional Routing ===
    graph.add_conditional_edges(
        "router",
        {
            "ddos_node": lambda x: x.threat_type == "ddos",
            "brute_force_node": lambda x: x.threat_type == "brute_force",
            "sql_injection_node": lambda x: x.threat_type == "sql_injection",
            "ransomware_node": lambda x: x.threat_type == "ransomware",
            "unknown_threat_node": lambda x: x.anomaly_score > 0.85,  # High anomaly → unknown threat
        },
    )

    # === Connect all branches to final log node ===
    graph.add_edge("ddos_node", "log_node")
    graph.add_edge("brute_force_node", "log_node")
    graph.add_edge("sql_injection_node", "log_node")
    graph.add_edge("ransomware_node", "log_node")
    graph.add_edge("unknown_threat_node", "log_node")
    graph.add_edge("log_node", END)

    return graph.compile()
