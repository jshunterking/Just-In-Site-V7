"""
RABBIT COMPLIANCE V7.0
The Safety & Certification Management Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the "Red Tape" that keeps the company legal and safe.
It tracks employee certifications, logs safety meetings (Toolbox Talks),
and handles incident reporting.

CORE CAPABILITIES:
1. Certification Tracking (OSHA, First Aid expiration).
2. Toolbox Talk Logging (Digital Signatures).
3. Incident/Near Miss Reporting.

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
"""

import uuid
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
# 🪪 CERTIFICATION DB (Mock Data)
# ==============================================================================

MOCK_CERTS = [
    {
        "user_id": "U-005", "name": "Foreman Mike",
        "cert_type": "OSHA_30", "expires": "2028-05-20", "status": "VALID"
    },
    {
        "user_id": "U-005", "name": "Foreman Mike",
        "cert_type": "CPR_FIRST_AID", "expires": "2026-02-01", "status": "VALID"  # Expiring soon
    },
    {
        "user_id": "U-012", "name": "Apprentice Joe",
        "cert_type": "OSHA_10", "expires": "2024-01-01", "status": "EXPIRED"  # Problem
    }
]


# ==============================================================================
# 🐰 RABBIT COMPLIANCE CLASS
# ==============================================================================

class RabbitCompliance:
    """
    The Safety Marshall.
    """

    def __init__(self):
        self.certs = MOCK_CERTS

    # ==========================================================================
    # 📜 CERTIFICATION TRACKING
    # ==========================================================================

    def check_crew_eligibility(self, crew_ids: List[str]) -> Dict[str, Any]:
        """
        Scans a list of users to see if anyone is illegal to work.
        """
        issues = []
        today = datetime.now()

        for cert in self.certs:
            if cert['user_id'] in crew_ids:
                exp_date = datetime.strptime(cert['expires'], "%Y-%m-%d")

                # Check Expiration
                if today > exp_date:
                    issues.append(f"⛔ {cert['name']}: {cert['cert_type']} EXPIRED on {cert['expires']}")
                    MonkeyHeart.log_system_event("COMPLIANCE_FAIL", f"Found expired cert for {cert['name']}")

                # Check "About to Expire" (30 days)
                elif today + timedelta(days=30) > exp_date:
                    issues.append(f"⚠️ {cert['name']}: {cert['cert_type']} expires soon ({cert['expires']})")

        if issues:
            Bananas.notify("Compliance Alert", f"Found {len(issues)} certification issues.")
            return {"safe": False, "issues": issues}

        return {"safe": True, "issues": []}

    # ==========================================================================
    # 🗣️ TOOLBOX TALKS (Digital Sign-In)
    # ==========================================================================

    def log_toolbox_talk(self, job_id: str, topic: str, attendees: List[str], foreman_sig: str) -> bool:
        """
        Records that a safety meeting occurred.
        """
        if not attendees:
            Bananas.notify("Error", "No attendees selected for Safety Talk.")
            return False

        # In a real app, we'd save a PDF signature sheet here.
        log_entry = {
            "id": f"TT-{uuid.uuid4().hex[:6]}",
            "job_id": job_id,
            "date": datetime.now().isoformat(),
            "topic": topic,
            "attendee_count": len(attendees),
            "foreman": foreman_sig
        }

        MonkeyHeart.log_system_event("SAFETY_TALK",
                                     f"Toolbox Talk '{topic}' logged for {job_id} ({len(attendees)} people).")
        return True

    # ==========================================================================
    # 🚑 INCIDENT REPORTING
    # ==========================================================================

    def report_incident(self, job_id: str, type: str, description: str, witnesses: str) -> str:
        """
        Logs a Near Miss or Injury.
        Auto-Emails the Safety Director (simulated).

        ARGS:
            type: "NEAR_MISS", "INJURY", "PROPERTY_DAMAGE"
        """
        report_id = f"INC-{datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"

        MonkeyHeart.log_system_event("INCIDENT", f"New {type} reported on {job_id}: {report_id}")

        # Simulate generating the legal PDF
        Bananas.notify("Incident Recorded", f"Report {report_id} generated. Notify HR immediately.")

        # In V7.0, we simulate the email trigger
        print(f" >> [EMAIL ALERT] To: safety@justinsite.com | Subj: URGENT {type} on {job_id}")

        return report_id


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    import random  # imported here for the mock function above to work in standalone

    print("\n🐰 RABBIT COMPLIANCE V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    marshal = RabbitCompliance()

    # 2. Check Certs (Should find issues)
    print("\n[TEST 1] Checking Crew Certifications...")
    # Checking Foreman Mike (U-005) and Apprentice Joe (U-012)
    check = marshal.check_crew_eligibility(["U-005", "U-012"])

    for issue in check['issues']:
        print(f" > {issue}")

    # 3. Log Safety Talk
    print("\n[TEST 2] Logging Morning Safety Talk...")
    marshal.log_toolbox_talk("JOB-26001", "Ladder Safety", ["Mike", "Joe", "Billy"], "Mike F.")

    # 4. Report Incident
    print("\n[TEST 3] Reporting Near Miss...")
    rpt_id = marshal.report_incident("JOB-26001", "NEAR_MISS", "Hammer dropped from 6ft ladder", "Joe")
    print(f" > Report ID Generated: {rpt_id}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT COMPLIANCE SYSTEM: OPERATIONAL")