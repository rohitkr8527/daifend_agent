from build_agent import build_graph
from build_agent import AgentState


if __name__ == "__main__":
    print("[+] Running LangGraph Self-Healing Agent...\n")

    input_state = AgentState(
        threat_type="ddos",
        confidence_score=0.93,
        anomaly_score=0.88,
        data={
            "src_ip": "198.51.100.101",
            "geo_location": "Russia",
            "request_rate": 21.5,
            "endpoint": "/login"
        },
        result={}
    )

    graph = build_graph()
    final_state = graph.invoke(input_state)
    print("\n[✓] Final State Output:")
    print(final_state.dict())
