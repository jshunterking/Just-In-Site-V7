"""
RABBIT CLAWS V7.0
The Tool & Equipment Tracking Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the company's "Hard Assets" (Drills, Benders, Ladders).
It ensures that expensive equipment doesn't walk away. It tracks who has what,
where it is, and if it is safe to use.

CORE CAPABILITIES:
1. Check-In / Check-Out (Assignment).
2. Calibration & Maintenance Tracking.
3. Condition Reporting (Broken/Lost).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Rabbit Geofence (Asset Tethering - optional)
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
# 🔨 THE TOOL CRIB (Mock Database)
# ==============================================================================

MOCK_TOOLS = {
    "TOOL-101": {
        "name": "Hilti TE-60 Hammer Drill",
        "category": "POWER_TOOL",
        "status": "IN_CRIB",  # IN_CRIB, ASSIGNED, BROKEN, LOST
        "assigned_to": None,
        "job_location": "WAREHOUSE",
        "calibration_due": None,
        "condition": "GOOD"
    },
    "TOOL-205": {
        "name": "Greenlee 555 Bender",
        "category": "HEAVY_EQUIP",
        "status": "ASSIGNED",
        "assigned_to": "Foreman Mike",
        "job_location": "JOB-26001",
        "calibration_due": None,
        "condition": "FAIR"
    },
    "TOOL-300": {
        "name": "Torque Wrench 1/2in",
        "category": "PRECISION",
        "status": "IN_CRIB",
        "assigned_to": None,
        "job_location": "WAREHOUSE",
        "calibration_due": "2025-01-01",  # EXPIRED!
        "condition": "GOOD"
    }
}


# ==============================================================================
# 🐰 RABBIT CLAWS CLASS
# ==============================================================================

class RabbitClaws:
    """
    The Tool Tracker.
    """

    def __init__(self):
        self.crib = MOCK_TOOLS

    # ==========================================================================
    # 📝 ASSIGNMENT (The Library)
    # ==========================================================================

    def checkout_tool(self, tool_id: str, user_id: str, job_id: str) -> Dict[str, Any]:
        """
        Moves tool from Crib to Job. Checks for blocks first.
        """
        tool = self.crib.get(tool_id)
        if not tool:
            return {"success": False, "reason": "Tool Not Found"}

        # 1. Availability Check
        if tool['status'] != "IN_CRIB":
            return {"success": False, "reason": f"Tool is {tool['status']} (at {tool['job_location']})"}

        # 2. Calibration Watchdog
        if tool['calibration_due']:
            due_date = datetime.strptime(tool['calibration_due'], "%Y-%m-%d")
            if datetime.now() > due_date:
                Bananas.notify("Safety Lock", f"{tool['name']} Calibration Expired on {tool['calibration_due']}.")
                return {"success": False, "reason": "CALIBRATION_EXPIRED"}

        # 3. Assign
        tool['status'] = "ASSIGNED"
        tool['assigned_to'] = user_id
        tool['job_location'] = job_id

        MonkeyHeart.log_system_event("TOOL_OUT", f"{tool['name']} assigned to {user_id} @ {job_id}")
        return {"success": True, "message": "Tool Checked Out."}

    def return_tool(self, tool_id: str, condition: str, notes: str = "") -> Dict[str, Any]:
        """
        Moves tool back to Crib.
        """
        tool = self.crib.get(tool_id)
        if not tool: return {"success": False}

        prev_user = tool['assigned_to']
        tool['status'] = "IN_CRIB"
        tool['assigned_to'] = None
        tool['job_location'] = "WAREHOUSE"
        tool['condition'] = condition

        MonkeyHeart.log_system_event("TOOL_IN", f"{tool['name']} returned by {prev_user}. Condition: {condition}")

        if condition == "BROKEN":
            self._flag_for_repair(tool_id, notes)

        return {"success": True, "message": "Tool Returned."}

    # ==========================================================================
    # 🔧 MAINTENANCE & REPAIR
    # ==========================================================================

    def _flag_for_repair(self, tool_id: str, issue: str):
        """
        Internal method to lock a broken tool.
        """
        tool = self.crib[tool_id]
        tool['status'] = "BROKEN"
        msg = f"REPAIR TICKET: {tool['name']} - {issue}"
        Bananas.notify("Tool Damaged", msg)
        MonkeyHeart.log_system_event("TOOL_BROKEN", msg)

    def get_calibration_alerts(self) -> List[str]:
        """
        Scans for expiring certs.
        """
        alerts = []
        now = datetime.now()
        warning_window = timedelta(days=30)

        for tid, data in self.crib.items():
            if data['calibration_due']:
                due = datetime.strptime(data['calibration_due'], "%Y-%m-%d")
                if now > due:
                    alerts.append(f"OVERDUE: {data['name']} (Exp: {data['calibration_due']})")
                elif now + warning_window > due:
                    alerts.append(f"DUE SOON: {data['name']} (Exp: {data['calibration_due']})")

        return alerts


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT CLAWS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    crib_manager = RabbitClaws()

    # 2. Test Checkout (Success)
    print("\n[TEST 1] Checking out Hammer Drill...")
    res1 = crib_manager.checkout_tool("TOOL-101", "Foreman Mike", "JOB-26001")
    print(f" > Status: {res1['success']} ({res1.get('message')})")

    # 3. Test Checkout (Fail - Expired)
    print("\n[TEST 2] Checking out Torque Wrench (Expired)...")
    res2 = crib_manager.checkout_tool("TOOL-300", "Apprentice Joe", "JOB-26001")
    print(f" > Status: {res2['success']} (Reason: {res2.get('reason')})")

    # 4. Return Broken
    print("\n[TEST 3] Returning Drill (Broken)...")
    res3 = crib_manager.return_tool("TOOL-101", "BROKEN", "Chuck is seized")
    print(f" > Status: {res3['message']}")

    # 5. Verify Lock
    tool = crib_manager.crib["TOOL-101"]
    print(f" > Drill Status: {tool['status']}")  # Should be BROKEN

    print("\n" + "=" * 40)
    print("🐰 RABBIT CLAWS SYSTEM: OPERATIONAL")