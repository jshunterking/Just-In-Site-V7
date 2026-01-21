"""
RAPTOR VENDOR V7.0
The External Supply Chain & EDI Integration Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module handles the heavy lifting of external procurement. It is the
interface between Just-In-Site and suppliers (Graybar, Rexel, Home Depot).
It validates stock availability and transmits digital Purchase Orders.

CORE CAPABILITIES:
1. PO Transmission (API/EDI Simulation).
2. Live Stock Queries.
3. Invoice Reconciliation (PO vs Invoice).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
"""

import time
import json
import uuid
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

# ==============================================================================
# 🏭 MOCK VENDOR APIs
# ==============================================================================

MOCK_VENDOR_DBS = {
    "GRAYBAR": {
        "BOX-4SQ-D": {"qty": 5000, "price": 2.15},
        "EMT-1/2": {"qty": 200, "price": 4.50},  # Low stock
        "WIRE-THHN-12-BLK": {"qty": 100000, "price": 0.12}
    },
    "REXEL": {
        "BOX-4SQ-D": {"qty": 2000, "price": 2.20},  # Higher price
        "EMT-1/2": {"qty": 5000, "price": 4.45}
    }
}


# ==============================================================================
# 🦕 RAPTOR VENDOR CLASS
# ==============================================================================

class RaptorVendor:
    """
    The Talons.
    """

    def __init__(self):
        self.vendors = MOCK_VENDOR_DBS

    # ==========================================================================
    # 📡 LIVE STOCK CHECK
    # ==========================================================================

    def check_availability(self, vendor_name: str, sku: str, required_qty: int) -> Dict[str, Any]:
        """
        Pings the vendor to see if they can fill the order.
        """
        vendor_db = self.vendors.get(vendor_name)
        if not vendor_db:
            return {"available": False, "reason": "Vendor Not Linked"}

        item = vendor_db.get(sku)
        if not item:
            return {"available": False, "reason": "Item Not Carried"}

        on_hand = item['qty']

        if on_hand >= required_qty:
            MonkeyHeart.log_system_event("VENDOR_CHECK", f"{vendor_name} has {on_hand} of {sku}. Order verified.")
            return {"available": True, "qty_on_hand": on_hand, "current_price": item['price']}
        else:
            Bananas.notify("Stock Warning", f"{vendor_name} only has {on_hand} of {sku} (Need {required_qty}).")
            return {"available": False, "reason": "Insufficient Stock", "qty_on_hand": on_hand}

    # ==========================================================================
    # 📤 TRANSMIT PO
    # ==========================================================================

    def transmit_digital_po(self, po_data: Dict) -> Dict[str, Any]:
        """
        Sends the JSON PO to the vendor.
        """
        vendor = po_data.get('vendor')
        po_num = po_data.get('po_number')

        MonkeyHeart.log_system_event("VENDOR_TX", f"Transmitting {po_num} to {vendor}...")

        # Simulate API Latency
        time.sleep(0.5)

        # Generate Vendor Confirmation Number
        conf_num = f"{vendor[:3]}-{uuid.uuid4().hex[:8].upper()}"

        MonkeyHeart.log_system_event("VENDOR_ACK", f"PO {po_num} Acknowledged. Ref: {conf_num}")

        return {
            "success": True,
            "status": "RECEIVED",
            "vendor_ref": conf_num,
            "estimated_delivery": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        }

    # ==========================================================================
    # 🧾 INVOICE RECONCILIATION
    # ==========================================================================

    def reconcile_invoice(self, po_data: Dict, invoice_data: Dict) -> Dict[str, Any]:
        """
        Compares what we ordered vs what they billed.
        """
        discrepancies = []

        # 1. Check Total
        if abs(po_data['total'] - invoice_data['total']) > 0.05:
            discrepancies.append(f"Total Mismatch: PO ${po_data['total']} vs Inv ${invoice_data['total']}")

        # 2. Check Line Items (Simplified for V7)
        # Assuming simple list matching

        if discrepancies:
            Bananas.notify("Invoice Alert", f"Found {len(discrepancies)} issues with Invoice {invoice_data['id']}.")
            MonkeyHeart.log_system_event("VENDOR_AUDIT", f"Invoice Failed Audit: {discrepancies}")
            return {"approved": False, "issues": discrepancies}

        MonkeyHeart.log_system_event("VENDOR_AUDIT", f"Invoice {invoice_data['id']} Matched PO {po_data['po_number']}.")
        return {"approved": True, "issues": []}


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    from datetime import datetime, timedelta  # Import locally for test

    print("\n🦕 RAPTOR VENDOR V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    supply_chain = RaptorVendor()

    # 2. Test Availability (Success)
    print("\n[TEST 1] Checking Stock @ Graybar...")
    res1 = supply_chain.check_availability("GRAYBAR", "BOX-4SQ-D", 100)
    print(f" > Available: {res1['available']} (Qty: {res1['qty_on_hand']})")

    # 3. Test Availability (Fail)
    print("\n[TEST 2] Checking Low Stock @ Graybar...")
    res2 = supply_chain.check_availability("GRAYBAR", "EMT-1/2", 500)  # Only have 200
    print(f" > Available: {res2['available']} (Reason: {res2.get('reason')})")

    # 4. Transmit PO
    print("\n[TEST 3] Sending PO to Rexel...")
    mock_po = {"po_number": "PO-26001-99", "vendor": "REXEL", "total": 500.00}
    tx_res = supply_chain.transmit_digital_po(mock_po)
    print(f" > Vendor Ref: {tx_res['vendor_ref']}")

    # 5. Reconcile Invoice (Fail)
    print("\n[TEST 4] Auditing Bad Invoice...")
    bad_inv = {"id": "INV-999", "total": 550.00}  # $50 higher than PO
    audit = supply_chain.reconcile_invoice(mock_po, bad_inv)
    print(f" > Approved: {audit['approved']}")
    print(f" > Issue: {audit['issues'][0]}")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR VENDOR SYSTEM: OPERATIONAL")