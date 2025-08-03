# from datetime import datetime, timedelta, timezone
# from tools.IPAnalyzerTool import IPAnalyzerTool  # Adjust import path as per your project

# # Create sample logs within the last minute
# now = datetime.now(timezone.utc)
# logs = []

# # Simulate 25 requests from one IP, 15 from another
# for _ in range(25):
#     logs.append({
#         "timestamp": (now - timedelta(seconds=20)).isoformat(),
#         "src_ip": "192.168.1.100"
#     })

# for _ in range(15):
#     logs.append({
#         "timestamp": (now - timedelta(seconds=40)).isoformat(),
#         "src_ip": "192.168.1.101"
#     })

# # Initialize tool with correct parameter
# tool = IPAnalyzerTool(threshold_per_minute=20)

# # Run tool
# result = tool.run({"logs": logs})

# # Print actual output
# print(result)

from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)
logs = [
    {"timestamp": (now - timedelta(seconds=30)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": (now - timedelta(seconds=25)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": (now - timedelta(seconds=20)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": (now - timedelta(seconds=15)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": (now - timedelta(seconds=10)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": (now - timedelta(seconds=5)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": (now - timedelta(seconds=4)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": (now - timedelta(seconds=3)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": (now - timedelta(seconds=2)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": (now - timedelta(seconds=1)).isoformat(), "src_ip": "192.168.1.10"},
    {"timestamp": now.isoformat(), "src_ip": "192.168.1.10"},
]

from tools.RateLimiterTool import RateLimiterTool
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)

# Simulated logs (11 requests in 60 sec from same IP)
logs = [
    {"timestamp": (now - timedelta(seconds=i)).isoformat(), "src_ip": "192.168.1.10"}
    for i in range(11)
]

# Initialize and run tool
tool = RateLimiterTool(decay_factor=0.2)
result = tool.run({"logs": logs})

# Pretty print result
print("=== RateLimiterTool Test Output ===")
from pprint import pprint
pprint(result)
