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

from toolchains import sql_injection_chain

def get_mock_context():
    return {
        "logs": [
            {"ip": "192.168.1.100", "path": "/login", "payload": "username=admin&password=' OR '1'='1"},
            {"ip": "192.168.1.101", "path": "/submit", "payload": "data=xyz"},
            {"ip": "192.168.1.102", "path": "/submit", "payload": "data=xyz&csrf_token=abc123"},
            {"ip": "192.168.1.103", "path": "/update", "payload": "drop table users;"},
        ],
        "threat_type": "sqlin"
    }

def main():
    context = get_mock_context()
    result = sql_injection_chain.execute(context)

    print("=== SQLi/CSRF Chain Execution Result ===")
    for tool, output in result.items():
        print(f"\n[{tool}]:\n{output}")

if __name__ == "__main__":
    main()
