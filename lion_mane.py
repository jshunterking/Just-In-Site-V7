"""
LION MANE V7.0
The Human Resources & Permissions Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the "Pride" (The Employees). It handles Authentication,
Authorization (Permissions), and the Onboarding/Offboarding lifecycle.
It ensures that an Apprentice cannot accidentally delete a Project Budget.

CORE CAPABILITIES:
1. User Authentication (Login Check).
2. Role Enforcement (RBAC).
3. New Hire Onboarding Wizard.
4. Org Chart Hierarchy.

INTEGRATIONS:
- Bananas (Security Alerts)
- Monkey Heart (Security Auditing)
- Monkey Brain (User Database)
"""

import hashlib
import uuid
import time
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
# 🦁 THE PRIDE (Mock User Database)
# ==============================================================================

MOCK_USERS = [
    {
        "id": "U-001", "username": "justin", "hash": "admin123_hashed",
        "role": "ADMIN", "full_name": "Justin (King Kong)", "reports_to": None
    },
    {
        "id": "U-005", "username": "mike", "hash": "pass123_hashed",
        "role": "FOREMAN", "full_name": "Foreman Mike", "reports_to": "U-002"
    },
    {
        "id": "U-012", "username": "joe", "hash": "pass123_hashed",
        "role": "APPRENTICE", "full_name": "Joe Apprentice", "reports_to": "U-005"
    }
]

# Permissions Matrix
ROLE_PERMISSIONS = {
    "ADMIN": ["ALL"],
    "PM": ["VIEW_FINANCIALS", "EDIT_BUDGET", "APPROVE_PO", "VIEW_SCHEDULE"],
    "FOREMAN": ["VIEW_PLANS", "CREATE_DAILY", "REQUEST_PO", "VIEW_SCHEDULE", "CLOCK_CREW"],
    "APPRENTICE": ["CLOCK_SELF", "VIEW_SCHEDULE", "VIEW_SAFETY"]
}


# ==============================================================================
# 🦁 LION MANE CLASS
# ==============================================================================

class LionMane:
    """
    The Gatekeeper.
    """

    def __init__(self):
        self.users = MOCK_USERS

    # ==========================================================================
    # 🔐 AUTHENTICATION
    # ==========================================================================

    def login(self, username: str, password_input: str) -> Dict[str, Any]:
        """
        Verifies credentials.
        """
        # Mock Hash Logic (In real life, use bcrypt)
        input_hash = f"{password_input}_hashed"

        user = next((u for u in self.users if u['username'] == username.lower()), None)

        if not user:
            MonkeyHeart.log_security_event("LOGIN_ATTEMPT", f"Unknown user: {username}", "FAILURE")
            return {"success": False, "reason": "User not found"}

        if user['hash'] == input_hash:
            MonkeyHeart.log_security_event("LOGIN", f"{username} logged in successfully.", "SUCCESS")
            return {
                "success": True,
                "user_id": user['id'],
                "role": user['role'],
                "name": user['full_name']
            }
        else:
            MonkeyHeart.log_security_event("LOGIN_ATTEMPT", f"Bad password for {username}", "FAILURE")
            return {"success": False, "reason": "Invalid credentials"}

    # ==========================================================================
    # 🛡️ AUTHORIZATION (Can I do this?)
    # ==========================================================================

    def check_permission(self, role: str, required_perm: str) -> bool:
        """
        Checks if the User Role is allowed to perform the Action.
        """
        allowed_actions = ROLE_PERMISSIONS.get(role, [])

        if "ALL" in allowed_actions:
            return True

        return required_perm in allowed_actions

    # ==========================================================================
    # 🐣 ONBOARDING WIZARD
    # ==========================================================================

    def onboard_new_hire(self, full_name: str, role: str, reports_to_id: str) -> Dict[str, Any]:
        """
        Automates the hiring process:
        1. Generates Username.
        2. Sets Default Password.
        3. Assigns to Org Chart.
        """
        # Generate Username (First Initial + Last Name)
        parts = full_name.split()
        if len(parts) >= 2:
            base_name = f"{parts[0][0]}{parts[-1]}".lower()
        else:
            base_name = full_name.lower()

        # Avoid duplicates (Simple check)
        username = base_name
        count = 1
        while any(u['username'] == username for u in self.users):
            username = f"{base_name}{count}"
            count += 1

        new_id = f"U-{len(self.users) + 100:03d}"
        temp_pass = "Welcome2026!"

        new_user = {
            "id": new_id,
            "username": username,
            "hash": f"{temp_pass}_hashed",
            "role": role,
            "full_name": full_name,
            "reports_to": reports_to_id
        }

        self.users.append(new_user)
        MonkeyHeart.log_system_event("HR_HIRE", f"Onboarded {full_name} as {role}. Username: {username}")

        return {
            "success": True,
            "username": username,
            "temp_password": temp_pass,
            "message": f"Welcome {full_name} to the Pride!"
        }

    # ==========================================================================
    # 🌳 ORG CHART
    # ==========================================================================

    def get_supervisor(self, user_id: str) -> Optional[str]:
        """
        Finds the boss of a specific user.
        """
        user = next((u for u in self.users if u['id'] == user_id), None)
        if user and user['reports_to']:
            boss = next((b for b in self.users if b['id'] == user['reports_to']), None)
            if boss:
                return boss['full_name']
        return "None (Top of Chain)"


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦁 LION MANE V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    hr = LionMane()

    # 2. Test Login (Success)
    print("\n[TEST 1] Logging in Foreman Mike...")
    login = hr.login("mike", "pass123")
    print(f" > Success: {login['success']} (Role: {login.get('role')})")

    # 3. Test Permission (Fail)
    print("\n[TEST 2] Can Foreman Mike Edit Budget?")
    can_do = hr.check_permission("FOREMAN", "EDIT_BUDGET")
    print(f" > Permission Granted: {can_do}")

    # 4. Test Onboarding
    print("\n[TEST 3] Hiring 'Billy The Kid'...")
    new_hire = hr.onboard_new_hire("Billy Kid", "APPRENTICE", "U-005")
    print(f" > Username: {new_hire['username']}")
    print(f" > Temp Pass: {new_hire['temp_password']}")

    # 5. Check Org Chart
    print("\n[TEST 4] Who is Joe Apprentice's Boss?")
    boss = hr.get_supervisor("U-012")
    print(f" > Boss: {boss}")

    print("\n" + "=" * 40)
    print("🦁 LION MANE SYSTEM: OPERATIONAL")