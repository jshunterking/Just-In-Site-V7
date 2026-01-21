"""
RABBIT SAFETY V7.0
The Safety Compliance & Incident Management Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the physical well-being of the crew. It handles mandatory
Toolbox Talks, OSHA recording (Incident Logs), and proactive hazard reporting.
It shifts safety from "Paperwork" to "Culture."

CORE CAPABILITIES:
1. Digital Toolbox Talks (Attendance Tracking).
2. Incident & Near-Miss Reporting.
3. Stop Work Authority (Emergency Stop).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Raptor Broadcast (Emergency Notifications)
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
        def log_security_event(event_type, details, status):
            print(f"🔒 [SECURITY] [{event_type}] {status}: {details}")

# ==============================================================================
# 🛡️ THE SAFETY LOG (Mock Database)
# ==============================================================================

MOCK_TALKS = [
    {
        "id": "TBT-26001-001",
        "job_id": "JOB-26001",
        "topic": "Ladder Safety",
        "foreman": "Mike",
        "attendees": ["Billy", "Joe"],
        "date": "2026-01-15"
    }
]


# ==============================================================================
# 🐰 RABBIT SAFETY CLASS
# ==============================================================================

class RabbitSafety:
    """
    The Shield.
    """

    def __init__(self):
        self.talks = MOCK_TALKS
        self.incidents = []

    # ==========================================================================
    # 🗣️ TOOLBOX TALKS
    # ==========================================================================

    def conduct_toolbox_talk(self, job_id: str, topic: str, foreman: str, attendees: List[str]) -> Dict[str, Any]:
        """
        Logs a mandatory safety meeting.
        """
        if not attendees:
            return {"success": False, "reason": "No attendees listed."}

        tbt_id = f"TBT-{job_id.replace('JOB-', '')}-{len(self.talks) + 1:03d}"

        record = {
            "id": tbt_id,
            "job_id": job_id,
            "topic": topic,
            "foreman": foreman,
            "attendees": attendees,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        self.talks.append(record)

        MonkeyHeart.log_system_event("SAFETY_TALK", f"{foreman} led '{topic}' for {len(attendees)} people.")
        return {"success": True, "tbt_id": tbt_id}

    # ==========================================================================
    # 🩹 INCIDENT REPORTING
    # ==========================================================================

    def report_incident(self, job_id: str, reporter: str, type_code: str, description: str) -> Dict[str, Any]:
        """
        Logs a Bad Day (Injury) or a Good Catch (Near Miss).
        Types: INJURY, PROPERTY_DAMAGE, NEAR_MISS.
        """
        inc_id = f"INC-{int(time.time())}"

        record = {
            "id": inc_id,
            "job_id": job_id,
            "reporter": reporter,
            "type": type_code,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "status": "OPEN"
        }

        self.incidents.append(record)

        if type_code == "NEAR_MISS":
            Bananas.notify("Good Catch!", f"{reporter} reported a hazard: {description}. Reward Points Issued.")
            MonkeyHeart.log_system_event("SAFETY_CATCH", f"Near Miss logged by {reporter}")

        else:
            # Injury or Damage = Bad
            Bananas.notify("🚨 INCIDENT REPORT 🚨", f"{type_code} at {job_id}: {description}")
            MonkeyHeart.log_security_event("SAFETY_INCIDENT", description, "CRITICAL")

        return {"success": True, "incident_id": inc_id}

    # ==========================================================================
    # 🛑 STOP WORK AUTHORITY
    # ==========================================================================

    def trigger_stop_work(self, job_id: str, user: str, reason: str):
        """
        The Nuclear Safety Option.
        """
        msg = f"STOP WORK TRIGGERED BY {user} AT {job_id}. REASON: {reason}"

        # 1. Notify Everyone
        Bananas.notify("🛑 STOP WORK ORDER 🛑", msg)
        MonkeyHeart.log_security_event("STOP_WORK", msg, "EMERGENCY")

        # 2. Mock: Call Raptor Broadcast
        print(f" >> [BROADCAST] PUSH TO ALL DEVICES ON SITE {job_id}: {msg}")

        return {"status": "HALTED", "time": datetime.now().strftime("%H:%M")}


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT SAFETY V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    shield = RabbitSafety()

    # 2. Toolbox Talk
    print("\n[TEST 1] Logging Toolbox Talk...")
    res1 = shield.conduct_toolbox_talk("JOB-26001", "PPE Inspection", "Foreman Mike", ["Billy", "Joe", "Sam"])
    print(f" > Talk ID: {res1['tbt_id']}")

    # 3. Near Miss (Good Catch)
    print("\n[TEST 2] Reporting Near Miss...")
    res2 = shield.report_incident("JOB-26001", "Billy", "NEAR_MISS", "Extension cord with exposed copper found.")
    print(f" > Incident ID: {res2['incident_id']}")

    # 4. Stop Work
    print("\n[TEST 3] STOP WORK TRIGGER...")
    shield.trigger_stop_work("JOB-26001", "Foreman Mike", "Unshored Trench Detected")

    print("\n" + "=" * 40)
    print("🐰 RABBIT SAFETY SYSTEM: OPERATIONAL")
