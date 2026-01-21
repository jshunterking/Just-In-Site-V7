"""
RAPTOR ADMIN V7.0
The System Administration & Configuration Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the control panel for the application itself. It manages
global settings, emergency lockouts, and deep system diagnostics.
It differs from Lion Mane (HR) because it controls the *Environment*, not the *Users*.

CORE CAPABILITIES:
1. Global Configuration Management (Tax, Burden).
2. Emergency System Lockdown (Kill Switch).
3. Session Shadowing (Debug/Audit).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Monkey Brain (Config Storage)
"""

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
# ⚙️ GLOBAL CONFIG (The Physics)
# ==============================================================================

MOCK_CONFIG = {
    "labor_burden_pct": 1.45,
    "sales_tax_ohio": 0.075,
    "sales_tax_pa": 0.060,
    "system_status": "ONLINE",  # ONLINE, MAINTENANCE, LOCKDOWN
    "maintenance_mode_message": "System is down for upgrades. Back at 6:00 AM."
}


# ==============================================================================
# 🦕 RAPTOR ADMIN CLASS
# ==============================================================================

class RaptorAdmin:
    """
    The Keymaster.
    """

    def __init__(self):
        self.config = MOCK_CONFIG

    # ==========================================================================
    # 🔧 CONFIGURATION MANAGEMENT
    # ==========================================================================

    def update_global_setting(self, key: str, value: Any, admin_user: str) -> bool:
        """
        Hot-swaps a system variable.
        """
        if key not in self.config:
            return False

        old_val = self.config[key]
        self.config[key] = value

        MonkeyHeart.log_system_event("CONFIG_CHANGE", f"{admin_user} changed {key} from {old_val} to {value}")
        return True

    def get_current_config(self) -> Dict[str, Any]:
        return self.config

    # ==========================================================================
    # 🔴 EMERGENCY LOCKDOWN
    # ==========================================================================

    def trigger_kill_switch(self, admin_user: str, reason: str):
        """
        The Nuclear Option. Revokes all access.
        """
        self.config['system_status'] = "LOCKDOWN"

        msg = f"SYSTEM LOCKDOWN INITIATED BY {admin_user}. REASON: {reason}"
        Bananas.notify("🚨 SECURITY LOCKDOWN 🚨", msg)
        MonkeyHeart.log_security_event("KILL_SWITCH", msg, "CRITICAL")

        # In real app: Calls MonkeyBrain to invalidate all session tokens immediately.
        print(" >> [ADMIN] All active sessions terminated.")
        print(" >> [ADMIN] API Gateways closed.")

    def lift_lockdown(self, admin_user: str):
        """
        Restores order.
        """
        self.config['system_status'] = "ONLINE"
        MonkeyHeart.log_security_event("SYSTEM_RESTORE", f"Lockdown lifted by {admin_user}", "SUCCESS")
        Bananas.notify("System Online", "Operations may resume.")

    # ==========================================================================
    # 👻 GHOST PROTOCOL (Shadowing)
    # ==========================================================================

    def shadow_user_session(self, target_user_id: str) -> Dict[str, Any]:
        """
        Retrieves the last 5 actions of a specific user for debugging.
        """
        # Mocking data retrieval from MonkeyHeart logs
        mock_activity = [
            "User logged in",
            "User clicked 'Submit Daily'",
            "ERROR: Collision in RabbitDaily",
            "User refreshed page"
        ]

        MonkeyHeart.log_security_event("ADMIN_SHADOW", f"Admin shadowing user {target_user_id}", "AUDIT")

        return {
            "user_id": target_user_id,
            "status": "ACTIVE",
            "recent_logs": mock_activity
        }


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦕 RAPTOR ADMIN V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    keymaster = RaptorAdmin()

    # 2. Test Config Change
    print("\n[TEST 1] Updating Sales Tax...")
    keymaster.update_global_setting("sales_tax_ohio", 0.080, "Justin")
    print(f" > New Ohio Tax: {keymaster.get_current_config()['sales_tax_ohio']}")

    # 3. Test Shadowing
    print("\n[TEST 2] Shadowing User U-005...")
    trace = keymaster.shadow_user_session("U-005")
    print(f" > Recent Activity: {trace['recent_logs']}")

    # 4. Test Kill Switch
    print("\n[TEST 3] KILL SWITCH ACTIVATION...")
    keymaster.trigger_kill_switch("Justin", "Suspected Data Breach")
    print(f" > System Status: {keymaster.get_current_config()['system_status']}")

    # 5. Restore
    print("\n[TEST 4] Restoring System...")
    keymaster.lift_lockdown("Justin")
    print(f" > System Status: {keymaster.get_current_config()['system_status']}")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR ADMIN SYSTEM: OPERATIONAL")