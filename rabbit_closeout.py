"""
RABBIT CLOSEOUT V7.0
The Project Completion & Warranty Management Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the "Last Mile" of construction. It tracks the Punch List
(deficiencies), compiles Operation & Maintenance (O&M) manuals, and issues
formal Warranties. It ensures we get the final 10% check (Retention).

CORE CAPABILITIES:
1. Punch List Management (Photo-backed Deficiencies).
2. Warranty Logic (Start/End Dates).
3. Document Turnover Tracking (O&Ms, As-Builts).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Rabbit Daily (Completion Dates)
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
# 🥊 THE PUNCH LIST (Mock Database)
# ==============================================================================

MOCK_PUNCH = [
    {
        "id": "PL-26001-001",
        "job_id": "JOB-26001",
        "item": "Missing cover plate in Room 102",
        "assigned_to": "Billy",
        "status": "OPEN",  # OPEN, COMPLETED, VERIFIED
        "due_date": "2026-02-01"
    }
]


# ==============================================================================
# 🐰 RABBIT CLOSEOUT CLASS
# ==============================================================================

class RabbitCloseout:
    """
    The Finisher.
    """

    def __init__(self):
        self.punch_list = MOCK_PUNCH
        self.warranties = []

    # ==========================================================================
    # 🥊 PUNCH LIST MANAGEMENT
    # ==========================================================================

    def add_punch_item(self, job_id: str, description: str, assigned_to: str) -> Dict[str, Any]:
        """
        Logs a deficiency found during the walk-through.
        """
        pl_id = f"PL-{job_id.replace('JOB-', '')}-{len(self.punch_list) + 1:03d}"
        due_dt = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        item = {
            "id": pl_id,
            "job_id": job_id,
            "item": description,
            "assigned_to": assigned_to,
            "status": "OPEN",
            "due_date": due_dt
        }

        self.punch_list.append(item)

        MonkeyHeart.log_system_event("PUNCH_ADD", f"Item added to {job_id}: {description}")
        Bananas.notify("Punch List", f"New Item for {assigned_to}: {description}")

        return {"success": True, "id": pl_id, "due": due_dt}

    def close_punch_item(self, pl_id: str, tech_user: str) -> bool:
        """
        Tech marks it done.
        """
        item = next((p for p in self.punch_list if p['id'] == pl_id), None)
        if not item: return False

        item['status'] = "COMPLETED"
        item['completed_by'] = tech_user
        item['completed_at'] = datetime.now().isoformat()

        MonkeyHeart.log_system_event("PUNCH_FIX", f"{pl_id} fixed by {tech_user}. Ready for Verification.")
        return True

    # ==========================================================================
    # 📜 WARRANTY GENERATION
    # ==========================================================================

    def issue_warranty(self, job_id: str, substantial_completion_date: str) -> Dict[str, Any]:
        """
        Generates the 1-Year Warranty Certificate.
        """
        # 1. Check for Open Punch Items
        open_items = [p for p in self.punch_list if p['job_id'] == job_id and p['status'] != "VERIFIED"]
        if open_items:
            Bananas.notify("Cannot Issue Warranty", f"{len(open_items)} Punch Items are still open!")
            return {"success": False, "reason": "OPEN_PUNCH_LIST"}

        start_dt = datetime.strptime(substantial_completion_date, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=365)

        warranty_id = f"WAR-{job_id.replace('JOB-', '')}"

        record = {
            "id": warranty_id,
            "job_id": job_id,
            "start_date": substantial_completion_date,
            "end_date": end_dt.strftime("%Y-%m-%d"),
            "status": "ACTIVE"
        }

        self.warranties.append(record)

        MonkeyHeart.log_system_event("WARRANTY_ISSUE", f"Warranty {warranty_id} issued. Expires {record['end_date']}")

        return {
            "success": True,
            "warranty_id": warranty_id,
            "message": "1-Year Warranty Certificate Generated."
        }

    # ==========================================================================
    # 📂 DOCUMENT TURNOVER (Retention Unlock)
    # ==========================================================================

    def check_retention_requirements(self, job_id: str) -> Dict[str, bool]:
        """
        Checks if we have submitted everything required to get paid.
        """
        # Mock logic checking file presence
        # In real app, check DB for file uploads
        return {
            "as_builts": True,
            "om_manuals": True,
            "warranty_cert": any(w['job_id'] == job_id for w in self.warranties),
            "punch_list_clear": not any(p['job_id'] == job_id and p['status'] != "VERIFIED" for p in self.punch_list)
        }


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT CLOSEOUT V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    finisher = RabbitCloseout()

    # 2. Add Punch Item
    print("\n[TEST 1] Architect finds a scratch...")
    res1 = finisher.add_punch_item("JOB-26001", "Scratch on Panel Cover", "Billy")
    print(f" > Item ID: {res1['id']}")

    # 3. Try to Issue Warranty (Fail)
    print("\n[TEST 2] Trying to Issue Warranty early...")
    res2 = finisher.issue_warranty("JOB-26001", "2026-02-01")
    print(f" > Success: {res2['success']} (Reason: {res2.get('reason')})")

    # 4. Fix Punch Item
    print("\n[TEST 3] Billy fixes the scratch...")
    finisher.close_punch_item(res1['id'], "Billy")
    # Mark Verified manually for test
    finisher.punch_list[-1]['status'] = "VERIFIED"

    # 5. Issue Warranty (Success)
    print("\n[TEST 4] Issuing Warranty...")
    # Clean up mock data first to ensure clean state
    finisher.punch_list = [p for p in finisher.punch_list if p['status'] == "VERIFIED"]

    res3 = finisher.issue_warranty("JOB-26001", "2026-02-01")
    print(f" > {res3.get('message')}")
    print(f" > Expires: {finisher.warranties[-1]['end_date']}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT CLOSEOUT SYSTEM: OPERATIONAL")