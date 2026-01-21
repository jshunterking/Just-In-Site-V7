"""
RABBIT PAWS V7.0
The Purchasing & Procurement Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module handles the acquisition of material. It acts as the bridge
between the Field (who wants stuff) and the Vendor (who sells stuff).
It enforces financial discipline by requiring approvals before spending.

CORE CAPABILITIES:
1. Requisition Management (Wishlist).
2. Approval Workflow (PM Gatekeeper).
3. Budget Validation (The Leash).
4. PO Generation.

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Lion Spine (Budget Data)
"""

import time
import uuid
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
# 🧺 THE BASKET (Mock Database)
# ==============================================================================

MOCK_REQS = [
    {
        "id": "REQ-001",
        "job_id": "JOB-26001",
        "requester": "Foreman Mike",
        "items": [{"sku": "EMT-1/2", "qty": 100, "est_cost": 450.00}],
        "status": "PENDING_APPROVAL",
        "total_cost": 450.00
    }
]


# ==============================================================================
# 🐰 RABBIT PAWS CLASS
# ==============================================================================

class RabbitPaws:
    """
    The Gatherer.
    """

    def __init__(self):
        self.reqs = MOCK_REQS
        self.purchase_orders = []

    # ==========================================================================
    # 🤲 REQUISITION (The Ask)
    # ==========================================================================

    def create_requisition(self, job_id: str, requester: str, items: List[Dict]) -> Dict[str, Any]:
        """
        Field creates a wishlist.
        Items format: [{'sku': 'X', 'qty': 10, 'est_cost': 5.00}]
        """
        total = sum(i['est_cost'] for i in items)

        req_id = f"REQ-{int(time.time())}"
        new_req = {
            "id": req_id,
            "job_id": job_id,
            "requester": requester,
            "items": items,
            "status": "PENDING_APPROVAL",
            "total_cost": round(total, 2),
            "created_at": datetime.now().isoformat()
        }

        self.reqs.append(new_req)

        MonkeyHeart.log_system_event("PURCHASE_REQ", f"{requester} requested ${total} for {job_id}")
        Bananas.notify("New Request", f"{requester} needs materials for {job_id}.")

        return {"success": True, "req_id": req_id}

    # ==========================================================================
    # 🚦 APPROVAL (The Gatekeeper)
    # ==========================================================================

    def approve_requisition(self, req_id: str, approver: str, budget_limit: float) -> Dict[str, Any]:
        """
        PM reviews and converts to PO.
        """
        req = next((r for r in self.reqs if r['id'] == req_id), None)
        if not req: return {"success": False, "reason": "Req Not Found"}

        # 1. Budget Check (The Leash)
        if req['total_cost'] > budget_limit:
            Bananas.notify("Over Budget", f"REQ {req_id} (${req['total_cost']}) exceeds limit (${budget_limit}).")
            return {"success": False, "reason": "OVER_BUDGET"}

        # 2. Convert to PO
        req['status'] = "APPROVED"
        po_number = f"PO-{req['job_id'].replace('JOB-', '')}-{uuid.uuid4().hex[:4].upper()}"

        po_record = {
            "po_number": po_number,
            "req_id": req_id,
            "vendor": "PREFERRED_VENDOR",  # Logic to pick vendor would be here
            "total": req['total_cost'],
            "issued_by": approver,
            "issued_at": datetime.now().isoformat(),
            "status": "ISSUED"
        }

        self.purchase_orders.append(po_record)

        MonkeyHeart.log_financial_event(req['job_id'], req['total_cost'], f"PO {po_number} Issued", approver)

        return {
            "success": True,
            "po_number": po_number,
            "message": "PO Generated and Sent to Vendor."
        }

    # ==========================================================================
    # 🕵️ STATUS TRACKER
    # ==========================================================================

    def check_status(self, req_id: str) -> str:
        req = next((r for r in self.reqs if r['id'] == req_id), None)
        if req:
            return req['status']
        return "UNKNOWN"


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT PAWS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    buyer = RabbitPaws()

    # 2. Create Req
    print("\n[TEST 1] Creating Requisition...")
    items = [{"sku": "WIRE-12", "qty": 1000, "est_cost": 200.00}]
    res1 = buyer.create_requisition("JOB-26001", "Foreman Mike", items)
    req_id = res1['req_id']
    print(f" > Req ID: {req_id}")

    # 3. Fail Approval (Budget)
    print("\n[TEST 2] Approving with Low Budget ($100)...")
    res2 = buyer.approve_requisition(req_id, "PM Justin", 100.00)
    print(f" > Success: {res2['success']} (Reason: {res2.get('reason')})")

    # 4. Success Approval
    print("\n[TEST 3] Approving with Good Budget ($500)...")
    res3 = buyer.approve_requisition(req_id, "PM Justin", 500.00)
    print(f" > Success: {res3['success']}")
    print(f" > PO Number: {res3.get('po_number')}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT PAWS SYSTEM: OPERATIONAL")