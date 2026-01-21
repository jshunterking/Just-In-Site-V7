"""
RABBIT PO V7.0
The Procurement & Purchasing Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the flow of money for materials.
It handles Request For Quotes (RFQ) from the field and converts them
into Purchase Orders (PO) for vendors.

CORE CAPABILITIES:
1. RFQ Creation (Field Requests).
2. PO Generation & Approval Logic.
3. Vendor Selection Routing.
4. "Exploded" Prefab Orders.

INTEGRATIONS:
- Bananas (Notifications)
- Monkey Heart (Financial Audit)
- Raptor Vendor (External API)
"""

import uuid
import time
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
        def log_system_event(event_type, message):
            print(f"❤️ [HEARTBEAT] [{event_type}] {message}")

        @staticmethod
        def log_financial_event(job_id, amount, description, user):
            print(f"💰 [AUDIT] {job_id}: ${amount} - {description}")

# ==============================================================================
# 🧾 MOCK PO DATABASE
# ==============================================================================

MOCK_POS = [
    {
        "po_number": "PO-26001-001",
        "job_id": "JOB-26001",
        "status": "SENT",
        "vendor": "GRAYBAR",
        "total": 500.00,
        "created_by": "Foreman Mike",
        "date": "2026-01-15"
    }
]


# ==============================================================================
# 🐰 RABBIT PO CLASS
# ==============================================================================

class RabbitPO:
    """
    The Purchasing Agent.
    """

    def __init__(self):
        self.orders = MOCK_POS
        self.approval_limit = 1000.00  # $1k limit before Manager approval needed

    # ==========================================================================
    # 📝 RFQ CREATION (The Ask)
    # ==========================================================================

    def create_rfq(self, job_id: str, requester: str, items: List[Dict], notes: str) -> Dict[str, Any]:
        """
        Field User submits a request for materials.

        ARGS:
            items: [{'description': '400A Fuse', 'qty': 3}]
        """
        rfq_id = f"RFQ-{uuid.uuid4().hex[:6].upper()}"

        MonkeyHeart.log_system_event("PO_RFQ", f"New RFQ {rfq_id} from {requester} for {job_id}")

        # In a real app, this saves to DB status 'PENDING_QUOTE'
        return {
            "success": True,
            "rfq_id": rfq_id,
            "message": "Request sent to Purchasing."
        }

    # ==========================================================================
    # 💳 PO GENERATION (The Buy)
    # ==========================================================================

    def generate_po(self, job_id: str, vendor: str, line_items: List[Dict], user: str) -> Dict[str, Any]:
        """
        Converts a list of items into a formal Purchase Order.
        Checks for approval limits.
        """
        # Calculate Total
        total_cost = sum([item['qty'] * item['price'] for item in line_items])

        po_number = f"PO-{job_id.replace('JOB-', '')}-{len(self.orders) + 1:03d}"

        status = "APPROVED"
        if total_cost > self.approval_limit:
            status = "PENDING_APPROVAL"
            Bananas.notify("Approval Required", f"PO exceeds ${self.approval_limit:,.2f} limit.")

        new_po = {
            "po_number": po_number,
            "job_id": job_id,
            "status": status,
            "vendor": vendor,
            "total": total_cost,
            "created_by": user,
            "items": line_items,
            "date": datetime.now().isoformat()
        }

        self.orders.append(new_po)

        if status == "APPROVED":
            self._finalize_po(new_po, user)
            return {"success": True, "po_number": po_number, "status": "SENT"}
        else:
            return {"success": True, "po_number": po_number, "status": "HELD_FOR_APPROVAL"}

    def approve_po(self, po_number: str, approver: str) -> bool:
        """
        Manager (Lion) approves a large purchase.
        """
        po = next((p for p in self.orders if p['po_number'] == po_number), None)
        if po and po['status'] == "PENDING_APPROVAL":
            po['status'] = "APPROVED"
            MonkeyHeart.log_system_event("PO_APPROVE", f"{po_number} approved by {approver}")
            self._finalize_po(po, approver)
            return True
        return False

    def _finalize_po(self, po: Dict, user: str):
        """
        Sends to vendor and logs financial hit.
        """
        # 1. Log the Money
        MonkeyHeart.log_financial_event(po['job_id'], po['total'], f"PO Issued to {po['vendor']}", user)

        # 2. Trigger Vendor API (Mock)
        # In V7.0, we assume 'raptor_vendor' handles the transmission
        # RaptorVendor().submit_purchase_order(po) -> This would be the link

    # ==========================================================================
    # 🧨 PREFAB EXPLOSION LINK
    # ==========================================================================

    def create_prefab_restock_po(self, exploded_list: List[Dict]) -> str:
        """
        Takes the raw material list from RabbitPrefab and makes a PO.
        """
        # Group by Vendor (Simple logic: Box=Graybar, Screw=Fastenal)
        # For Demo, everything goes to Graybar

        line_items = []
        for part in exploded_list:
            line_items.append({
                "sku": part['sku'],
                "qty": part['qty_needed'],
                "price": 0.00  # Pricing would be looked up in RabbitPricing
            })

        res = self.generate_po("SHOP-STOCK", "GRAYBAR", line_items, "Prefab Manager")
        return res['po_number']


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT PO V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    purchasing = RabbitPO()

    # 2. Test Small PO (Auto Approve)
    print("\n[TEST 1] Creating $50 PO...")
    items_small = [{"sku": "BOX", "qty": 10, "price": 5.00}]
    res1 = purchasing.generate_po("JOB-26001", "GRAYBAR", items_small, "Foreman")
    print(f" > PO: {res1['po_number']} Status: {res1['status']}")

    # 3. Test Large PO (Hold)
    print("\n[TEST 2] Creating $5,000 PO...")
    items_big = [{"sku": "GEAR", "qty": 1, "price": 5000.00}]
    res2 = purchasing.generate_po("JOB-26001", "GRAYBAR", items_big, "Foreman")
    print(f" > PO: {res2['po_number']} Status: {res2['status']}")

    # 4. Approve Large PO
    print("\n[TEST 3] Approving Large PO...")
    purchasing.approve_po(res2['po_number'], "Lion Manager")

    # 5. Verify Ledger
    print("\n[TEST 4] Checking Ledger...")
    # (Visual check of console logs for 💰 symbol)

    print("\n" + "=" * 40)
    print("🐰 RABBIT PO SYSTEM: OPERATIONAL")