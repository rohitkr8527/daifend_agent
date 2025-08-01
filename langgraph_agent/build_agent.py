from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import Any, Dict

from router import route_to_node
from nodes.ddos_node import ddos_toolchain
from nodes.brute_force_node import brute_force_toolchain
from nodes.sql_injection_node import sql_injection_toolchain
from nodes.ransomware_node import ransomware_toolchain
from nodes.log_node import log_node

class AgentState(BaseModel):
    threat_type: str
    confidence_score: float
    anomaly_score: float
    data: Dict[str, Any]
    result: Dict[str, Any] = {}

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", route_to_node)
    graph.add_node("ddos_node", ddos_toolchain)
    graph.add_node("brute_force_node", brute_force_toolchain)
    graph.add_node("sql_injection_node", sql_injection_toolchain)
    graph.add_node("ransomware_node", ransomware_toolchain)
    graph.add_node("log_node", log_node)

    graph.set_entry_point("router")

    # Real conditional logic
    graph.add_conditional_edges(
        "router",
        {
            "ddos_node": lambda x: x.threat_type == "ddos",
            "brute_force_node": lambda x: x.threat_type == "brute_force",
            "sql_injection_node": lambda x: x.threat_type == "sql_injection",
            "ransomware_node": lambda x: x.threat_type == "ransomware",
        },
    )

    graph.add_edge("ddos_node", "log_node")
    graph.add_edge("brute_force_node", "log_node")
    graph.add_edge("sql_injection_node", "log_node")
    graph.add_edge("ransomware_node", "log_node")
    graph.add_edge("log_node", END)

    return graph.compile()
