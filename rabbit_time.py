"""
RABBIT TIME V7.0
The Time & Attendance Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module handles the heartbeat of labor. It captures start/stop times,
enforces location presence (Geo-Clock), and assigns labor costs to
specific project phases (Cost Codes).

CORE CAPABILITIES:
1. GPS-Gated Clocking (No cheating).
2. Cost Code Allocation (Rough vs Finish).
3. Overtime Prediction & Alerting.

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Raptor Geofence (Location Validation)
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
# ⏱️ THE TIMESHEET (Mock Database)
# ==============================================================================

MOCK_TIMESHEETS = [
    {
        "id": "TS-001", "user": "Billy", "week_start": "2026-01-19",
        "entries": [
            {"date": "2026-01-19", "hours": 10.0, "code": "ROUGH-IN", "job": "JOB-26001"},
            {"date": "2026-01-20", "hours": 10.0, "code": "ROUGH-IN", "job": "JOB-26001"},
            {"date": "2026-01-21", "hours": 10.0, "code": "ROUGH-IN", "job": "JOB-26001"}
        ]
        # Billy has 30 hours by Wednesday. He is in danger of OT.
    }
]


# ==============================================================================
# 🐰 RABBIT TIME CLASS
# ==============================================================================

class RabbitTime:
    """
    The Clock.
    """

    def __init__(self):
        self.sheets = MOCK_TIMESHEETS
        self.active_clocks = {}  # {user_id: start_time}

    # ==========================================================================
    # 📍 GEO-CLOCKING
    # ==========================================================================

    def clock_in(self, user_id: str, job_id: str, lat: float, lon: float) -> Dict[str, Any]:
        """
        Attempts to start the meter. Fails if outside the fence.
        """
        # 1. Simulate Raptor Geofence Check
        # In real code: RaptorGeofence.check_user_entry(user_id, lat, lon, job_id)
        # Mock Logic: If Lat is 0, we assume 'Test Fail'
        is_inside = True if lat != 0 else False

        if not is_inside:
            Bananas.notify("Clock Rejected", "You are not at the job site.")
            return {"success": False, "reason": "GEOFENCE_FAIL"}

        self.active_clocks[user_id] = {
            "job": job_id,
            "start": datetime.now(),
            "lat_in": lat
        }

        MonkeyHeart.log_system_event("TIME_IN", f"{user_id} clocked in at {job_id}")
        return {"success": True, "start_time": datetime.now().strftime("%H:%M")}

    def clock_out(self, user_id: str, cost_code: str) -> Dict[str, Any]:
        """
        Stops the meter and logs the hours.
        """
        session = self.active_clocks.get(user_id)
        if not session:
            return {"success": False, "reason": "NO_ACTIVE_CLOCK"}

        start_time = session['start']
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 3600  # Hours

        # Round to nearest 0.25
        duration = round(duration * 4) / 4

        # Log to sheet (Mock)
        MonkeyHeart.log_system_event("TIME_OUT", f"{user_id} clocked out. Duration: {duration} hrs ({cost_code})")

        # Clean up
        del self.active_clocks[user_id]

        # Trigger OT Check
        self._check_overtime_risk(user_id, duration)

        return {"success": True, "hours": duration}

    # ==========================================================================
    # ⚠️ OVERTIME WATCHDOG
    # ==========================================================================

    def _check_overtime_risk(self, user_id: str, new_hours: float):
        """
        Calculates total weekly hours. If > 40, screams.
        """
        # Mock summing logic
        current_total = 0
        user_sheet = next((s for s in self.sheets if s['user'] == user_id), None)

        if user_sheet:
            current_total = sum(e['hours'] for e in user_sheet['entries'])

        total = current_total + new_hours

        if total > 40:
            Bananas.notify("OVERTIME ALERT", f"{user_id} has hit {total} hours this week!")
        elif total > 35:
            Bananas.notify("OT Warning", f"{user_id} is at {total} hours. Manage their time.")


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT TIME V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    clock = RabbitTime()

    # 2. Test Geo-Block
    print("\n[TEST 1] Clocking in from 'Home' (Lat 0)...")
    fail = clock.clock_in("Billy", "JOB-26001", 0, 0)
    print(f" > Success: {fail['success']} (Reason: {fail.get('reason')})")

    # 3. Test Valid Clock In
    print("\n[TEST 2] Clocking in from Site...")
    success = clock.clock_in("Billy", "JOB-26001", 41.0995, -80.6400)
    print(f" > Started: {success.get('start_time')}")

    # 4. Simulate Work (Sleep) & Clock Out
    print("\n[TEST 3] Working...")
    time.sleep(0.1)  # Simulate time passing
    out = clock.clock_out("Billy", "TRIM-OUT")
    print(f" > Logged: {out['hours']} hours")

    # 5. Test OT Watchdog
    # Billy already had 30 hours in mock data.
    # If we add a mock entry of 8 hours, he hits 38 (Warning)
    print("\n[TEST 4] Triggering OT Warning...")
    clock._check_overtime_risk("Billy", 8.0)

    print("\n" + "=" * 40)
    print("🐰 RABBIT TIME SYSTEM: OPERATIONAL")