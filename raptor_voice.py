"""
RAPTOR VOICE V8.1 | INVENTORY INTELLIGENCE
"""
import re


class RaptorVoice:
    def parse_inventory_command(self, transcript: str):
        t = transcript.lower()
        qty = float(re.search(r'(\d+)', t).group(1)) if re.search(r'(\d+)', t) else 0

        # Extract material between quantity and 'from'
        mat_match = re.search(r'\d+\s*(?:feet|ft|pcs)?\s*(?:of)?\s*(.*?)\s+from', t)
        material = mat_match.group(1).strip().upper() if mat_match else "UNKNOWN"

        # Extract Jobs
        locations = re.findall(r'(?:from|to)\s+([\w-]+)', t)
        source = locations[0].upper() if len(locations) > 0 else "UNKNOWN"
        dest = locations[1].upper() if len(locations) > 1 else "SHOP STOCK"

        return {"material": material, "qty": qty, "from": source, "to": dest}