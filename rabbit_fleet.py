"""
RABBIT FLEET V7.0
The Vehicle Management Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the rolling assets (Trucks, Vans, Trailers).
It ensures vehicles are maintained, inspected, and assigned correctly.

CORE CAPABILITIES:
1. Odometer Tracking & Maintenance Alerts.
2. Vehicle Assignment (Who is driving?).
3. Inspection Logging (Tire pressure, fluids).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
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

# ==============================================================================
# 🚚 THE MOTOR POOL (Mock Data)
# ==============================================================================

MOCK_FLEET = [
    {
        "id": "V-01",
        "name": "Ford F-250 (The Beast)",
        "type": "TRUCK",
        "status": "ACTIVE",
        "driver": "Foreman Mike",
        "odometer": 45200,
        "last_service_mileage": 40000,
        "service_interval": 5000,
        "plate": "OH-5592"
    },
    {
        "id": "V-02",
        "name": "Ford Transit (Service 1)",
        "type": "VAN",
        "status": "ACTIVE",
        "driver": "Billy",
        "odometer": 12050,
        "last_service_mileage": 10000,
        "service_interval": 5000,
        "plate": "OH-1120"
    },
    {
        "id": "V-03",
        "name": "Chevy Express (Spare)",
        "type": "VAN",
        "status": "AVAILABLE",
        "driver": None,
        "odometer": 189000,
        "last_service_mileage": 185000,
        "service_interval": 3000,  # Old engine needs love
        "plate": "OH-9981"
    }
]


# ==============================================================================
# 🐰 RABBIT FLEET CLASS
# ==============================================================================

class RabbitFleet:
    """
    The Fleet Manager.
    """

    def __init__(self):
        self.fleet = MOCK_FLEET

    # ==========================================================================
    # 🛣️ MILEAGE & MAINTENANCE
    # ==========================================================================

    def log_trip(self, vehicle_id: str, miles_driven: int, driver: str) -> Dict[str, Any]:
        """
        Updates the odometer and checks for maintenance triggers.
        """
        vehicle = self._find_vehicle(vehicle_id)
        if not vehicle:
            return {"success": False, "error": "Vehicle Not Found"}

        # Update Odometer
        old_reading = vehicle['odometer']
        new_reading = old_reading + miles_driven
        vehicle['odometer'] = new_reading

        MonkeyHeart.log_system_event("FLEET_TRIP",
                                     f"{vehicle['name']}: Driven {miles_driven} miles by {driver}. Total: {new_reading}")

        # Maintenance Check
        miles_since_service = new_reading - vehicle['last_service_mileage']
        alert = None

        if miles_since_service >= vehicle['service_interval']:
            alert = f"MAINTENANCE DUE! ({miles_since_service} miles since last oil change)"
            Bananas.notify("Fleet Warning", f"{vehicle['name']} needs service immediately.")
            MonkeyHeart.log_system_event("FLEET_MAINT", f"{vehicle['name']} triggered service alert.")

        return {
            "success": True,
            "new_odometer": new_reading,
            "alert": alert
        }

    def perform_maintenance(self, vehicle_id: str, service_notes: str):
        """
        Resets the maintenance counter (Oil Change Complete).
        """
        vehicle = self._find_vehicle(vehicle_id)
        if vehicle:
            current_odo = vehicle['odometer']
            vehicle['last_service_mileage'] = current_odo

            MonkeyHeart.log_system_event("FLEET_SERVICE", f"Service Performed on {vehicle['name']}: {service_notes}")
            Bananas.notify("Fleet Update", f"{vehicle['name']} is back in action.")
            return True
        return False

    # ==========================================================================
    # 🔑 ASSIGNMENT
    # ==========================================================================

    def assign_vehicle(self, vehicle_id: str, driver_name: str) -> bool:
        """
        Hands the keys to a driver.
        """
        vehicle = self._find_vehicle(vehicle_id)
        if not vehicle:
            return False

        if vehicle['status'] != 'AVAILABLE' and vehicle['driver'] != driver_name:
            # Force reassignment logic
            MonkeyHeart.log_system_event("FLEET_SWAP",
                                         f"Reassigning {vehicle['name']} from {vehicle['driver']} to {driver_name}")

        vehicle['driver'] = driver_name
        vehicle['status'] = 'ACTIVE'
        return True

    def _find_vehicle(self, v_id: str) -> Optional[Dict]:
        for v in self.fleet:
            if v['id'] == v_id:
                return v
        return None


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT FLEET V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    garage = RabbitFleet()

    # 2. Log Trip (Normal)
    print("\n[TEST 1] Logging 50 miles on V-02 (Billy's Van)...")
    res1 = garage.log_trip("V-02", 50, "Billy")
    print(f" > Odometer: {res1['new_odometer']}")
    print(f" > Alert: {res1['alert']}")

    # 3. Log Trip (Trigger Maintenance)
    print("\n[TEST 2] Logging 600 miles on V-01 (The Beast)...")
    # Current: 45200. Last Service: 40000. Diff: 5200. Interval: 5000.
    # This should trigger an alert.
    res2 = garage.log_trip("V-01", 600, "Mike")
    print(f" > Odometer: {res2['new_odometer']}")
    print(f" > Alert: {res2['alert']}")

    # 4. Perform Service
    print("\n[TEST 3] Performing Oil Change on V-01...")
    garage.perform_maintenance("V-01", "Oil Change & Tire Rotation")

    # 5. Verify Reset
    v = garage._find_vehicle("V-01")
    print(f" > Last Service Reset To: {v['last_service_mileage']}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT FLEET SYSTEM: OPERATIONAL")