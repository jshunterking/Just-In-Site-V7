"""
PANTHER BRAIN V7.0
The Service Dispatch & Decision Intelligence for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.2 (Diamond-Grade)

DESCRIPTION:
This module is the mind of the Service Department. It processes incoming
stimuli (Customer Calls), categorizes the threat level (Triage), and
commands the resources (Technicians) to neutralize the issue.

CORE CAPABILITIES:
1. Sensory Triage (Auto-Priority).
2. Survival Timer (SLA Monitoring).
3. Neural Routing (Tech Assignment).
4. State of Mind (Status Workflow).

INTEGRATIONS:
- Bananas (Pain Signals/Alerts)
- Monkey Heart (Memory/Logging)
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
# 🎫 THE SHORT TERM MEMORY (Active Tickets)
# ==============================================================================

MOCK_TICKETS = [
    {
        "id": "T-1001",
        "customer": "Mercy Hospital",
        "issue": "Outlet sparking in OR 3",
        "priority": "CRITICAL",
        "status": "OPEN",
        "created_at": datetime.now().isoformat(),
        "sla_deadline": (datetime.now() + timedelta(hours=2)).isoformat(),  # 2 Hour response
        "tech_assigned": None,
        "gps_lat": 41.0995, "gps_lon": -80.6400
    },
    {
        "id": "T-1002",
        "customer": "Burger King",
        "issue": "Sign light out",
        "priority": "NORMAL",
        "status": "SCHEDULED",
        "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
        "sla_deadline": (datetime.now() + timedelta(days=2)).isoformat(),
        "tech_assigned": "Billy",
        "gps_lat": 41.1050, "gps_lon": -80.6550
    }
]


# ==============================================================================
# 🐆 PANTHER BRAIN CLASS
# ==============================================================================

class PantherBrain:
    """
    The Dispatch Intelligence.
    """

    def __init__(self):
        self.tickets = MOCK_TICKETS

    # ==========================================================================
    # ⚡ SENSORY TRIAGE (Creating Tickets)
    # ==========================================================================

    def process_stimulus(self, customer: str, issue_text: str, address: str) -> Dict[str, Any]:
        """
        Logs a new call. Uses Auto-Triage to set priority.
        """
        # 1. Auto-Triage Logic (The Instinct)
        priority = "NORMAL"
        response_hours = 48

        text_lower = issue_text.lower()
        if any(x in text_lower for x in ["spark", "fire", "smoke", "power out", "emergency"]):
            priority = "CRITICAL"
            response_hours = 2
        elif any(x in text_lower for x in ["flicker", "noise", "outage"]):
            priority = "HIGH"
            response_hours = 24

        # 2. Create Memory
        t_id = f"T-{len(self.tickets) + 1003}"
        deadline = datetime.now() + timedelta(hours=response_hours)

        new_ticket = {
            "id": t_id,
            "customer": customer,
            "issue": issue_text,
            "priority": priority,
            "status": "OPEN",
            "created_at": datetime.now().isoformat(),
            "sla_deadline": deadline.isoformat(),
            "tech_assigned": None,
            "address": address
        }

        self.tickets.append(new_ticket)
        MonkeyHeart.log_system_event("PANTHER_THINK",
                                     f"Ticket {t_id} categorized as {priority}. Deadline: {deadline.strftime('%H:%M')}")

        if priority == "CRITICAL":
            Bananas.notify("ADRENALINE SPIKE", f"{customer}: {issue_text}")

        return {"success": True, "ticket_id": t_id, "priority": priority}

    # ==========================================================================
    # 🚐 NEURAL ROUTING (Dispatch)
    # ==========================================================================

    def command_limb(self, ticket_id: str, tech_name: str) -> bool:
        """
        Commands a technician (Limb) to go to a target.
        """
        ticket = self._find_ticket(ticket_id)
        if not ticket: return False

        ticket['tech_assigned'] = tech_name
        ticket['status'] = "SCHEDULED"

        MonkeyHeart.log_system_event("PANTHER_CMD", f"Dispatched {tech_name} to {ticket_id}")
        return True

    def update_state(self, ticket_id: str, new_status: str) -> bool:
        """
        Workflow: OPEN -> EN_ROUTE -> ON_SITE -> COMPLETE.
        """
        ticket = self._find_ticket(ticket_id)
        if not ticket: return False

        ticket['status'] = new_status
        MonkeyHeart.log_system_event("PANTHER_STATE", f"{ticket_id} state changed to {new_status}")

        if new_status == "COMPLETE":
            # Signal the Mouth to Eat (Billing)
            Bananas.notify("Kill Confirmed", f"{ticket_id} ready for consumption (Invoice).")

        return True

    # ==========================================================================
    # ⏱️ SURVIVAL TIMER (SLA)
    # ==========================================================================

    def check_survival_clock(self) -> List[Dict]:
        """
        Scans all open tickets to see if we are dying (Breach).
        """
        breaches = []
        now = datetime.now()

        for t in self.tickets:
            if t['status'] != "COMPLETE":
                deadline = datetime.fromisoformat(t['sla_deadline'])
                if now > deadline:
                    breaches.append({
                        "id": t['id'],
                        "customer": t['customer'],
                        "overdue_by": str(now - deadline)
                    })

        if breaches:
            Bananas.notify("PAIN SIGNAL", f"{len(breaches)} contracts are bleeding out (SLA Breach)!")

        return breaches

    def _find_ticket(self, t_id: str) -> Optional[Dict]:
        for t in self.tickets:
            if t['id'] == t_id:
                return t
        return None


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐆 PANTHER BRAIN V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    brain = PantherBrain()

    # 2. Process Stimulus (Critical)
    print("\n[TEST 1] Processing Threat: 'Fryer sparking'...")
    res1 = brain.process_stimulus("Taco Bell", "Fryer sparking and smoking", "123 Main St")
    print(f" > Threat Level: {res1['priority']}")

    # 3. Process Stimulus (Normal)
    print("\n[TEST 2] Processing Stimulus: 'Light out'...")
    res2 = brain.process_stimulus("Library", "Replace ballast in lobby", "444 Read Ave")
    print(f" > Threat Level: {res2['priority']}")

    # 4. Neural Command
    print("\n[TEST 3] Commanding Billy...")
    brain.command_limb(res1['ticket_id'], "Billy")

    # 5. Update State
    print("\n[TEST 4] Tech Arrived...")
    brain.update_state(res1['ticket_id'], "ON_SITE")

    # 6. Survival Check
    print("\n[TEST 5] Checking Survival Clocks...")
    breaches = brain.check_survival_clock()
    if not breaches:
        print(" > All systems stable.")
    else:
        print(f" > PAIN: {len(breaches)} breaches detected.")

    print("\n" + "=" * 40)
    print("🐆 PANTHER BRAIN SYSTEM: OPERATIONAL")