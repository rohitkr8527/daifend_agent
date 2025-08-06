# 
## --------ddos_chain.py--------##
# test_ddos_chain.py

# from toolchains import ddos_chain

# def get_mock_context():
#     """
#     Simulated context extracted from logs and threat classifier.
#     These are typical DDoS-related features.
#     """
#     return {
#         "source_ips": [
#             "192.168.1.101", "192.168.1.102", "10.0.0.5", "45.56.78.90"
#         ],
#         "destination_ip": "172.16.0.10",
#         "unusual_traffic_volume": True,
#         "suspicious_patterns": [
#             "SYN flood", "UDP amplification"
#         ],
#         "timestamp": "2025-08-06T12:00:00Z",
#         "geo_data": {
#             "192.168.1.101": "IN",
#             "192.168.1.102": "IN",
#             "10.0.0.5": "RU",
#             "45.56.78.90": "CN"
#         },
#         "request_rate": {
#             "192.168.1.101": 1500,
#             "192.168.1.102": 1800,
#             "10.0.0.5": 3200,
#             "45.56.78.90": 5000
#         },
#         "threat_type": "DDoS"
#     }

# def main():
#     context = get_mock_context()
#     result = ddos_chain.execute(context)

#     print("=== DDoS Chain Execution Result ===")
#     for tool, output in result.items():
#         print(f"\n[{tool}]:\n{output}")


# if __name__ == "__main__":
#     main()

##---------ransomware_chain.py--------##
# test_ransomware_chain.py

# from toolchains import ransomware_chain

# def get_mock_context():
#     return {
#         "infected_host": "host-xyz.local",
#         "encryption_detected": True,
#         "ransom_note_found": True,
#         "timestamp": "2025-08-06T14:30:00Z",
#         "threat_type": "ransomware",
#         "suspicious_processes": [
#             {"pid": 2331, "name": "encryptor.exe", "entropy": 8.2},
#             {"pid": 8742, "name": "safe_process", "entropy": 3.1},
#             {"pid": 9921, "name": "encrypt_payload", "entropy": 9.0}
#         ]
#     }

# def main():
#     context = get_mock_context()
#     result = ransomware_chain.execute(context)

#     print("=== Ransomware Chain Execution Result ===")
#     for tool, output in result.items():
#         print(f"\n[{tool}]:\n{output}")

# if __name__ == "__main__":
#     main()

##---------sql_injection_chain.py--------##
# test_sqlin_chain.py

# from toolchains import sql_injection_chain

# def get_mock_context():
#     return {
#         "logs": [
#             {"ip": "192.168.1.100", "path": "/login", "payload": "username=admin&password=' OR '1'='1"},
#             {"ip": "192.168.1.101", "path": "/submit", "payload": "data=xyz"},
#             {"ip": "192.168.1.102", "path": "/submit", "payload": "data=xyz&csrf_token=abc123"},
#             {"ip": "192.168.1.103", "path": "/update", "payload": "drop table users;"},
#         ],
#         "threat_type": "sqlin"
#     }

# def main():
#     context = get_mock_context()
#     result = sql_injection_chain.execute(context)

#     print("=== SQLi/CSRF Chain Execution Result ===")
#     for tool, output in result.items():
#         print(f"\n[{tool}]:\n{output}")

# if __name__ == "__main__":
#     main()

##---------brute_force_chain.py--------##
# test_brute_force_chain.py

import json
from datetime import datetime, timedelta, timezone

from toolchains.brute_force_chain import execute


def generate_test_logs():
    """
    Generate sample log entries to simulate brute force behavior.
    """
    now = datetime.now(timezone.utc)
    logs = []

    # IP with repeated failed login attempts (should be flagged)
    for i in range(7):
        logs.append({
            "timestamp": (now - timedelta(seconds=i * 60)).isoformat(),
            "src_ip": "192.168.1.101",
            "event_type": "login_attempt",
            "status": "failed",
            "user_id": "user_alpha",
            "username": "user_alpha",
            "success": False
        })

    # Another user with fewer failures (should not be locked)
    for i in range(2):
        logs.append({
            "timestamp": (now - timedelta(seconds=i * 120)).isoformat(),
            "src_ip": "192.168.1.202",
            "event_type": "login_attempt",
            "status": "failed",
            "user_id": "user_beta",
            "username": "user_beta",
            "success": False
        })

    # Successful login attempt (should be ignored)
    logs.append({
        "timestamp": now.isoformat(),
        "src_ip": "192.168.1.150",
        "event_type": "login_attempt",
        "status": "success",
        "user_id": "user_alpha",
        "username": "user_alpha",
        "success": True
    })

    return logs


def main():
    # Simulate Layer 3 input
    context = {
        "logs": generate_test_logs(),
        "attack_type": "brute_force",
        "alert": True,
        "alert_message": "Brute force attempt detected",
        "severity_level": "Medium",
        "confidence_score": 88.5
    }

    # Run brute force toolchain
    result = execute(context)

    # Print summary output
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
