from build_agent import build_graph
from router import AgentState

# Build the LangGraph agent
graph = build_graph()

# Example test input (SQL Injection case)
test_input = {
    "threat_type": "sql_injection",  # try changing this to "ddos", "brute_force", "ransomware", or use high anomaly_score
    "anomaly_score": 0.3,            # set > 0.85 to test unknown threat routing
    "data": {
        "ip": "192.168.1.100",
        "url": "/login.php?id=1' OR '1'='1",
        "method": "GET"
    }
}

# Run the graph with the test input
final_state = graph.invoke(AgentState(**test_input))

# Print results
from pprint import pprint
pprint(final_state)
