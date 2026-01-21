"""
RABBIT DAILY V7.0
The Daily Reporting & Field Journal Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the official record of the job site. It tracks progress,
delays, weather, and manpower. It is the primary shield against
"He said, She said" disputes.

CORE CAPABILITIES:
1. Auto-Weather Logging.
2. Issue Escalation (Blocker Detection).
3. Evidence Enforcement (Photo Required).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Raptor Broadcast (Escalation)
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
# 📓 THE JOURNAL (Mock Database)
# ==============================================================================

MOCK_REPORTS = [
    {
        "id": "RPT-26001-001",
        "job_id": "JOB-26001",
        "date": "2026-01-19",
        "foreman": "Mike",
        "weather": "Snow, 28F",
        "notes": "Rough-in continues on 2nd floor.",
        "blockers": [],
        "status": "SUBMITTED"
    }
]


# ==============================================================================
# 🐰 RABBIT DAILY CLASS
# ==============================================================================

class RabbitDaily:
    """
    The Field Journal.
    """

    def __init__(self):
        self.reports = MOCK_REPORTS

    # ==========================================================================
    # 📝 REPORT GENERATION
    # ==========================================================================

    def start_daily_report(self, job_id: str, foreman: str) -> Dict[str, Any]:
        """
        Initializes the daily log and pulls weather.
        """
        # 1. Auto-Weather (Mock)
        weather = "Clear, 45F"  # In real app, call RaptorAPI here

        rpt_id = f"RPT-{job_id.replace('JOB-', '')}-{datetime.now().strftime('%Y%m%d')}"

        report = {
            "id": rpt_id,
            "job_id": job_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "foreman": foreman,
            "weather": weather,
            "notes": "",
            "blockers": [],
            "photos": [],
            "status": "DRAFT"
        }

        self.reports.append(report)
        MonkeyHeart.log_system_event("DAILY_START", f"{foreman} started report for {job_id}")

        return report

    # ==========================================================================
    # 🚩 ISSUE LOGGING
    # ==========================================================================

    def log_issue(self, report_id: str, issue_text: str, is_blocker: bool, has_photo: bool) -> Dict[str, Any]:
        """
        Adds a problem to the report.
        """
        report = next((r for r in self.reports if r['id'] == report_id), None)
        if not report: return {"success": False}

        # 1. Evidence Enforcement
        if is_blocker and not has_photo:
            return {
                "success": False,
                "reason": "PHOTO_REQUIRED",
                "message": "You cannot flag a Blocker without photo evidence."
            }

        entry = {
            "text": issue_text,
            "is_blocker": is_blocker,
            "has_photo": has_photo,
            "time": datetime.now().strftime("%H:%M")
        }

        report['blockers'].append(entry)

        # 2. Immediate Escalation
        if is_blocker:
            Bananas.notify("BLOCKER ALERT", f"{report['job_id']}: {issue_text}")
            MonkeyHeart.log_system_event("DAILY_BLOCKER", f"Escalated: {issue_text}")

        return {"success": True, "message": "Issue Logged"}

    # ==========================================================================
    # 🔒 SUBMISSION
    # ==========================================================================

    def submit_report(self, report_id: str) -> bool:
        """
        Finalizes the journal for the day.
        """
        report = next((r for r in self.reports if r['id'] == report_id), None)
        if not report: return False

        report['status'] = "SUBMITTED"

        # Check for empty notes
        if len(report['notes']) < 10 and not report['blockers']:
            Bananas.notify("Lazy Reporting", f"{report['foreman']} submitted a very short report.")

        MonkeyHeart.log_system_event("DAILY_SUBMIT", f"Report {report_id} locked by {report['foreman']}")
        return True


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT DAILY V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    journal = RabbitDaily()

    # 2. Start Report
    print("\n[TEST 1] Starting Day at Mercy Hospital...")
    rpt = journal.start_daily_report("JOB-26001", "Foreman Mike")
    print(f" > Weather Auto-Logged: {rpt['weather']}")

    # 3. Log Blocker (Fail - No Photo)
    print("\n[TEST 2] Logging 'Wall not ready' (No Photo)...")
    fail = journal.log_issue(rpt['id'], "GC didn't finish framing", is_blocker=True, has_photo=False)
    print(f" > Success: {fail['success']} (Reason: {fail.get('reason')})")

    # 4. Log Blocker (Success)
    print("\n[TEST 3] Logging 'Wall not ready' (With Photo)...")
    success = journal.log_issue(rpt['id'], "GC didn't finish framing", is_blocker=True, has_photo=True)
    print(f" > Success: {success['success']}")

    # 5. Submit
    print("\n[TEST 4] Submitting Report...")
    journal.submit_report(rpt['id'])
    print(f" > Status: {rpt['status']}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT DAILY SYSTEM: OPERATIONAL")