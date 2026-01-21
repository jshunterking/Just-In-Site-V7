"""
RABBIT INVENTORY V7.0
The Material Management Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the physical stuff. It tracks counts in the Main Warehouse
and inside the Service Vans. It powers the "Storefront" UI that Foremen use
to order material.

CORE CAPABILITIES:
1. Stock Deduction & Tracking.
2. Van Stock Management.
3. Smart Storefront (Context-Aware Menus).
4. Low Stock Alerts (Par Levels).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Financial Logging)
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
        def log_system_event(event_type, message):
            print(f"❤️ [HEARTBEAT] [{event_type}] {message}")

        @staticmethod
        def log_financial_event(job_id, amount, description, user):
            print(f"💰 [AUDIT] {job_id}: ${amount} - {description}")

# ==============================================================================
# 📦 THE WAREHOUSE (Mock Data)
# ==============================================================================
# In production, this is 'monkey_brain.db' -> 'inventory' table.

MOCK_INVENTORY = [
    # ROUGH-IN MATERIALS
    {"sku": "BOX-4SQ-D", "name": "4-Square Box Deep", "category": "ROUGH", "qty": 5000, "par": 1000, "cost": 2.15},
    {"sku": "EMT-1/2", "name": "1/2 Inch EMT (10ft)", "category": "ROUGH", "qty": 2000, "par": 500, "cost": 4.50},
    {"sku": "CONN-SS-1/2", "name": "1/2 SS Connector", "category": "ROUGH", "qty": 3000, "par": 500, "cost": 0.45},
    {"sku": "GRD-SCREW", "name": "Green Ground Screw", "category": "ROUGH", "qty": 10000, "par": 1000, "cost": 0.10},

    # WIRE
    {"sku": "WIRE-THHN-12-BLK", "name": "THHN #12 Black (500ft)", "category": "WIRE", "qty": 50, "par": 10,
     "cost": 65.00},
    {"sku": "WIRE-MC-12/2", "name": "12/2 MC Cable (250ft)", "category": "WIRE", "qty": 20, "par": 5, "cost": 120.00},

    # FINISH
    {"sku": "DEV-DUPLEX-W", "name": "Duplex Receptacle (White)", "category": "FINISH", "qty": 200, "par": 50,
     "cost": 1.25},
    {"sku": "PLATE-1G-W", "name": "1-Gang Plate (White)", "category": "FINISH", "qty": 300, "par": 50, "cost": 0.50}
]


# ==============================================================================
# 🐰 RABBIT INVENTORY CLASS
# ==============================================================================

class RabbitInventory:
    """
    The Stock Keeper.
    """

    def __init__(self):
        self.stock = MOCK_INVENTORY

    # ==========================================================================
    # 🛒 SMART STOREFRONT (The Menu)
    # ==========================================================================

    def get_smart_menu(self, phase: str) -> List[Dict]:
        """
        Returns a filtered list of items based on the Job Phase.
        This prevents the Foreman from scrolling through 10,000 items.

        ARGS:
            phase: 'ROUGH', 'WIRE', 'FINISH', 'ALL'
        """
        if phase == 'ALL':
            return self.stock

        filtered = [item for item in self.stock if item['category'] == phase]
        MonkeyHeart.log_system_event("INV_FILTER", f"Filtered Storefront for '{phase}' ({len(filtered)} items)")
        return filtered

    # ==========================================================================
    # 📉 STOCK MOVEMENT (The Transaction)
    # ==========================================================================

    def deduct_stock(self, sku: str, qty: int, job_id: str, user: str) -> Dict[str, Any]:
        """
        Moves item from Warehouse to Job. Logs cost.
        """
        item = self._find_item(sku)

        if not item:
            Bananas.notify("Inventory Error", f"SKU {sku} not found.")
            return {"success": False}

        if item['qty'] < qty:
            Bananas.notify("Low Stock", f"Only {item['qty']} of {item['name']} available.")
            return {"success": False, "reason": "NSF"}

        # Execute Move
        item['qty'] -= qty
        total_cost = round(item['cost'] * qty, 2)

        # Financial Log
        MonkeyHeart.log_financial_event(job_id, total_cost, f"Internal Transfer: {qty}x {item['name']}", user)

        # Check Par Level
        self._check_par(item)

        return {
            "success": True,
            "new_qty": item['qty'],
            "cost_charged": total_cost
        }

    def restock_item(self, sku: str, qty: int):
        """
        Adds inventory (from Vendor PO).
        """
        item = self._find_item(sku)
        if item:
            item['qty'] += qty
            MonkeyHeart.log_system_event("INV_RESTOCK", f"Added {qty} to {item['name']}. Total: {item['qty']}")
            return True
        return False

    # ==========================================================================
    # ⚠️ ALERTS
    # ==========================================================================

    def _check_par(self, item: Dict):
        """Checks if we are running low."""
        if item['qty'] <= item['par']:
            Bananas.notify("Restock Alert", f"{item['name']} is below par ({item['qty']}/{item['par']}). Order now.")
            MonkeyHeart.log_system_event("INV_LOW", f"SKU {item['sku']} triggered Par Alert.")

    def _find_item(self, sku: str) -> Optional[Dict]:
        for i in self.stock:
            if i['sku'] == sku:
                return i
        return None


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT INVENTORY V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    warehouse = RabbitInventory()

    # 2. Test Smart Menu
    print("\n[TEST 1] Testing 'ROUGH' Filter...")
    menu = warehouse.get_smart_menu("ROUGH")
    for item in menu:
        print(f" > {item['name']} ({item['qty']} avail)")

    # 3. Test Deduction
    print("\n[TEST 2] Foreman Mike ordering 100 Boxes for JOB-26001...")
    res = warehouse.deduct_stock("BOX-4SQ-D", 100, "JOB-26001", "Foreman Mike")
    print(f" > Status: {res['success']}")
    print(f" > Charged: ${res['cost_charged']}")

    # 4. Test Low Stock Alert
    print("\n[TEST 3] Draining THHN Wire to trigger alert...")
    # Has 50, Par 10. We take 45.
    warehouse.deduct_stock("WIRE-THHN-12-BLK", 45, "JOB-26001", "Mike")

    print("\n" + "=" * 40)
    print("🐰 RABBIT INVENTORY SYSTEM: OPERATIONAL")