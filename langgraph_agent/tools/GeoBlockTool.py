from typing import List, Dict, Optional, Set


class GeoBlockTool:
    """
    flags IPs based on geolocation originating from blacklisted countries.
    """

    def __init__(self, blacklist: Optional[Set[str]] = None):
        self.blacklist = blacklist or {"Russia", "North Korea", "Iran", "China", "Syria"}

    def run(self, context: Dict) -> Dict:
        logs = context.get("logs", [])
        flagged_ips = self._find_blacklisted_ips(logs)

        return {
            "flagged_ips": flagged_ips,
            "meta": {
                "blacklist_used": sorted(self.blacklist),
                "flagged_count": len(flagged_ips)
            }
        }

    def _find_blacklisted_ips(self, logs: List[Dict]) -> List[Dict]:
        """
        Returns a list of logs where the source country is in the blacklist.
        """
        flagged = []

        for entry in logs:
            ip = entry.get("src_ip")
            country = self._extract_country(entry.get("geo_location"))

            if ip and country in self.blacklist:
                flagged.append({
                    "ip": ip,
                    "geo_location": entry.get("geo_location", ""),
                    "action": f"Block traffic from {country}"
                })

        return flagged

    @staticmethod
    def _extract_country(geo: Optional[str]) -> str:
        """
        Extracts the country from a geo_location string like "City, Country".
        """
        if not geo or "," not in geo:
            return ""
        return geo.split(",")[-1].strip()
