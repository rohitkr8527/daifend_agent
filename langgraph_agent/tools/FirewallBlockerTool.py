from typing import List, Dict, Set


class FirewallBlockerTool:
    """
    Blocks confirmed malicious IPs based on outputs from GeoBlockTool and IPAnalyzerTool.
    """

    def run(self, context: Dict) -> Dict:
        geo_result = context.get("GeoBlockTool", {})
        analyzer_result = context.get("IPAnalyzerTool", {})

        # Extract flagged IPs from each tool
        geo_flagged = geo_result.get("flagged_ips", [])
        analyzer_flagged = analyzer_result.get("IPAnalyzerTool", [])

        # Extract IPs from each list
        geo_ips = {entry["ip"] for entry in geo_flagged if "ip" in entry}
        analyzer_ips = {entry["ip"] for entry in analyzer_flagged if "ip" in entry}

        # Union of all unique IPs
        all_malicious_ips = geo_ips.union(analyzer_ips)

        blocked_entries = [{"ip": ip, "status": "Blocked at perimeter firewall"} for ip in sorted(all_malicious_ips)]

        return {
            "FirewallBlockerTool": blocked_entries,
            "meta": {
                "blocked_count": len(blocked_entries)
            }
        }
