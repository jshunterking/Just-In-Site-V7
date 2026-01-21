"""
JAGUAR HEART V7.0
The Estimating & Bidding Vital Organ for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.2 (Diamond-Grade)

DESCRIPTION:
This module is the pumping mechanism of the Pre-Construction department.
It circulates cost data through the system. It takes raw inputs (Assemblies),
oxygenates them with Labor Rates, and pumps out a Proposal.

CORE CAPABILITIES:
1. Assembly-Based Circulation (1 Count = Many Parts).
2. Labor Pressure Calc (Base Rate + Burden + Difficulty).
3. Vitals Check (Recap: Overhead, Profit, Tax).
4. Proposal Generation.

INTEGRATIONS:
- Bananas (Error Handling)
- Monkey Heart (System Logging)
- Raptor Pricing (Material Costs)
"""

import uuid
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

# ==============================================================================
# 🍌 IMPORT BANANAS (The Shield)
# ==============================================================================
try:
    from bananas import Bananas
except ImportError:
    class Bananas:
        @staticmethod
        def notify(title, message):
            print(f"🍌 [BANANAS] TOAST: {title} - {message}")

# ==============================================================================
# ❤️ IMPORT MONKEY HEART (The System Logger)
# ==============================================================================
try:
    from monkey_heart import MonkeyHeart
except ImportError:
    class MonkeyHeart:
        @staticmethod
        def log_system_event(event_type, message):
            print(f"❤️ [HEARTBEAT] [{event_type}] {message}")

# ==============================================================================
# ⚡ THE ASSEMBLY LIBRARY (Mock Data)
# ==============================================================================
# In production, this pulls from 'monkey_brain.db'.

MOCK_ASSEMBLIES = {
    "ASM-REC-20A": {
        "name": "20A Duplex Receptacle Complete",
        "description": "Box, device, plate, pigtail, 15ft pipe/wire",
        "material_cost": 12.50,  # Aggregate cost of parts
        "labor_hours": 0.50,  # 30 mins to install
        "category": "DEVICES"
    },
    "ASM-LIGHT-2x4": {
        "name": "2x4 LED Troffer Complete",
        "description": "Fixture, seismic wire, whip, connection",
        "material_cost": 65.00,
        "labor_hours": 0.75,
        "category": "LIGHTING"
    },
    "ASM-SW-1P": {
        "name": "Single Pole Switch Complete",
        "description": "Box, switch, plate, pigtail, 15ft pipe/wire",
        "material_cost": 9.25,
        "labor_hours": 0.45,
        "category": "DEVICES"
    }
}


# ==============================================================================
# 🐆 JAGUAR HEART CLASS
# ==============================================================================

class JaguarHeart:
    """
    The Bid Builder.

    ATTRIBUTES:
        base_labor_rate (float): Hourly wage (e.g., $35).
        labor_burden (float): Taxes/Insurance multiplier (e.g., 1.4).
    """

    def __init__(self, base_labor_rate: float = 35.00, labor_burden: float = 1.45):
        self.labor_rate = base_labor_rate
        self.burden = labor_burden
        self.burdened_rate = round(base_labor_rate * labor_burden, 2)

        # Temporary storage for the active bid
        self.current_bid = {
            "id": None,
            "name": None,
            "items": [],
            "difficulty_factor": 1.0
        }

    # ==========================================================================
    # 📝 CIRCULATION (Adding Items)
    # ==========================================================================

    def start_new_bid(self, project_name: str, difficulty: str = "NORMAL"):
        """
        Initializes a blank estimate.
        """
        # Determine Difficulty Multiplier (The Blood Pressure)
        factor = 1.0
        if difficulty == "HIGH_CEILINGS":
            factor = 1.2
        elif difficulty == "CONFINED_SPACE":
            factor = 1.5
        elif difficulty == "OCCUPIED_PREMISES":
            factor = 1.3

        self.current_bid = {
            "id": f"EST-{uuid.uuid4().hex[:6].upper()}",
            "name": project_name,
            "items": [],
            "difficulty_factor": factor
        }

        MonkeyHeart.log_system_event("JAGUAR_PUMP", f"Started Estimate for {project_name} (Factor: {factor}x)")
        return self.current_bid['id']

    def pump_assembly(self, assembly_sku: str, qty: int) -> bool:
        """
        Adds a count to the bid.
        """
        assembly = MOCK_ASSEMBLIES.get(assembly_sku)
        if not assembly:
            Bananas.notify("Clot Detected", f"Assembly {assembly_sku} not found.")
            return False

        line_item = {
            "sku": assembly_sku,
            "name": assembly['name'],
            "qty": qty,
            "unit_mat_cost": assembly['material_cost'],
            "unit_labor_hours": assembly['labor_hours'],
            "total_mat_cost": round(assembly['material_cost'] * qty, 2),
            "total_labor_hours": round(assembly['labor_hours'] * qty, 2)
        }

        self.current_bid['items'].append(line_item)
        return True

    # ==========================================================================
    # 🧮 VITALS CHECK (The Recap)
    # ==========================================================================

    def check_vitals(self, overhead_pct: float = 10.0, profit_pct: float = 15.0) -> Dict[str, Any]:
        """
        Crunches the numbers to find the Sell Price.
        """
        items = self.current_bid['items']
        diff_factor = self.current_bid['difficulty_factor']

        # 1. Sum Raw Totals
        total_mat = sum(item['total_mat_cost'] for item in items)
        base_labor_hours = sum(item['total_labor_hours'] for item in items)

        # 2. Apply Difficulty to Labor
        adjusted_labor_hours = base_labor_hours * diff_factor
        total_labor_cost = adjusted_labor_hours * self.burdened_rate

        raw_cost = total_mat + total_labor_cost

        # 3. Calculate Markups
        overhead_amt = raw_cost * (overhead_pct / 100)
        break_even = raw_cost + overhead_amt

        profit_amt = break_even * (profit_pct / 100)
        sell_price = break_even + profit_amt

        return {
            "estimate_id": self.current_bid['id'],
            "project": self.current_bid['name'],
            "material_total": round(total_mat, 2),
            "labor_hours_base": round(base_labor_hours, 2),
            "labor_hours_adj": round(adjusted_labor_hours, 2),
            "labor_cost_total": round(total_labor_cost, 2),
            "raw_cost": round(raw_cost, 2),
            "overhead_amt": round(overhead_amt, 2),
            "profit_amt": round(profit_amt, 2),
            "sell_price": round(sell_price, 2),
            "margin_pct": round((profit_amt / sell_price) * 100, 1) if sell_price > 0 else 0
        }

    # ==========================================================================
    # 📄 PROPOSAL GENERATOR
    # ==========================================================================

    def generate_proposal_text(self, recap: Dict) -> str:
        """
        Creates the text for the client letter.
        """
        return f"""
        PROPOSAL FOR: {recap['project']}
        --------------------------------------------------
        SCOPE OF WORK:
        Furnish and install electrical systems as estimated.
        Includes {recap['labor_hours_adj']} man-hours of labor.

        EXCLUSIONS:
        - Overtime
        - Utility Company Fees
        - Painting or Patching

        TOTAL PRICE: ${recap['sell_price']:,.2f}
        --------------------------------------------------
        Authorized Signature: __________________________
        """


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐆 JAGUAR HEART V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    # Rate: $35/hr * 1.45 burden = $50.75/hr cost
    heart = JaguarHeart(base_labor_rate=35.00, labor_burden=1.45)

    # 2. Start Bid (Hard Job)
    print("\n[TEST 1] Starting Bid: 'High Ceiling Warehouse'...")
    heart.start_new_bid("Warehouse Reno", difficulty="HIGH_CEILINGS")

    # 3. Add Items
    print("\n[TEST 2] Pumping Assemblies...")
    heart.pump_assembly("ASM-LIGHT-2x4", 100)  # 100 Lights
    heart.pump_assembly("ASM-SW-1P", 10)  # 10 Switches

    # 4. Calculate Recap
    print("\n[TEST 3] Checking Vitals...")
    recap = heart.check_vitals(overhead_pct=10, profit_pct=15)

    print(f" > Material: ${recap['material_total']:,.2f}")
    print(f" > Labor Hrs: {recap['labor_hours_adj']} (Includes 1.2x Difficulty)")
    print(f" > Raw Cost: ${recap['raw_cost']:,.2f}")
    print(f" > SELL PRICE: ${recap['sell_price']:,.2f}")

    # 5. Proposal
    print("\n[TEST 4] Proposal Preview...")
    print(heart.generate_proposal_text(recap))

    print("\n" + "=" * 40)
    print("🐆 JAGUAR HEART SYSTEM: OPERATIONAL")