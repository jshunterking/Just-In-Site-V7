"""
RABBIT CHANGE ORDER V7.0
The Scope Management & Change Control Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the "Extra Work." It tracks deviations from the original
contract, calculates the cost impact (Labor + Material + Markup), and
generates formal Proposals (COPs) for the client to sign.

CORE CAPABILITIES:
1. COP Generation & Versioning.
2. Automatic Markup Calculation (O&P).
3. RFI Linking (Audit Trail).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Rabbit RFIs (Source of Scope Change)
"""

import time
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
        def report_collision(error, context):
            print(f"🍌 [BANANAS] SLIP in {context}: {error}")

        @staticmethod
        def notify(title, message):
            print(f"🍌 [BANANAS] TOAST: {title} - {message}")

# ==============================================================================
# ❤️ IMPORT MONKEY HEART (The Logger)
# ==============================================================================
try:
    from monkey_heart import MonkeyHeart
except ImportError:
    class MonkeyHeart:
        @staticmethod
        def log_financial_event(job_id, amount, description, user):
            print(f"💰 [AUDIT] {job_id}: ${amount} - {description}")

        @staticmethod
        def log_system_event(event_type, message):
            print(f"❤️ [HEARTBEAT] [{event_type}] {message}")

# ==============================================================================
# 📝 THE CHANGE LOG (Mock Database)
# ==============================================================================

MOCK_COPS = [
    {
        "id": "COP-26001-001",
        "job_id": "JOB-26001",
        "title": "Added Outlets in Lobby",
        "rfi_link": "N/A",
        "status": "APPROVED",
        "total": 1250.00
    }
]


# ==============================================================================
# 🐰 RABBIT CHANGE ORDER CLASS
# ==============================================================================

class RabbitChangeOrder:
    """
    The Negotiator.
    """

    def __init__(self):
        self.cops = MOCK_COPS
        self.rates = {
            "labor_hr": 85.00,
            "overhead_pct": 0.10,  # 10%
            "profit_pct": 0.05  # 5%
        }

    # ==========================================================================
    # 💰 PROPOSAL GENERATION
    # ==========================================================================

    def create_proposal(self, job_id: str, title: str, labor_hrs: float, material_cost: float, rfi_id: str = None) -> \
    Dict[str, Any]:
        """
        Calculates the sell price and generates a COP.
        """
        # 1. Base Costs
        labor_total = labor_hrs * self.rates['labor_hr']
        subtotal = labor_total + material_cost

        # 2. Markups (The Profit Protection)
        overhead = subtotal * self.rates['overhead_pct']
        profit = (subtotal + overhead) * self.rates['profit_pct']
        grand_total = subtotal + overhead + profit

        cop_id = f"COP-{job_id.replace('JOB-', '')}-{len(self.cops) + 1:03d}"

        new_cop = {
            "id": cop_id,
            "job_id": job_id,
            "title": title,
            "rfi_link": rfi_id if rfi_id else "N/A",
            "breakdown": {
                "labor": labor_total,
                "material": material_cost,
                "overhead": overhead,
                "profit": profit
            },
            "total": round(grand_total, 2),
            "status": "DRAFT",
            "created_at": datetime.now().isoformat()
        }

        self.cops.append(new_cop)

        MonkeyHeart.log_system_event("COP_CREATE", f"Drafted {cop_id}: ${grand_total:.2f}")

        return {"success": True, "cop_id": cop_id, "total": round(grand_total, 2)}

    # ==========================================================================
    # 🤝 APPROVAL
    # ==========================================================================

    def process_approval(self, cop_id: str, approved_by: str) -> bool:
        """
        Client signed the paper. We can now bill for it.
        """
        cop = next((c for c in self.cops if c['id'] == cop_id), None)
        if not cop: return False

        cop['status'] = "APPROVED"
        cop['approved_by'] = approved_by
        cop['approved_date'] = datetime.now().isoformat()

        # Log Revenue Event
        MonkeyHeart.log_financial_event(cop['job_id'], cop['total'], f"Change Order {cop_id} APPROVED", approved_by)
        Bananas.notify("New Revenue", f"COP {cop_id} Approved! Value: ${cop['total']}")

        return True

    # ==========================================================================
    # 🔗 RFI LINKING
    # ==========================================================================

    def link_rfi(self, cop_id: str, rfi_id: str):
        """
        Connects the question (RFI) to the cost (COP).
        """
        cop = next((c for c in self.cops if c['id'] == cop_id), None)
        if cop:
            cop['rfi_link'] = rfi_id
            MonkeyHeart.log_system_event("COP_LINK", f"Linked {cop_id} to {rfi_id}")


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT CHANGE ORDER V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    negotiator = RabbitChangeOrder()

    # 2. Draft COP (From RFI)
    print("\n[TEST 1] Drafting COP for RFI-26001-001...")
    # 10 Hours, $500 Material
    res1 = negotiator.create_proposal("JOB-26001", "RFI-001 Impact", 10.0, 500.00, "RFI-26001-001")
    print(f" > COP ID: {res1['cop_id']}")
    print(f" > Grand Total: ${res1['total']}")

    # 3. Approve
    print("\n[TEST 2] Approving COP...")
    negotiator.process_approval(res1['cop_id'], "GC Project Manager")

    # 4. Verify Status
    cop = negotiator.cops[-1]
    print(f" > Final Status: {cop['status']}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT CHANGE ORDER SYSTEM: OPERATIONAL")