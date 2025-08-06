from typing import Dict, List, Set


class CDNActivatorTool:
    """
    Simulates rerouting legitimate traffic through a CDN/scrubbing center to absorb potential DDoS load.
    It excludes IPs already flagged by GeoBlocker or IPAnalyzer.
    """

    def run(self, context: Dict) -> Dict:
        logs = context.get("logs", [])
        geo_flagged_ips = self._extract_flagged_ips(context.get("GeoBlockTool", {}))
        analyzer_flagged_ips = self._extract_flagged_ips(context.get("IPAnalyzerTool", {}))

        all_malicious_ips = geo_flagged_ips.union(analyzer_flagged_ips)
        rerouted_ips = self._reroute_legitimate_ips(logs, all_malicious_ips)

        return {
            "CDNActivatorTool": rerouted_ips,
            "meta": {
                "malicious_ips_excluded": len(all_malicious_ips),
                "rerouted_count": len(rerouted_ips)
            }
        }

    def _extract_flagged_ips(self, tool_output: Dict) -> Set[str]:
        ips = set()
        for item in tool_output.get("flagged_ips", []):
            if isinstance(item, dict):
                ip = item.get("ip")
                if ip:
                    ips.add(ip)
        return ips

    def _reroute_legitimate_ips(self, logs: List[Dict], malicious_ips: Set[str]) -> List[Dict]:
        rerouted = []
        for entry in logs:
            ip = entry.get("src_ip")
            if ip and ip not in malicious_ips:
                rerouted.append({
                    "ip": ip,
                    "status": "Rerouted through CDN for DDoS resilience"
                })
        return rerouted
