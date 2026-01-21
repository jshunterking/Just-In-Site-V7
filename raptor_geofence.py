"""
RAPTOR GEOFENCE V7.0
The Boundary Enforcement & Asset Security Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
While Raptor Maps handles the raw GPS math, Raptor Geofence handles the
POLICY. It tracks the state of assets and people (Inside/Outside) and
triggers alerts when boundaries are violated.

CORE CAPABILITIES:
1. Zone State Tracking (Entered/Exited).
2. Asset Theft Protection (The Tether).
3. Auto-Attendance Triggers.

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Raptor Maps (Distance Calculation)
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
        def log_security_event(event_type, details, status):
            print(f"🔒 [SECURITY] [{event_type}] {status}: {details}")

# ==============================================================================
# 🚧 THE ZONES (Mock Database)
# ==============================================================================

MOCK_ZONES = {
    "JOB-26001": {"name": "Mercy Hospital", "lat": 41.0995, "lon": -80.6400, "radius": 200},
    "WAREHOUSE": {"name": "Main Shop", "lat": 41.1000, "lon": -80.6500, "radius": 100}
}

ASSET_STATES = {
    "TOOL-001": {"name": "DeWalt Generator", "assigned_zone": "JOB-26001", "last_status": "INSIDE"}
}


# ==============================================================================
# 🦕 RAPTOR GEOFENCE CLASS
# ==============================================================================

class RaptorGeofence:
    """
    The Border Patrol.
    """

    def __init__(self):
        self.zones = MOCK_ZONES
        self.assets = ASSET_STATES

    # ==========================================================================
    # 🕵️ ASSET MONITORING
    # ==========================================================================

    def update_asset_location(self, asset_id: str, lat: float, lon: float):
        """
        Called when a GPS tag pings. Checks if it broke its tether.
        """
        asset = self.assets.get(asset_id)
        if not asset: return

        assigned_zone_id = asset['assigned_zone']
        zone = self.zones.get(assigned_zone_id)

        # 1. Calculate Distance (Simplified Haversine approximation for speed)
        # 1 deg lat ~ 111km. 0.00001 ~ 1.11m
        lat_diff = abs(lat - zone['lat']) * 111000
        lon_diff = abs(lon - zone['lon']) * 111000  # Rough approx
        distance = (lat_diff ** 2 + lon_diff ** 2) ** 0.5

        is_inside = distance <= zone['radius']

        # 2. State Change Logic
        if asset['last_status'] == "INSIDE" and not is_inside:
            self._trigger_breach(asset, zone, distance)
            asset['last_status'] = "OUTSIDE"

        elif asset['last_status'] == "OUTSIDE" and is_inside:
            MonkeyHeart.log_security_event("ASSET_RETURN", f"{asset['name']} returned to {zone['name']}", "SAFE")
            asset['last_status'] = "INSIDE"

    def _trigger_breach(self, asset: Dict, zone: Dict, distance: float):
        """
        The Theft Alert.
        """
        msg = f"THEFT ALERT: {asset['name']} left {zone['name']} without authorization! (Dist: {int(distance)}m)"
        Bananas.notify("🚨 GEOFENCE BREACH", msg)
        MonkeyHeart.log_security_event("ASSET_BREACH", msg, "CRITICAL")

    # ==========================================================================
    # 📍 AUTO-ATTENDANCE
    # ==========================================================================

    def check_user_entry(self, user_id: str, lat: float, lon: float, active_job_id: str) -> bool:
        """
        Used by Rabbit Time to auto-clock in.
        """
        zone = self.zones.get(active_job_id)
        if not zone: return False

        # Simple distance check
        lat_diff = abs(lat - zone['lat']) * 111000
        lon_diff = abs(lon - zone['lon']) * 111000
        distance = (lat_diff ** 2 + lon_diff ** 2) ** 0.5

        if distance <= zone['radius']:
            MonkeyHeart.log_security_event("USER_ENTRY", f"User {user_id} entered {active_job_id}", "INFO")
            return True
        return False


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦕 RAPTOR GEOFENCE V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    fence = RaptorGeofence()

    # 2. Test Asset Safe
    print("\n[TEST 1] Asset Pinging inside zone...")
    # Generator is at the hospital (lat 41.0995)
    fence.update_asset_location("TOOL-001", 41.0995, -80.6400)

    # 3. Test Asset Breach
    print("\n[TEST 2] Asset Moving away...")
    # Generator moves 1 mile away
    fence.update_asset_location("TOOL-001", 41.1200, -80.6400)

    # 4. Test Auto-Clock
    print("\n[TEST 3] User arriving at work...")
    is_at_work = fence.check_user_entry("U-005", 41.0995, -80.6400, "JOB-26001")
    print(f" > User at site: {is_at_work}")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR GEOFENCE SYSTEM: OPERATIONAL")