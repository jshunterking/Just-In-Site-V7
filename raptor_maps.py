"""
RAPTOR MAPS V7.0
The Geospatial & Navigation Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the eyes in the sky. It handles all location-based logic.
It validates addresses, calculates travel times for Dispatch, and
enforces Geo-Fences for Time & Attendance.

CORE CAPABILITIES:
1. Geocoding (Address -> Lat/Lon).
2. Distance Matrix (Travel Time Calculation).
3. Geo-Fencing (Is User at Job Site?).

INTEGRATIONS:
- Bananas (Error Handling)
- Monkey Heart (Logging)
- External: Google Maps API (Simulated)
"""

import math
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
# 🦕 RAPTOR MAPS CLASS
# ==============================================================================

class RaptorMaps:
    """
    The Navigator.
    """

    def __init__(self, api_key: str = "MOCK_KEY_123"):
        self.api_key = api_key
        # Earth radius in meters
        self.R = 6371000

        # ==========================================================================

    # 📍 GEOCODING (Where is it?)
    # ==========================================================================

    def get_coordinates(self, address: str) -> Dict[str, Any]:
        """
        Converts '123 Main St' to Lat/Lon.
        (Mocked response for V7.0).
        """
        MonkeyHeart.log_system_event("MAPS_GEO", f"Geocoding address: {address}")

        # Simulating API Latency
        time.sleep(0.2)

        # Mock Logic: Returns a fixed coordinate near Youngstown, OH
        # unless it's a specific known test case
        if "Taco Bell" in address:
            return {"lat": 41.1000, "lon": -80.6500, "valid": True}
        elif "Mercy" in address:
            return {"lat": 41.0995, "lon": -80.6400, "valid": True}

        # Default
        return {"lat": 41.0800, "lon": -80.6300, "valid": True}

    # ==========================================================================
    # 🚧 GEO-FENCING (Are you there?)
    # ==========================================================================

    def check_geofence(self, user_lat: float, user_lon: float,
                       site_lat: float, site_lon: float,
                       radius_meters: int = 200) -> Dict[str, Any]:
        """
        Uses Haversine formula to see if User is within Radius of Site.
        """
        # Convert to radians
        phi1 = user_lat * math.pi / 180
        phi2 = site_lat * math.pi / 180
        dphi = (site_lat - user_lat) * math.pi / 180
        dlambda = (site_lon - user_lon) * math.pi / 180

        # Haversine Math
        a = (math.sin(dphi / 2) * math.sin(dphi / 2)) + \
            (math.cos(phi1) * math.cos(phi2) * \
             math.sin(dlambda / 2) * math.sin(dlambda / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = self.R * c  # Distance in meters

        inside = distance <= radius_meters

        status_msg = "INSIDE" if inside else "OUTSIDE"
        MonkeyHeart.log_system_event("MAPS_FENCE", f"User is {int(distance)}m from target. Status: {status_msg}")

        return {
            "inside": inside,
            "distance_meters": round(distance, 1),
            "radius_limit": radius_meters
        }

    # ==========================================================================
    # 🛣️ ROUTING (How long to get there?)
    # ==========================================================================

    def get_travel_time(self, origin_lat: float, origin_lon: float,
                        dest_lat: float, dest_lon: float) -> Dict[str, Any]:
        """
        Estimates drive time.
        Mock Logic: Calculates straight line distance and assumes 45mph avg speed.
        """
        # Get raw distance
        fence_result = self.check_geofence(origin_lat, origin_lon, dest_lat, dest_lon, radius_meters=9999999)
        dist_meters = fence_result['distance_meters']
        dist_miles = dist_meters * 0.000621371

        # Mock Speed: 30mph city + 2 mins traffic penalty
        speed_mph = 30
        hours = dist_miles / speed_mph
        minutes = int(hours * 60) + 2

        return {
            "distance_miles": round(dist_miles, 1),
            "minutes": minutes,
            "traffic_condition": "LIGHT"
        }


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦕 RAPTOR MAPS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    nav = RaptorMaps()

    # 2. Test Geocoding
    print("\n[TEST 1] Geocoding 'Mercy Hospital'...")
    coords = nav.get_coordinates("Mercy Hospital, Youngstown OH")
    print(f" > Lat: {coords['lat']}, Lon: {coords['lon']}")

    # 3. Test Geo-Fence (Success)
    print("\n[TEST 2] Checking Geo-Fence (User is close)...")
    # User is 50 meters away
    # 0.00045 deg lat is roughly 50m
    user_close = {"lat": 41.1000, "lon": -80.6500}
    site = {"lat": 41.1004, "lon": -80.6500}

    fence_in = nav.check_geofence(user_close['lat'], user_close['lon'], site['lat'], site['lon'])
    print(f" > Distance: {fence_in['distance_meters']}m")
    print(f" > Status: {'✅ INSIDE' if fence_in['inside'] else '❌ OUTSIDE'}")

    # 4. Test Geo-Fence (Fail)
    print("\n[TEST 3] Checking Geo-Fence (User is far)...")
    user_far = {"lat": 41.2000, "lon": -80.6500}  # Miles away
    fence_out = nav.check_geofence(user_far['lat'], user_far['lon'], site['lat'], site['lon'])
    print(f" > Distance: {fence_out['distance_meters']}m")
    print(f" > Status: {'✅ INSIDE' if fence_out['inside'] else '❌ OUTSIDE'}")

    # 5. Test Travel Time
    print("\n[TEST 4] Calculating Travel Time...")
    route = nav.get_travel_time(41.1000, -80.6500, 41.2000, -80.6500)
    print(f" > Distance: {route['distance_miles']} miles")
    print(f" > ETA: {route['minutes']} minutes")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR MAPS SYSTEM: OPERATIONAL")