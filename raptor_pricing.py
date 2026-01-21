"""
RAPTOR PRICING V7.0
The Material Pricing & Commodity Intelligence Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the cost of goods. It separates "Inventory Counts" (Rabbit)
from "Dollar Values" (Raptor). It ensures that Jaguar (Estimating) and
Rabbit PO (Purchasing) are using accurate, up-to-date pricing.

CORE CAPABILITIES:
1. Dynamic SKU Pricing.
2. Commodity Adjustments (Copper Adder).
3. Volume Discount Logic (Tier 1 vs Tier 3).
4. Vendor Price File Sync (Simulation).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
"""

import time
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
# 📈 THE MARKET DATA (Mock Database)
# ==============================================================================

MOCK_PRICING_DB = {
    # Commodities (Subject to Fluctuation)
    "WIRE-THHN-12-BLK": {"base_price": 0.12, "is_commodity": True, "category": "WIRE"},  # Per Foot
    "EMT-1/2": {"base_price": 4.50, "is_commodity": True, "category": "PIPE"},  # Per 10ft Stick

    # Static Items
    "BOX-4SQ-D": {"base_price": 2.15, "is_commodity": False, "category": "ROUGH"},
    "DEV-DUPLEX-W": {"base_price": 1.25, "is_commodity": False, "category": "FINISH"},

    # Expensive Gear
    "PANEL-200A": {"base_price": 250.00, "is_commodity": False, "category": "GEAR"}
}


# ==============================================================================
# 🦕 RAPTOR PRICING CLASS
# ==============================================================================

class RaptorPricing:
    """
    The Ticker.
    """

    def __init__(self):
        self.prices = MOCK_PRICING_DB
        self.copper_adder_pct = 0.0  # Percentage increase (e.g., 5.0 for 5%)

    # ==========================================================================
    # 💲 PRICE LOOKUP
    # ==========================================================================

    def get_price(self, sku: str, qty: int = 1) -> float:
        """
        Calculates the Unit Price based on Quantity and Commodities.
        """
        item = self.prices.get(sku)
        if not item:
            MonkeyHeart.log_system_event("PRICE_MISS", f"SKU {sku} has no pricing data.")
            return 0.00

        unit_price = item['base_price']

        # 1. Apply Commodity Adder (if applicable)
        if item['is_commodity'] and self.copper_adder_pct > 0:
            adder = unit_price * (self.copper_adder_pct / 100)
            unit_price += adder

        # 2. Apply Volume Discount
        # Mock Logic: >1000 items gets 10% off
        if qty >= 1000:
            unit_price = unit_price * 0.90
        elif qty >= 100:
            unit_price = unit_price * 0.95

        return round(unit_price, 4)

    # ==========================================================================
    # 📉 MARKET ADJUSTMENTS
    # ==========================================================================

    def update_copper_basis(self, new_adder_pct: float):
        """
        Updates the global wire/pipe multiplier.
        """
        old_val = self.copper_adder_pct
        self.copper_adder_pct = new_adder_pct

        MonkeyHeart.log_system_event("PRICE_ADJ", f"Copper Adder adjusted: {old_val}% -> {new_adder_pct}%")
        Bananas.notify("Market Update", f"Wire prices updated by {new_adder_pct}%.")

    def sync_vendor_file(self, vendor_name: str, csv_data: str) -> Dict[str, Any]:
        """
        Simulates parsing a price sheet update from Graybar/Rexel.
        """
        # Mocking the parsing logic
        updated_count = 0
        lines = csv_data.strip().split('\n')

        for line in lines:
            # Assume Format: SKU,PRICE
            if "," in line:
                sku, price = line.split(',')
                if sku in self.prices:
                    self.prices[sku]['base_price'] = float(price)
                    updated_count += 1

        MonkeyHeart.log_system_event("PRICE_SYNC", f"Updated {updated_count} items from {vendor_name}")
        return {"success": True, "updated": updated_count}


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦕 RAPTOR PRICING V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    ticker = RaptorPricing()

    # 2. Test Standard Price
    print("\n[TEST 1] Checking Box Price (Static)...")
    p1 = ticker.get_price("BOX-4SQ-D", 1)
    print(f" > Price (Qty 1): ${p1}")
    p2 = ticker.get_price("BOX-4SQ-D", 1000)
    print(f" > Price (Qty 1000 - Volume Discount): ${p2}")

    # 3. Test Commodity Adjustment
    print("\n[TEST 2] Checking Wire Price (Commodity)...")
    base_wire = ticker.get_price("WIRE-THHN-12-BLK", 1)
    print(f" > Base Wire Price: ${base_wire}")

    print(" >> MARKET SURGE: Copper up 10%!")
    ticker.update_copper_basis(10.0)

    surge_wire = ticker.get_price("WIRE-THHN-12-BLK", 1)
    print(f" > Adjusted Wire Price: ${surge_wire}")

    # 4. Test Vendor Sync
    print("\n[TEST 3] Syncing 'Graybar.csv'...")
    csv_mock = "BOX-4SQ-D,2.50\nPANEL-200A,260.00"
    res = ticker.sync_vendor_file("Graybar", csv_mock)
    print(f" > Updates Processed: {res['updated']}")
    print(f" > New Box Price: ${ticker.get_price('BOX-4SQ-D', 1)}")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR PRICING SYSTEM: OPERATIONAL")