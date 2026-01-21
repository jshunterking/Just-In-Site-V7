"""
PANTHER MOUTH V7.0
The Invoicing & Revenue Intake Organ for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.2 (Diamond-Grade)

DESCRIPTION:
This module handles the consumption of revenue. It interacts with the customer
at the "Point of Sale." It is responsible for vocalizing the cost (Invoicing)
and consuming the payment.

CORE CAPABILITIES:
1. Flat Rate "Menu" Pricing (The Bite).
2. T&M Calculation (The Hunt).
3. Invoice Generation (Vocalization).
4. Payment Processing (Consumption).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Financial Audit)
"""

import uuid
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

# ==============================================================================
# 🍔 THE MENU (Pre-Set Bites)
# ==============================================================================

FLAT_RATE_BOOK = {
    "FR-101": {"name": "Diagnostic Fee (Standard)", "price": 89.00, "desc": "Trip charge and initial troubleshooting."},
    "FR-205": {"name": "Replace GFI Receptacle", "price": 249.00, "desc": "Includes device, plate, and testing."},
    "FR-301": {"name": "Ceiling Fan Install (Standard)", "price": 350.00,
               "desc": "Assembly and hanging on existing box."},
    "FR-401": {"name": "Panel Tune-Up", "price": 199.00, "desc": "Tighten all connections and inspect breakers."}
}

COMMERCIAL_RATES = {
    "LABOR_STD": 125.00,  # Per Hour
    "LABOR_OT": 187.50,
    "MAT_MARKUP": 1.40  # 40% Markup
}


# ==============================================================================
# 🐆 PANTHER MOUTH CLASS
# ==============================================================================

class PantherMouth:
    """
    The Revenue Consumer.
    """

    def __init__(self):
        self.menu = FLAT_RATE_BOOK
        self.rates = COMMERCIAL_RATES
        self.pending_meals = []  # Invoices waiting for payment

    # ==========================================================================
    # 🗣️ VOCALIZATION (Invoicing)
    # ==========================================================================

    def speak_flat_rate(self, ticket_id: str, codes: List[str], tech_user: str) -> Dict[str, Any]:
        """
        Generates a bill based on the Menu.
        """
        line_items = []
        total_bite = 0.0

        for code in codes:
            item = self.menu.get(code)
            if item:
                line_items.append(item)
                total_bite += item['price']

        inv_id = f"INV-{ticket_id.replace('T-', '')}-{int(time.time())}"

        invoice = {
            "id": inv_id,
            "ticket_id": ticket_id,
            "type": "FLAT_RATE",
            "items": line_items,
            "total": round(total_bite, 2),
            "created_by": tech_user,
            "status": "DRAFT",
            "date": datetime.now().isoformat()
        }
        self.pending_meals.append(invoice)

        return invoice

    def speak_time_and_material(self, ticket_id: str, hours: float, materials_cost: float, tech_user: str) -> Dict[
        str, Any]:
        """
        Calculates the hunt cost (T&M).
        """
        labor_total = hours * self.rates['LABOR_STD']
        mat_total = materials_cost * self.rates['MAT_MARKUP']
        subtotal = labor_total + mat_total

        inv_id = f"INV-{ticket_id.replace('T-', '')}-{int(time.time())}"

        invoice = {
            "id": inv_id,
            "ticket_id": ticket_id,
            "type": "T_AND_M",
            "items": [
                {"name": f"Labor ({hours} hrs @ ${self.rates['LABOR_STD']})", "price": labor_total},
                {"name": "Material (w/ Handling)", "price": mat_total}
            ],
            "total": round(subtotal, 2),
            "created_by": tech_user,
            "status": "DRAFT",
            "date": datetime.now().isoformat()
        }
        self.pending_meals.append(invoice)

        return invoice

    # ==========================================================================
    # 🥩 CONSUMPTION (Payment)
    # ==========================================================================

    def consume_payment(self, invoice_id: str, payment_method: str) -> Dict[str, Any]:
        """
        The Panther eats. Closes the invoice and logs the money.
        """
        inv = next((i for i in self.pending_meals if i['id'] == invoice_id), None)
        if not inv:
            Bananas.notify("Hunger Error", "Invoice not found. Cannot feed.")
            return {"success": False, "error": "Invoice not found"}

        inv['status'] = "PAID"
        inv['payment_method'] = payment_method
        inv['paid_at'] = datetime.now().isoformat()

        # Log to Audit Trail
        MonkeyHeart.log_financial_event(inv['ticket_id'], inv['total'], f"Feeding Complete via {payment_method}",
                                        inv['created_by'])

        return {
            "success": True,
            "message": f"Consumed ${inv['total']}. The Beast is fed.",
            "receipt_id": f"RCPT-{uuid.uuid4().hex[:6]}"
        }


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐆 PANTHER MOUTH V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    mouth = PantherMouth()

    # 2. Test Flat Rate (Residential)
    print("\n[TEST 1] Preparing Residential Meal...")
    # Diagnostic + GFI Replace
    res_inv = mouth.speak_flat_rate("T-1002", ["FR-101", "FR-205"], "Billy")
    print(f" > Total Calories (Price): ${res_inv['total']}")
    for item in res_inv['items']:
        print(f"   - {item['name']}: ${item['price']}")

    # 3. Test T&M (Commercial)
    print("\n[TEST 2] Preparing Commercial Hunt...")
    # 4 Hours labor, $100 material cost
    com_inv = mouth.speak_time_and_material("T-1001", 4.0, 100.00, "Mike")
    print(f" > Total Hunt Cost: ${com_inv['total']}")

    # 4. Pay Bill
    print("\n[TEST 3] Feeding the Beast...")
    receipt = mouth.consume_payment(com_inv['id'], "CREDIT_CARD_VISA")
    print(f" > {receipt['message']}")
    print(f" > {receipt['receipt_id']}")

    print("\n" + "=" * 40)
    print("🐆 PANTHER MOUTH SYSTEM: OPERATIONAL")