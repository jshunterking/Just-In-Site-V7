"""
RABBIT SUBMITTALS V7.0
The Material Specification & Approval Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the "Submittal" process—getting approval from the
Architect/Engineer to purchase specific products. It tracks the ball-in-court,
status codes, and critical lead time impacts.

CORE CAPABILITIES:
1. Submittal Log Management.
2. Digital Stamping (Approval Workflow).
3. Lead Time Criticality Analysis.

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Rabbit Schedule (Date Validation)
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
# 📑 THE LOG (Mock Database)
# ==============================================================================

MOCK_LOG = [
    {
        "id": "SUB-26001-26-01",
        "job_id": "JOB-26001",
        "spec_section": "26-51-00",
        "description": "LED Light Fixtures (Type A, B, C)",
        "status": "OPEN",  # OPEN, SUBMITTED, APPROVED, REJECTED
        "lead_time_weeks": 12,
        "required_on_site": "2026-06-01",
        "date_submitted": None
    }
]


# ==============================================================================
# 🐰 RABBIT SUBMITTALS CLASS
# ==============================================================================

class RabbitSubmittals:
    """
    The Gatekeeper.
    """

    def __init__(self):
        self.log = MOCK_LOG

    # ==========================================================================
    # 📤 CREATION & SUBMISSION
    # ==========================================================================

    def create_package(self, job_id: str, spec_sec: str, desc: str, lead_weeks: int, need_date: str) -> Dict[str, Any]:
        """
        Bundles a product for approval.
        """
        # 1. Criticality Check
        need_dt = datetime.strptime(need_date, "%Y-%m-%d")
        drop_dead_date = need_dt - timedelta(weeks=lead_weeks)

        # If today is past the drop-dead date, we are already late.
        is_critical = False
        if datetime.now() > drop_dead_date:
            is_critical = True
            Bananas.notify("CRITICAL SUBMITTAL", f"{desc} has {lead_weeks}wk lead time. We are late!")

        sub_id = f"SUB-{job_id.replace('JOB-', '')}-{spec_sec[:2]}-{len(self.log) + 1:02d}"

        entry = {
            "id": sub_id,
            "job_id": job_id,
            "spec_section": spec_sec,
            "description": desc,
            "status": "OPEN",
            "lead_time_weeks": lead_weeks,
            "required_on_site": need_date,
            "date_submitted": None
        }

        self.log.append(entry)
        MonkeyHeart.log_system_event("SUB_CREATE", f"Created {sub_id}: {desc}")

        return {"success": True, "sub_id": sub_id, "critical": is_critical}

    def submit_to_architect(self, sub_id: str):
        """
        Sends the package out.
        """
        item = next((s for s in self.log if s['id'] == sub_id), None)
        if not item: return False

        item['status'] = "SUBMITTED"
        item['date_submitted'] = datetime.now().strftime("%Y-%m-%d")

        MonkeyHeart.log_system_event("SUB_SENT", f"{sub_id} sent to Architect.")
        return True

    # ==========================================================================
    # 🕵️ THE STAMP (Review)
    # ==========================================================================

    def process_return(self, sub_id: str, status_code: str, comments: str) -> bool:
        """
        Processes the returned paperwork.
        Codes: NET (No Exceptions Taken), MCN (Make Corrections Noted), RR (Revise Resubmit), REJ (Rejected).
        """
        item = next((s for s in self.log if s['id'] == sub_id), None)
        if not item: return False

        is_good = status_code in ["NET", "MCN"]
        final_status = "APPROVED" if is_good else "REJECTED"

        item['status'] = final_status
        item['return_comments'] = comments
        item['date_returned'] = datetime.now().strftime("%Y-%m-%d")

        MonkeyHeart.log_system_event("SUB_RETURN", f"{sub_id} returned as {status_code}. Status: {final_status}")

        if not is_good:
            Bananas.notify("Submittal Rejected", f"{item['description']} was rejected ({status_code}). Fix ASAP.")
        else:
            Bananas.notify("Submittal Approved", f"{item['description']} is ready to order!")

        return True


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT SUBMITTALS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    gatekeeper = RabbitSubmittals()

    # 2. Create (Critical Lead Time)
    print("\n[TEST 1] Creating Switchgear Submittal (40 weeks lead)...")
    # Need it in 10 weeks (Impossible!)
    impossible_date = (datetime.now() + timedelta(weeks=10)).strftime("%Y-%m-%d")
    res1 = gatekeeper.create_package("JOB-26001", "26-24-00", "Main Switchgear", 40, impossible_date)
    print(f" > Critical Alert: {res1['critical']}")

    # 3. Submit
    print("\n[TEST 2] Sending to Architect...")
    gatekeeper.submit_to_architect(res1['sub_id'])

    # 4. Return (Approved)
    print("\n[TEST 3] Architect Approves...")
    gatekeeper.process_return(res1['sub_id'], "NET", "Approved as submitted.")

    # 5. Verify Status
    item = gatekeeper.log[-1]
    print(f" > Final Status: {item['status']}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT SUBMITTALS SYSTEM: OPERATIONAL")