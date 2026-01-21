"""
RABBIT RFIS V7.0
The Request for Information (RFI) Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the formal Q&A process between the Field and the
Design Team (Architect/Engineer). It ensures that questions are documented,
numbered, and answered within a contractual timeframe.

CORE CAPABILITIES:
1. RFI Generation & Numbering.
2. Cost/Schedule Impact Detection.
3. Response Tracking & Aging (SLA).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Rabbit Change Order (Cost Triggers)
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
# ❓ THE QUESTION QUEUE (Mock Database)
# ==============================================================================

MOCK_RFIS = [
    {
        "id": "RFI-26001-001",
        "job_id": "JOB-26001",
        "subject": "Beam Conflict in Room 101",
        "question": "HVAC duct blocks cable tray path. Can we lower tray 6 inches?",
        "proposed_solution": "Lower tray to 9ft AFF.",
        "status": "OPEN",  # OPEN, ANSWERED, CLOSED
        "cost_impact": True,
        "date_sent": "2026-01-15",
        "due_date": "2026-01-18"  # Overdue!
    }
]


# ==============================================================================
# 🐰 RABBIT RFIS CLASS
# ==============================================================================

class RabbitRFIs:
    """
    The Questioner.
    """

    def __init__(self):
        self.rfis = MOCK_RFIS

    # ==========================================================================
    # 📤 DRAFTING
    # ==========================================================================

    def create_rfi(self, job_id: str, subject: str, question: str,
                   impact_cost: bool, impact_schedule: bool) -> Dict[str, Any]:
        """
        Generates a formal question.
        """
        # Auto-Numbering
        job_rfis = [r for r in self.rfis if r['job_id'] == job_id]
        next_num = len(job_rfis) + 1
        rfi_id = f"RFI-{job_id.replace('JOB-', '')}-{next_num:03d}"

        # Calculate Due Date (Standard 3 Days)
        due_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

        new_rfi = {
            "id": rfi_id,
            "job_id": job_id,
            "subject": subject,
            "question": question,
            "status": "OPEN",
            "cost_impact": impact_cost,
            "schedule_impact": impact_schedule,
            "date_sent": datetime.now().strftime("%Y-%m-%d"),
            "due_date": due_date,
            "answer": None
        }

        self.rfis.append(new_rfi)

        MonkeyHeart.log_system_event("RFI_SENT", f"{rfi_id}: {subject} (Cost Impact: {impact_cost})")

        # 1. The Cost Trap
        if impact_cost:
            Bananas.notify("Potential Change Order", f"RFI {rfi_id} flagged for cost impact. Alerting PM.")
            # In real app: RabbitChangeOrder.create_placeholder(rfi_id)

        return {"success": True, "rfi_id": rfi_id, "due_date": due_date}

    # ==========================================================================
    # 📥 PROCESSING ANSWER
    # ==========================================================================

    def receive_answer(self, rfi_id: str, answer_text: str, answered_by: str):
        """
        Logs the architect's reply.
        """
        rfi = next((r for r in self.rfis if r['id'] == rfi_id), None)
        if not rfi: return False

        rfi['answer'] = answer_text
        rfi['status'] = "ANSWERED"
        rfi['date_answered'] = datetime.now().strftime("%Y-%m-%d")

        MonkeyHeart.log_system_event("RFI_ANSWER", f"{rfi_id} answered by {answered_by}")
        Bananas.notify("RFI Answered", f"{rfi_id}: See response.")

        return True

    # ==========================================================================
    # ⏱️ AGING & NAGGING
    # ==========================================================================

    def check_overdue_rfis(self) -> List[str]:
        """
        Finds questions that are rotting on the vine.
        """
        overdue = []
        now = datetime.now().strftime("%Y-%m-%d")

        for rfi in self.rfis:
            if rfi['status'] == "OPEN" and now > rfi['due_date']:
                msg = f"OVERDUE: {rfi['id']} (Due {rfi['due_date']})"
                overdue.append(msg)

        if overdue:
            Bananas.notify("RFI Delay", f"{len(overdue)} RFIs are late. Send the nag email.")

        return overdue


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT RFIS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    questioner = RabbitRFIs()

    # 2. Create RFI (With Cost Impact)
    print("\n[TEST 1] Drafting RFI for 'Wrong Paint Color'...")
    res1 = questioner.create_rfi("JOB-26001", "Paint Color", "Spec says Blue, Plan says Red?", True, False)
    print(f" > RFI ID: {res1['rfi_id']}")
    print(f" > Due Date: {res1['due_date']}")

    # 3. Receive Answer
    print("\n[TEST 2] Architect Responds...")
    questioner.receive_answer(res1['rfi_id'], "Use Blue.", "Architect John")

    # 4. Check Overdue (The Mock Data has one overdue)
    print("\n[TEST 3] Checking Aging Report...")
    late_list = questioner.check_overdue_rfis()
    for l in late_list:
        print(f" > {l}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT RFIS SYSTEM: OPERATIONAL")
