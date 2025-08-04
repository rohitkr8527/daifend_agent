from tools.tool_interface import ToolInterface

class GeoBlockTool(ToolInterface):
    """
    Blocks traffic from IPs originating in known high-risk countries.
    """

    def __init__(self, blacklist=None):
        # Default blacklist of high-risk countries
        self.blacklist = blacklist or {"Russia", "North Korea", "Iran", "China", "Syria"}

    def run(self, context: dict) -> dict:
        logs = context.get("logs", [])
        flagged = []

        for entry in logs:
            ip = entry.get("src_ip")
            geo = entry.get("geo_location", "")
            country = geo.split(",")[-1].strip() if geo else ""

            if country in self.blacklist:
                flagged.append({
                    "ip": ip,
                    "geo_location": geo,
                    "action": f"Block traffic from {country}"
                })

        return {
            "GeoBlockTool": flagged,
            "meta": {
                "blacklist_used": list(self.blacklist),
                "flagged_count": len(flagged)
            }
        }
