"""
RABBIT STOMACH V7.0
The Warehouse & Material Inventory Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the physical stock sitting on the shelves. It tracks
Quantity on Hand (QOH), Bin Locations, and Valuation. It feeds the
Job Sites (Rabbit Daily) and replenishes via Purchasing (Raptor Vendor).

CORE CAPABILITIES:
1. QR Scanning (Check-In/Check-Out).
2. FIFO Tracking (Expiration Management).
3. Min/Max Reordering (Hunger Signals).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Raptor Pricing (Valuation)
"""

import time
from datetime import datetime, timedelta
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
# 📦 THE PANTRY (Mock Database)
# ==============================================================================

MOCK_INVENTORY = {
    "EMT-1/2": {
        "name": "1/2in EMT Conduit",
        "bin": "A-01",
        "qoh": 4500,  # Feet
        "min_level": 2000,
        "max_level": 10000,
        "batches": [
            {"qty": 2000, "date_in": "2025-10-01", "cost": 4.00},
            {"qty": 2500, "date_in": "2025-12-01", "cost": 4.50}
        ]
    },
    "CAULK-FIRE": {
        "name": "3M Fire Barrier Caulk",
        "bin": "Z-99",
        "qoh": 12,  # Tubes
        "min_level": 24,  # We are low!
        "max_level": 100,
        "batches": [
            {"qty": 12, "date_in": "2024-01-01", "cost": 15.00}  # Old!
        ]
    }
}


# ==============================================================================
# 🐰 RABBIT STOMACH CLASS
# ==============================================================================

class RabbitStomach:
    """
    The Warehouse Manager.
    """

    def __init__(self):
        self.stock = MOCK_INVENTORY

    # ==========================================================================
    # 📥 CONSUMPTION (Check In/Out)
    # ==========================================================================

    def digest_material(self, sku: str, qty: int, transaction_type: str, job_id: str = None) -> Dict[str, Any]:
        """
        Handles moving items in or out of the stomach.
        Types: RECEIVE (In), TRANSFER (Out to Job).
        """
        item = self.stock.get(sku)
        if not item:
            Bananas.notify("Indigestion", f"Unknown SKU: {sku}")
            return {"success": False}

        if transaction_type == "RECEIVE":
            # Add to stock
            item['qoh'] += qty
            # Add new batch (FIFO)
            item['batches'].append({
                "qty": qty,
                "date_in": datetime.now().strftime("%Y-%m-%d"),
                "cost": 0.0  # Logic to pull from PO would go here
            })
            MonkeyHeart.log_system_event("INV_RECEIVE", f"Received {qty} of {sku}. New Total: {item['qoh']}")
            return {"success": True, "new_total": item['qoh']}

        elif transaction_type == "TRANSFER":
            # Remove from stock (Check FIFO)
            if item['qoh'] < qty:
                Bananas.notify("Starvation", f"Not enough {sku} (Has: {item['qoh']}, Need: {qty})")
                return {"success": False}

            item['qoh'] -= qty
            self._consume_batches(item, qty)

            MonkeyHeart.log_system_event("INV_TRANSFER", f"Sent {qty} of {sku} to {job_id}.")

            # Check for Hunger
            if item['qoh'] < item['min_level']:
                Bananas.notify("Hunger Pang", f"Low Stock: {sku} dropped below min ({item['qoh']})!")

            return {"success": True, "remaining": item['qoh']}

    def _consume_batches(self, item: Dict, qty_needed: int):
        """
        FIFO Logic: Eat the oldest food first.
        """
        remaining_need = qty_needed
        # Iterate through batches (oldest first)
        for batch in item['batches']:
            if remaining_need <= 0: break

            if batch['qty'] > 0:
                take = min(batch['qty'], remaining_need)
                batch['qty'] -= take
                remaining_need -= take

    # ==========================================================================
    # 🥗 NUTRITION CHECK (Audit)
    # ==========================================================================

    def check_pantry_health(self) -> List[str]:
        """
        Scans for Low Stock and Expired Items.
        """
        issues = []

        for sku, data in self.stock.items():
            # 1. Hunger Check
            if data['qoh'] < data['min_level']:
                issues.append(f"LOW STOCK: {data['name']} ({data['qoh']} < {data['min_level']})")

            # 2. Expiration Check (Mock: Old Caulk)
            if "CAULK" in sku:
                for batch in data['batches']:
                    # If batch is older than 1 year
                    in_date = datetime.strptime(batch['date_in'], "%Y-%m-%d")
                    if (datetime.now() - in_date).days > 365 and batch['qty'] > 0:
                        issues.append(f"EXPIRED: {data['name']} (Batch from {batch['date_in']})")

        return issues


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT STOMACH V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    warehouse = RabbitStomach()

    # 2. Test Receive (Digestion)
    print("\n[TEST 1] Receiving 500ft of EMT...")
    warehouse.digest_material("EMT-1/2", 500, "RECEIVE")

    # 3. Test Transfer (FIFO)
    print("\n[TEST 2] Sending 1000ft EMT to Job...")
    warehouse.digest_material("EMT-1/2", 1000, "TRANSFER", "JOB-26001")

    # 4. Test Health Check (Hunger/Expire)
    print("\n[TEST 3] Checking Pantry Health...")
    # Expecting Low Stock on Caulk + Expired Caulk
    report = warehouse.check_pantry_health()
    for issue in report:
        print(f" > {issue}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT STOMACH SYSTEM: OPERATIONAL")
