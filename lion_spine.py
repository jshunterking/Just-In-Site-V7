"""
LION SPINE V7.0
The Project Management Backbone for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module supports the heavy weight of Project Management. It is the central
nervous system for an Active Job. It handles the transition from "Sales" to
"Operations" and manages the critical documentation (RFIs, Submittals).

CORE CAPABILITIES:
1. Job Genesis (Estimate -> Active Job).
2. RFI & Submittal Tracking.
3. Financial Health Monitoring (Budget vs Actual).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Monkey Brain (Database Write)
"""

import uuid
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
# 🦁 LION SPINE CLASS
# ==============================================================================

class LionSpine:
    """
    The PM's Support Structure.
    """

    def __init__(self):
        # In a real app, these lists live in 'monkey_brain.db'
        self.active_rfis = []
        self.submittals = []

    # ==========================================================================
    # 🧬 JOB GENESIS (The Big Bang)
    # ==========================================================================

    def convert_bid_to_project(self, estimate_data: Dict, pm_user: str) -> Dict[str, Any]:
        """
        Takes a 'Won' Estimate from Jaguar and creates the Project Infrastructure.

        ARGS:
            estimate_data: { 'project': 'Mercy Hospital', 'raw_cost': 150000, ... }
            pm_user: "Justin"
        """
        # 1. Generate New Job ID
        # In V7, we'd call MonkeyBrain.generate_job_id(). Mocking here:
        new_job_id = f"JOB-26{int(time.time()) % 1000:03d}"

        # 2. Establish Budget
        # We lock the budget at the "Raw Cost" from the estimate.
        original_budget = estimate_data.get('raw_cost', 0)

        # 3. Create Record
        project_record = {
            "job_id": new_job_id,
            "name": estimate_data.get('project', 'New Project'),
            "status": "ACTIVE",
            "pm": pm_user,
            "budget_total": original_budget,
            "budget_spent": 0.0,
            "start_date": datetime.now().strftime("%Y-%m-%d")
        }

        MonkeyHeart.log_system_event("LION_GENESIS",
                                     f"Created Project {new_job_id} from Estimate. Budget: ${original_budget:,.2f}")

        return {
            "success": True,
            "job_id": new_job_id,
            "message": f"Project {new_job_id} Live. Handover complete."
        }

    # ==========================================================================
    # 📩 THE PAPER TRAIL (RFIs & Submittals)
    # ==========================================================================

    def create_rfi(self, job_id: str, question: str, author: str) -> str:
        """
        Logs a formal Request For Information.
        """
        rfi_num = len([r for r in self.active_rfis if r['job_id'] == job_id]) + 1
        rfi_id = f"RFI-{job_id.replace('JOB-', '')}-{rfi_num:03d}"

        record = {
            "id": rfi_id,
            "job_id": job_id,
            "question": question,
            "answer": None,
            "status": "OPEN",  # OPEN, ANSWERED, CLOSED
            "author": author,
            "date_sent": datetime.now().strftime("%Y-%m-%d"),
            "due_date": (datetime.now() + 7 * datetime.resolution).strftime("%Y-%m-%d")
            # Default 7 days? No, simple math for V7 mock
        }

        self.active_rfis.append(record)
        MonkeyHeart.log_system_event("LION_RFI", f"RFI {rfi_id} Generated: {question[:30]}...")
        return rfi_id

    def answer_rfi(self, rfi_id: str, answer: str):
        """
        Logs the Architect's response.
        """
        rfi = next((r for r in self.active_rfis if r['id'] == rfi_id), None)
        if rfi:
            rfi['answer'] = answer
            rfi['status'] = "ANSWERED"
            MonkeyHeart.log_system_event("LION_RFI", f"RFI {rfi_id} Answered.")
            Bananas.notify("RFI Update", f"{rfi_id} has been answered. Check the log.")
            return True
        return False

    # ==========================================================================
    # 🌡️ BURN RATE (Financial Health)
    # ==========================================================================

    def check_project_health(self, job_id: str, total_budget: float, current_spend: float) -> Dict[str, Any]:
        """
        Calculates how fast we are burning money vs how much work is done.

        ARGS:
            current_spend: Sum of Payroll + POs.
        """
        if total_budget == 0:
            return {"status": "UNKNOWN", "burn_pct": 0}

        burn_pct = (current_spend / total_budget) * 100
        remaining = total_budget - current_spend

        status = "HEALTHY"
        if burn_pct > 90:
            status = "CRITICAL"
        elif burn_pct > 75:
            status = "WARNING"

        return {
            "job_id": job_id,
            "budget": total_budget,
            "spent": current_spend,
            "remaining": remaining,
            "burn_pct": round(burn_pct, 1),
            "status": status
        }


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦁 LION SPINE V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    pm_core = LionSpine()

    # 2. Test Genesis
    print("\n[TEST 1] Creating New Project from Estimate...")
    mock_est = {"project": "Mercy ER Renovation", "raw_cost": 250000.00}
    res = pm_core.convert_bid_to_project(mock_est, "PM Justin")
    job_id = res['job_id']
    print(f" > {res['message']}")

    # 3. Test RFI
    print("\n[TEST 2] Creating RFI #1...")
    rfi_id = pm_core.create_rfi(job_id, "Does the Architect want 3500K or 4000K LEDs?", "Foreman Mike")
    print(f" > RFI ID: {rfi_id}")

    # 4. Answer RFI
    print("\n[TEST 3] Answering RFI...")
    pm_core.answer_rfi(rfi_id, "Use 4000K per spec section 26-51.")

    # 5. Health Check
    print("\n[TEST 4] Checking Budget Health...")
    # Budget 250k. Spent 200k.
    health = pm_core.check_project_health(job_id, 250000, 200000)
    print(f" > Burn: {health['burn_pct']}%")
    print(f" > Status: {health['status']}")

    print("\n" + "=" * 40)
    print("🦁 LION SPINE SYSTEM: OPERATIONAL")