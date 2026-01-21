"""
RAPTOR OUTLOOK V7.0
The Calendar & Email Integration Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module bridges the gap between the Just-In-Site ecosystem and the
corporate email/calendar server (Microsoft 365 / Exchange). It ensures
that operational schedules align with personal calendars.

CORE CAPABILITIES:
1. Availability Checking (Free/Busy/OOO).
2. Meeting Invitation Automation.
3. Critical Date Protection.

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- External: MS Graph API (Simulated)
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
# 🦅 THE CLOUD (Mock Exchange Server)
# ==============================================================================

MOCK_CALENDARS = {
    "billy@justinsite.com": [
        {"subject": "Doctor Appt", "date": "2026-01-21", "status": "OOO"},
        {"subject": "Lunch", "date": "2026-01-22", "status": "BUSY"}
    ],
    "mike@justinsite.com": [
        {"subject": "Material Run", "date": "2026-01-21", "status": "TENTATIVE"}
    ]
}


# ==============================================================================
# 🦕 RAPTOR OUTLOOK CLASS
# ==============================================================================

class RaptorOutlook:
    """
    The Sentry.
    """

    def __init__(self):
        self.calendars = MOCK_CALENDARS

    # ==========================================================================
    # 📅 AVAILABILITY CHECK
    # ==========================================================================

    def check_user_availability(self, email: str, date_str: str) -> Dict[str, Any]:
        """
        Queries the Exchange server to see if a user is free.
        """
        # 1. Look up user
        events = self.calendars.get(email, [])

        # 2. Scan for conflicts
        conflict = next((e for e in events if e['date'] == date_str), None)

        if not conflict:
            return {"available": True, "status": "FREE"}

        # 3. Analyze Conflict Severity
        status = conflict['status']
        if status == "OOO":
            MonkeyHeart.log_system_event("OUTLOOK_BLOCK", f"{email} is OOO on {date_str}: {conflict['subject']}")
            return {"available": False, "status": "OOO", "reason": conflict['subject']}
        elif status == "BUSY":
            return {"available": False, "status": "BUSY", "reason": conflict['subject']}
        elif status == "TENTATIVE":
            # We can override tentative!
            return {"available": True, "status": "TENTATIVE", "note": "Existing event is tentative."}

        return {"available": True, "status": "FREE"}

    # ==========================================================================
    # ✉️ INVITE AUTOMATION
    # ==========================================================================

    def send_calendar_invite(self, subject: str, date_str: str,
                             attendees: List[str], location: str) -> bool:
        """
        Simulates sending an .ics invite to a group.
        """
        if not attendees:
            return False

        # Mock API Call
        time.sleep(0.5)

        MonkeyHeart.log_system_event("OUTLOOK_INVITE", f"Sent '{subject}' to {len(attendees)} people for {date_str}")
        Bananas.notify("Invites Sent", f"Outlook updated for {len(attendees)} users.")

        return True

    # ==========================================================================
    # 🛡️ THE SAFETY NET (Critical Path)
    # ==========================================================================

    def validate_time_off_request(self, email: str, date_str: str, is_critical_week: bool) -> bool:
        """
        Approves or Denies vacation requests based on project status.
        """
        if is_critical_week:
            # Check role (Mock: assuming 'justin' is boss)
            if "justin" in email:
                MonkeyHeart.log_system_event("OUTLOOK_OVERRIDE", "Boss overrode Critical Path lock.")
                return True

            Bananas.notify("Request Denied", "Cannot book off during Critical Path week.")
            MonkeyHeart.log_system_event("OUTLOOK_DENY", f"Denied vacation for {email} on {date_str} (Critical Path).")
            return False

        return True


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦕 RAPTOR OUTLOOK V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    sentry = RaptorOutlook()

    # 2. Test Availability (OOO)
    print("\n[TEST 1] Checking Billy (OOO)...")
    res1 = sentry.check_user_availability("billy@justinsite.com", "2026-01-21")
    print(f" > Available: {res1['available']}")
    print(f" > Reason: {res1.get('reason')}")

    # 3. Test Availability (Tentative)
    print("\n[TEST 2] Checking Mike (Tentative)...")
    res2 = sentry.check_user_availability("mike@justinsite.com", "2026-01-21")
    print(f" > Available: {res2['available']}")
    print(f" > Note: {res2.get('note')}")

    # 4. Test Safety Net (Critical Path)
    print("\n[TEST 3] Requesting Vacation during Critical Path...")
    allowed = sentry.validate_time_off_request("billy@justinsite.com", "2026-02-01", is_critical_week=True)
    print(f" > Request Approved: {allowed}")

    # 5. Send Invites
    print("\n[TEST 4] Blasting Safety Meeting Invites...")
    sentry.send_calendar_invite("Safety Stand-Down", "2026-01-22", ["all@justinsite.com"], "Shop Floor")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR OUTLOOK SYSTEM: OPERATIONAL")
