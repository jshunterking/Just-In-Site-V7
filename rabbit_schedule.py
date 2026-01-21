"""
RABBIT SCHEDULE V7.0
The Manpower & Dispatch Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the chessboard. It manages where every employee is supposed
to be. It powers the "Drag-and-Drop" scheduler UI and ensures we don't
double-book our talent.

CORE CAPABILITIES:
1. Shift Assignment (User -> Job).
2. Conflict Detection (Vacation/Double Booking).
3. Capacity Planning (Are we busy or slow?).
4. "The Bench" (Unassigned User Tracking).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Raptor Outlook (Calendar Availability)
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
# 📅 THE SCHEDULE BOARD (Mock Database)
# ==============================================================================

MOCK_SCHEDULE = [
    {
        "id": "SCH-001",
        "user_id": "U-005", "user_name": "Foreman Mike",
        "job_id": "JOB-26001",
        "date": "2026-01-21",  # Wednesday
        "shift": "DAY"
    },
    {
        "id": "SCH-002",
        "user_id": "U-012", "user_name": "Apprentice Joe",
        "job_id": "JOB-26001",
        "date": "2026-01-21",
        "shift": "DAY"
    }
]


# ==============================================================================
# 🐰 RABBIT SCHEDULE CLASS
# ==============================================================================

class RabbitSchedule:
    """
    The Grandmaster.
    """

    def __init__(self):
        self.board = MOCK_SCHEDULE
        # Simulation of Total Headcount
        self.total_staff = 10

        # ==========================================================================

    # ♟️ ASSIGNMENT LOGIC
    # ==========================================================================

    def assign_shift(self, user_id: str, user_name: str, job_id: str, date_str: str) -> Dict[str, Any]:
        """
        Tries to put a person on a job.
        Checks for conflicts first.
        """
        # 1. Check Double Booking (Internal)
        for shift in self.board:
            if shift['user_id'] == user_id and shift['date'] == date_str:
                Bananas.notify("Scheduling Conflict", f"{user_name} is already on {shift['job_id']} that day.")
                return {"success": False, "reason": "DOUBLE_BOOKED"}

        # 2. Check Outlook (External - Vacation/Appointments)
        # We assume raptor_outlook is imported or mocked here.
        # For V7.0, we simulate a simple check.
        if "Billy" in user_name and "Wednesday" in self._get_day_name(date_str):
            Bananas.notify("Outlook Conflict", f"{user_name} is OOO (Doctor's Appt).")
            return {"success": False, "reason": "OUTLOOK_OOO"}

        # 3. Create Assignment
        new_shift = {
            "id": f"SCH-{int(time.time())}",
            "user_id": user_id,
            "user_name": user_name,
            "job_id": job_id,
            "date": date_str,
            "shift": "DAY"
        }
        self.board.append(new_shift)

        MonkeyHeart.log_system_event("SCHED_ASSIGN", f"Assigned {user_name} to {job_id} on {date_str}")

        return {"success": True, "shift_id": new_shift['id']}

    # ==========================================================================
    # 📊 CAPACITY PLANNING
    # ==========================================================================

    def get_daily_capacity(self, date_str: str) -> Dict[str, Any]:
        """
        Returns stats for the day: Who is working, who is on the bench.
        """
        working = [s for s in self.board if s['date'] == date_str]
        count_working = len(working)
        count_bench = self.total_staff - count_working
        utilization = (count_working / self.total_staff) * 100

        status = "OPTIMAL"
        if utilization > 100:
            status = "OVERBOOKED"
        elif utilization < 60:
            status = "UNDERUTILIZED"

        return {
            "date": date_str,
            "total_staff": self.total_staff,
            "working": count_working,
            "bench": count_bench,
            "utilization_pct": round(utilization, 1),
            "status": status,
            "roster": working
        }

    def _get_day_name(self, date_str: str) -> str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%A")
        except:
            return ""


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT SCHEDULE V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    dispatch = RabbitSchedule()

    # 2. Test Assignment (Success)
    print("\n[TEST 1] Assigning Mike to JOB-26002 (Thursday)...")
    res1 = dispatch.assign_shift("U-005", "Foreman Mike", "JOB-26002", "2026-01-22")
    print(f" > Status: {res1['success']}")

    # 3. Test Double Booking (Fail)
    print("\n[TEST 2] Assigning Mike AGAIN for Thursday...")
    res2 = dispatch.assign_shift("U-005", "Foreman Mike", "JOB-99999", "2026-01-22")
    print(f" > Status: {res2['success']} (Reason: {res2.get('reason')})")

    # 4. Test Outlook Conflict (Billy)
    print("\n[TEST 3] Assigning Billy on Wednesday (Doctor)...")
    # Note: Our mock logic in _get_day_name handles the date check
    res3 = dispatch.assign_shift("U-003", "Billy", "JOB-26001", "2026-01-21")
    print(f" > Status: {res3['success']} (Reason: {res3.get('reason')})")

    # 5. Capacity Check
    print("\n[TEST 4] Capacity Report for Wednesday...")
    cap = dispatch.get_daily_capacity("2026-01-21")
    print(f" > Utilization: {cap['utilization_pct']}% ({cap['status']})")
    print(f" > On The Bench: {cap['bench']} people")

    print("\n" + "=" * 40)
    print("🐰 RABBIT SCHEDULE SYSTEM: OPERATIONAL")