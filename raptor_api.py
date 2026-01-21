"""
RAPTOR API V7.0
The Universal Connector for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module handles generic API connections that don't fit into specific
categories (like Vendor or Maps). It is responsible for environmental context
(Weather) and external messaging (Webhooks).

CORE CAPABILITIES:
1. Weather Fetching (For Daily Logs).
2. Traffic Estimation (For Dispatch).
3. External Notifications (Slack/Discord Webhooks).

INTEGRATIONS:
- Bananas (Error Handling)
- Monkey Heart (Logging)
"""

import time
import json
import random
import requests
from datetime import datetime
from typing import Dict, Optional, Any

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
# 🦖 RAPTOR API CLASS
# ==============================================================================

class RaptorAPI:
    """
    The General Purpose Interface.

    ATTRIBUTES:
        use_mock_data (bool): If True, returns simulated weather/traffic.
    """

    def __init__(self, use_mock_data: bool = True):
        self.use_mock_data = use_mock_data

        # Hardcoded Weather Codes (WMO) for simulation
        self.weather_codes = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Fog",
            51: "Light Drizzle",
            61: "Rain",
            71: "Snow",
            95: "Thunderstorm"
        }

    # ==========================================================================
    # 🌦️ WEATHER ENGINE (For Daily Logs)
    # ==========================================================================

    def get_site_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetches current weather for a specific GPS location.
        Used by Foremen (Silverbacks) to auto-fill Daily Reports.
        """
        MonkeyHeart.log_system_event("API_WEATHER", f"Fetching weather for {lat}, {lon}...")

        if self.use_mock_data:
            return self._mock_weather_response()

        try:
            # Using Open-Meteo (Free, No Key required)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                current = data.get("current_weather", {})
                w_code = current.get("weathercode", 0)
                condition = self.weather_codes.get(w_code, "Unknown")

                return {
                    "temp_f": round((current.get("temperature", 0) * 9 / 5) + 32, 1),  # Convert C to F
                    "condition": condition,
                    "wind_speed": current.get("windspeed", 0),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                raise Exception(f"API Error {response.status_code}")

        except Exception as e:
            Bananas.report_collision(e, "Weather Fetch")
            return self._mock_weather_response(is_fallback=True)

    def _mock_weather_response(self, is_fallback=False) -> Dict[str, Any]:
        """
        Simulates Youngstown, Ohio weather.
        """
        sim_condition = random.choice(["Clear Sky", "Overcast", "Light Drizzle", "Snow"])
        sim_temp = random.randint(20, 85)  # Ohio fluctuates wildly

        if is_fallback:
            MonkeyHeart.log_system_event("API_WARN", "Using Fallback Weather Data.")

        return {
            "temp_f": sim_temp,
            "condition": sim_condition,
            "wind_speed": random.randint(5, 20),
            "timestamp": datetime.now().isoformat(),
            "note": "SIMULATED DATA"
        }

    # ==========================================================================
    # 🚦 TRAFFIC ENGINE (For Dispatch)
    # ==========================================================================

    def estimate_drive_time(self, start_coords: tuple, end_coords: tuple) -> Dict[str, Any]:
        """
        Calculates ETA between two points.
        """
        # In a real app, we'd use Google Routes API or OSRM.
        # Here we use "Crow Flight" distance + Mock Traffic Factor.

        dist_miles = self._calc_distance_miles(start_coords, end_coords)

        # Assume average speed of 45 MPH in city/mix
        base_hours = dist_miles / 45.0

        # Traffic Factor (Random 1.0 to 1.5 multiplier)
        traffic_multiplier = random.uniform(1.0, 1.4)

        total_minutes = int((base_hours * traffic_multiplier) * 60)

        traffic_status = "CLEAR"
        if traffic_multiplier > 1.25:
            traffic_status = "HEAVY"
        elif traffic_multiplier > 1.1:
            traffic_status = "MODERATE"

        return {
            "distance_miles": round(dist_miles, 1),
            "eta_minutes": total_minutes,
            "traffic_condition": traffic_status
        }

    def _calc_distance_miles(self, start, end):
        """
        Simple Haversine approximation for drive estimates.
        """
        from math import radians, cos, sin, asin, sqrt
        lon1, lat1, lon2, lat2 = map(radians, [start[1], start[0], end[1], end[0]])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 3956  # Radius of Earth in miles
        return c * r

    # ==========================================================================
    # 📡 WEBHOOK BLASTER (The Broadcast)
    # ==========================================================================

    def send_victory_toast(self, job_name: str, value: int):
        """
        Sends a message to external platforms (Slack/Discord) when a job is WON.
        """
        # Mock URL - in production this would be in a config file
        webhook_url = "https://discord.com/api/webhooks/mock_url"

        payload = {
            "username": "Just-In-Site Overlord",
            "content": f"🚀 **VICTORY SECURED!**\nJob: {job_name}\nValue: ${value:,}\nGood hunting, team."
        }

        MonkeyHeart.log_system_event("API_WEBHOOK", f"Broadcasting Victory: {job_name}")

        # In mock mode, we just log it.
        # requests.post(webhook_url, json=payload)
        print(f" >> [EXTERNAL API] POST {webhook_url}: {json.dumps(payload)}")


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦖 RAPTOR API V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    api = RaptorAPI(use_mock_data=True)  # Set False to test Open-Meteo if you have internet

    # 2. Test Weather
    print("\n[TEST 1] Fetching Weather for Shop (Youngstown)...")
    weather = api.get_site_weather(41.1000, -80.6500)
    print(f" > Condition: {weather['condition']}")
    print(f" > Temp: {weather['temp_f']}°F")

    # 3. Test Traffic
    print("\n[TEST 2] Estimating Drive to Cleveland...")
    drive = api.estimate_drive_time((41.1000, -80.6500), (41.4993, -81.6944))
    print(f" > Distance: {drive['distance_miles']} miles")
    print(f" > ETA: {drive['eta_minutes']} minutes ({drive['traffic_condition']})")

    # 4. Test Webhook
    print("\n[TEST 3] Sending Victory Toast...")
    api.send_victory_toast("Mercy Hospital", 1500000)

    print("\n" + "=" * 40)
    print("🦕 RAPTOR API SYSTEM: OPERATIONAL")