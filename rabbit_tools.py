"""
RABBIT TOOLS V7.0
The Asset Tracking & Tool Crib Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages high-value assets (Drills, Benders, Threaders, Testers).
It replaces the "clipboard on the wall" with a digital ledger that holds
employees accountable for the gear they take.

CORE CAPABILITIES:
1. Check-In / Check-Out Logic.
2. Maintenance Scheduling (Calibration Tracking).
3. "Broken Tool" Quarantine Workflow.

INTEGRATIONS:
- Bananas (Error Handling)
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
# 🧰 THE TOOL CRIB (Mock Inventory)
# ==============================================================================
# In production, this lives in 'monkey_brain.db' (inventory table).

MOCK_TOOL_CRIB = [
    {
        "id": "T-101",
        "name": "Milwaukee M18 Hammer Drill",
        "category": "POWER_TOOL",
        "status": "AVAILABLE",  # AVAILABLE, ASSIGNED, BROKEN, CALIBRATION
        "assigned_to": None,
        "job_id": None,
        "condition": "GOOD",
        "purchase_date": "2024-01-15",
        "last_calibrated": None
    },
    {
        "id": "T-102",
        "name": "Greenlee 555 Bender",
        "category": "HEAVY_EQUIP",
        "status": "ASSIGNED",
        "assigned_to": "User-005 (Mike)",
        "job_id": "JOB-26001",
        "condition": "FAIR",
        "purchase_date": "2020-05-20",
        "last_calibrated": None
    },
    {
        "id": "T-201",
        "name": "Fluke 1587 Insulation Tester",
        "category": "TESTER",
        "status": "AVAILABLE",
        "assigned_to": None,
        "job_id": None,
        "condition": "GOOD",
        "purchase_date": "2023-11-01",
        "last_calibrated": "2025-01-01"  # Due annually
    },
    {
        "id": "T-999",
        "name": "Ridgid 300 Threader",
        "category": "HEAVY_EQUIP",
        "status": "BROKEN",
        "assigned_to": None,
        "job_id": None,
        "condition": "NEEDS_REPAIR",
        "purchase_date": "2018-03-10",
        "last_calibrated": None
    }
]


# ==============================================================================
# 🐰 RABBIT TOOLS CLASS
# ==============================================================================

class RabbitTools:
    """
    The Crib Master.
    """

    def __init__(self):
        # Load inventory into memory for V7.0 Demo
        self.inventory = MOCK_TOOL_CRIB

    # ==========================================================================
    # 🔄 CHECK-OUT / CHECK-IN
    # ==========================================================================

    def checkout_tool(self, tool_id: str, user_name: str, job_id: str) -> Dict[str, Any]:
        """
        Assigns a tool to a user.
        """
        tool = self._find_tool(tool_id)

        if not tool:
            Bananas.notify("Tool Error", f"ID {tool_id} not found.")
            return {"success": False}

        if tool['status'] != 'AVAILABLE':
            Bananas.notify("Tool Unavailable", f"{tool['name']} is currently {tool['status']}.")
            return {"success": False}

        # Execute Checkout
        tool['status'] = 'ASSIGNED'
        tool['assigned_to'] = user_name
        tool['job_id'] = job_id

        MonkeyHeart.log_system_event("TOOLS_OUT", f"{user_name} took {tool['name']} to {job_id}")
        return {
            "success": True,
            "message": f"Assigned {tool['name']} to {user_name}."
        }

    def checkin_tool(self, tool_id: str, condition: str, notes: str = "") -> Dict[str, Any]:
        """
        Returns a tool to the crib.
        """
        tool = self._find_tool(tool_id)

        if not tool:
            return {"success": False}

        prev_user = tool['assigned_to']

        # Reset State
        tool['assigned_to'] = None
        tool['job_id'] = None
        tool['condition'] = condition

        if condition in ['BROKEN', 'DAMAGED', 'NEEDS_REPAIR']:
            tool['status'] = 'BROKEN'
            MonkeyHeart.log_system_event("TOOLS_BROKEN",
                                         f"{tool['name']} returned BROKEN by {prev_user}. Note: {notes}")
            Bananas.notify("Maintenance Alert", f"{tool['name']} flagged for repair.")
        else:
            tool['status'] = 'AVAILABLE'
            MonkeyHeart.log_system_event("TOOLS_IN",
                                         f"{tool['name']} returned by {prev_user} in {condition} condition.")

        return {"success": True, "status": tool['status']}

    # ==========================================================================
    # 🛠️ MAINTENANCE LOGIC
    # ==========================================================================

    def check_calibration_status(self) -> List[Dict]:
        """
        Scans all testers to see if their calibration is expired (1 Year).
        """
        alerts = []
        today = datetime.now()

        for tool in self.inventory:
            if tool.get('last_calibrated'):
                last_cal = datetime.strptime(tool['last_calibrated'], "%Y-%m-%d")
                next_cal = last_cal + timedelta(days=365)

                if today > next_cal:
                    tool['status'] = 'CALIBRATION_EXPIRED'
                    alerts.append({
                        "id": tool['id'],
                        "name": tool['name'],
                        "expired_on": next_cal.strftime("%Y-%m-%d")
                    })

        if alerts:
            MonkeyHeart.log_system_event("TOOLS_CAL", f"Found {len(alerts)} tools with expired calibration.")

        return alerts

    def _find_tool(self, tool_id: str) -> Optional[Dict]:
        """Helper to search the list."""
        for t in self.inventory:
            if t['id'] == tool_id:
                return t
        return None


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT TOOLS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    crib = RabbitTools()

    # 2. Test Checkout
    print("\n[TEST 1] Checking Out T-101 (Drill)...")
    res1 = crib.checkout_tool("T-101", "Justin", "JOB-26001")
    print(f" > {res1['message']}")

    # 3. Test Double Checkout (Should Fail)
    print("\n[TEST 2] Checking Out T-101 Again...")
    res2 = crib.checkout_tool("T-101", "Another Guy", "JOB-26002")
    if not res2['success']:
        print(" > Success: Prevented double booking.")

    # 4. Test Checkin (Broken)
    print("\n[TEST 3] Returning T-101 (Broken)...")
    res3 = crib.checkin_tool("T-101", "BROKEN", "Dropped off ladder")
    print(f" > New Status: {res3['status']}")

    # 5. Calibration Check
    print("\n[TEST 4] Checking Calibration...")
    alerts = crib.check_calibration_status()
    if alerts:
        print(f" > ALERT: {alerts[0]['name']} expired on {alerts[0]['expired_on']}")
    else:
        print(" > All tools calibrated.")

    print("\n" + "=" * 40)
    print("🐰 RABBIT TOOLS SYSTEM: OPERATIONAL")