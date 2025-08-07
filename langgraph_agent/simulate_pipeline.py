from build_agent import build_graph
from router import AgentState
from pprint import pprint

# -------------------------------
# Layer 1: Simulated Normalized Logs
# -------------------------------

def layer_1_log_ingestion():
    # You can manually specify known threat logs here
    log = {
        "timestamp": "2025-07-18T14:22:31Z",
        "src_ip": "192.168.1.45",
        "dest_ip": "93.184.216.34",
        "src_port": 54231,
        "dest_port": 80,
        "protocol": "TCP",
        "packet_length": 512,
        "duration": 3.57,
        "conn_state": "S1",
        "tcp_flags": "SYN, ACK",
        "payload_bytes": 452,
        "alert": True,
        "alert_message": "Possible DDoS attempt detected",
        "attack_type": "DDoS",
        "attack_signature_id": "SIG20301",
        "mitre_attack_tactics": "TA0011",
        "severity_level": "High",
        "action_taken": "Blocked IP, Alerted SOC",
        "confidence_score": 92.5,
        "user_id": "user123",
        "device_id": "deviceA5",
        "geo_location": "New York, USA",
        "network_segment": "Internal DMZ",
        "local_src": True,
        "local_dest": False,
        "proxy_used": True,
        "proxy_info": "proxy.corp.local:3128",
        "dns_response_ips": "93.184.216.34",
        "certificate_info": "Let's Encrypt R3, Valid till Sep 2025",
        "log_source": "Zeek",
        "sensor_id": "sensor_23",
        "session_id": "C8el6C2OaYlFddr8K",
        "community_id": "1:hVfzyVnLbY7cWjkVkXsx1uGNL7s=",
        "malware_family": "Mirai",
        "ioc_type": "IP",
        "ioc_value": "198.51.100.101",
        "yara_rule_match": "mirai_detection_rule",
        "file_hash": "3b2f1a5c5d9c8c6f8f2f6e13e7f92434"
    }
    return log

# -------------------------------
# Layer 2: Threat Classification
# -------------------------------

def layer_2_threat_classification(log):
    # You already know it's a DDoS from the log
    threat_type = "ddos"
    anomaly_score = 0.22
    return threat_type, anomaly_score

# -------------------------------
# Layer 3: LangGraph Self-Healing Agent
# -------------------------------

def layer_3_run_agent(threat_type, anomaly_score, log):
    graph = build_graph()
    input_state = {
        "threat_type": threat_type,
        "anomaly_score": anomaly_score,
        "data": log
    }
    final_state = graph.invoke(AgentState(**input_state))
    return final_state

# -------------------------------
# Run Full Pipeline
# -------------------------------

if __name__ == "__main__":
    print("\n--- Layer 1: Ingesting Normalized Log ---")
    normalized_log = layer_1_log_ingestion()
   

    print("\n--- Layer 2: Detecting Threat Type & Anomaly Score ---")
    threat_type, anomaly_score = layer_2_threat_classification(normalized_log)


    print("\n--- Layer 3: Executing Self-Healing Agent ---")
    result = layer_3_run_agent(threat_type, anomaly_score, normalized_log)
    pprint(result)
