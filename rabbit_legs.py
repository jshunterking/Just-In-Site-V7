"""
RABBIT LEGS V7.0
The Fleet & Vehicle Management Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the company's rolling assets (Vans, Trucks, Trailers).
It tracks location, maintenance health, and the inventory stored inside
each vehicle. It ensures the "Legs" of the company are always ready to run.

CORE CAPABILITIES:
1. Vehicle Telematics (Driver Scoring).
2. Rolling Stock Tracking (Van Inventory).
3. Predictive Maintenance Scheduling.

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Raptor Maps (Mileage Data)
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
# 🚐 THE GARAGE (Mock Database)
# ==============================================================================

MOCK_FLEET = [
    {
        "id": "VAN-04",
        "make": "Ford Transit 250",
        "driver": "Foreman Mike",
        "odometer": 45000,
        "last_service_date": "2025-10-01",
        "last_service_odo": 40000,
        "inventory": {"BREAKER-20A": 3, "WIRE-THHN-12": 500},
        "driver_score": 98
    },
    {
        "id": "TRUCK-01",
        "make": "Chevy Silverado 2500",
        "driver": "Billy",
        "odometer": 82000,
        "last_service_date": "2025-08-15",
        "last_service_odo": 75000,  # Overdue for service soon (7k interval)
        "inventory": {"SHOVEL": 2, "LADDER-24FT": 1},
        "driver_score": 72  # Bad driver
    }
]


# ==============================================================================
# 🐰 RABBIT LEGS CLASS
# ==============================================================================

class RabbitLegs:
    """
    The Fleet Manager.
    """

    def __init__(self):
        self.fleet = MOCK_FLEET

    # ==========================================================================
    # 🛠️ MAINTENANCE HEALTH
    # ==========================================================================

    def check_fleet_health(self) -> List[Dict]:
        """
        Scans all vehicles to see who needs an oil change.
        """
        alerts = []
        service_interval = 5000  # Miles

        for vehicle in self.fleet:
            miles_since = vehicle['odometer'] - vehicle['last_service_odo']
            remaining = service_interval - miles_since

            status = "GOOD"
            if remaining < 0:
                status = "OVERDUE"
                msg = f"{vehicle['id']} is OVERDUE by {abs(remaining)} miles!"
                alerts.append(msg)
                Bananas.notify("Maintenance Alert", msg)
            elif remaining < 500:
                status = "DUE_SOON"
                msg = f"{vehicle['id']} due for service in {remaining} miles."
                alerts.append(msg)

            MonkeyHeart.log_system_event("FLEET_CHECK", f"{vehicle['id']}: {status} (Miles Since: {miles_since})")

        return alerts

    # ==========================================================================
    # 📦 ROLLING INVENTORY
    # ==========================================================================

    def check_van_stock(self, vehicle_id: str, item_sku: str, qty_needed: int) -> bool:
        """
        Checks if a specific van has the parts we need.
        """
        vehicle = next((v for v in self.fleet if v['id'] == vehicle_id), None)
        if not vehicle: return False

        on_hand = vehicle['inventory'].get(item_sku, 0)

        if on_hand >= qty_needed:
            MonkeyHeart.log_system_event("FLEET_STOCK", f"{vehicle_id} has {on_hand} of {item_sku}. USE IT.")
            return True
        else:
            return False

    # ==========================================================================
    # 🏎️ DRIVER SAFETY
    # ==========================================================================

    def log_telematics_event(self, vehicle_id: str, event_type: str):
        """
        Logs harsh events and dings the driver's score.
        Events: HARSH_BRAKE, RAPID_ACCEL, SPEEDING.
        """
        vehicle = next((v for v in self.fleet if v['id'] == vehicle_id), None)
        if not vehicle: return

        # Penalties
        penalty = 0
        if event_type == "HARSH_BRAKE":
            penalty = 2
        elif event_type == "SPEEDING":
            penalty = 5

        vehicle['driver_score'] -= penalty

        MonkeyHeart.log_system_event("FLEET_SAFETY",
                                     f"{vehicle['driver']} ({vehicle_id}) flagged for {event_type}. Score: {vehicle['driver_score']}")

        if vehicle['driver_score'] < 80:
            Bananas.notify("Driver Warning", f"{vehicle['driver']} score dropped to {vehicle['driver_score']}!")


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT LEGS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    garage = RabbitLegs()

    # 2. Check Maintenance
    print("\n[TEST 1] Checking Fleet Health...")
    # Truck-01 is at 82k, last svc 75k. Diff 7k. Interval 5k. Overdue.
    alerts = garage.check_fleet_health()
    for a in alerts:
        print(f" > {a}")

    # 3. Check Van Inventory
    print("\n[TEST 2] Looking for 2 Breakers in VAN-04...")
    has_stock = garage.check_van_stock("VAN-04", "BREAKER-20A", 2)
    print(f" > Found in Van: {has_stock}")

    # 4. Telematics
    print("\n[TEST 3] Logging Speeding Event for TRUCK-01...")
    garage.log_telematics_event("TRUCK-01", "SPEEDING")

    print("\n" + "=" * 40)
    print("🐰 RABBIT LEGS SYSTEM: OPERATIONAL")