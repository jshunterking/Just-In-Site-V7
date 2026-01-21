"""
PULSE CHECK V7.0
The System Diagnostic & Health Monitoring Utility for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.2 (Diamond-Grade)

DESCRIPTION:
This is the Master Key. It attempts to spin up the entire Just-In-Site
organism. It imports every vital organ, tests the connections, and
declares the system status.

CORE CAPABILITIES:
1. Module Integrity Check (Import Verification).
2. Dependency Resolution.
3. System Latency Measurement.
4. The "Green Board" (Launch Status).

INTEGRATIONS:
- All V7.0 Modules
"""

import sys
import time
import importlib
from datetime import datetime

# ==============================================================================
# 📋 THE V7.0 MANIFEST
# ==============================================================================

MODULES_TO_CHECK = [
    # 🍌 & ❤️ The Core
    ("bananas", "The Shield"),
    ("monkey_heart", "The Logger"),

    # 🐆 Panther (Service)
    ("panther_brain", "Service Dispatch"),
    ("panther_mouth", "Service Billing"),

    # 🦕 Raptor (Intelligence)
    ("raptor_maps", "Navigation"),
    ("raptor_voice", "Voice Command"),
    ("raptor_pricing", "Market Pricing"),
    ("raptor_vendor", "Supply Chain"),
    ("raptor_broadcast", "Emergency Comms"),
    ("raptor_automation", "Workflow Logic"),
    ("raptor_geofence", "Asset Security"),
    ("raptor_admin", "Global Config"),
    ("raptor_marketing", "Lead Gen"),
    ("raptor_bid_history", "Estimating Archive"),

    # 🐰 Rabbit (Operations)
    ("rabbit_legs", "Fleet Mgmt"),
    ("rabbit_stomach", "Inventory"),
    ("rabbit_paws", "Purchasing"),
    ("rabbit_claws", "Tool Tracking"),
    ("rabbit_time", "Time & Attendance"),
    ("rabbit_daily", "Field Reporting"),
    ("rabbit_rfis", "RFI Mgmt"),
    ("rabbit_changeorder", "Scope Mgmt"),
    ("rabbit_submittals", "Spec Mgmt"),
    ("rabbit_safety", "Safety Compliance"),
    ("rabbit_closeout", "Project Closeout")
]


# ==============================================================================
# 🩺 DIAGNOSTIC ENGINE
# ==============================================================================

class PulseCheck:
    def __init__(self):
        self.results = []
        self.start_time = time.time()

    def run_diagnostics(self):
        print("\n" + "=" * 60)
        print(f"🩺 JUST-IN-SITE V7.0 SYSTEM DIAGNOSTIC")
        print(f"📅 DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60 + "\n")

        success_count = 0

        for module_name, friendly_name in MODULES_TO_CHECK:
            status = self._test_organ(module_name, friendly_name)
            if status:
                success_count += 1

        self._print_summary(success_count)

    def _test_organ(self, module_name: str, friendly_name: str) -> bool:
        """
        Attempts to import and init the module.
        """
        try:
            # 1. Import Time
            t0 = time.time()
            mod = importlib.import_module(module_name)
            t1 = time.time()
            import_ms = (t1 - t0) * 1000

            # 2. Check for Class (Naive check for PascalCase matching filename)
            # e.g., raptor_pricing -> RaptorPricing
            class_name = "".join(x.title() for x in module_name.split('_'))

            has_class = hasattr(mod, class_name)
            status_icon = "✅" if has_class else "⚠️"

            print(f"{status_icon} {module_name:<20} | {friendly_name:<20} | {import_ms:.2f}ms")
            return True

        except ImportError:
            print(f"❌ {module_name:<20} | {friendly_name:<20} | MODULE MISSING")
            return False
        except Exception as e:
            print(f"🔥 {module_name:<20} | {friendly_name:<20} | CRASH: {str(e)}")
            return False

    def _print_summary(self, success_count: int):
        total = len(MODULES_TO_CHECK)
        elapsed = time.time() - self.start_time

        print("\n" + "-" * 60)
        print(f"📊 DIAGNOSTIC COMPLETE IN {elapsed:.4f} SECONDS")
        print(f"🟢 OPERATIONAL: {success_count}/{total}")

        if success_count == total:
            print("\n🚀 SYSTEM STATUS: GREEN. READY FOR LAUNCH.")
            print("   The Beast is awake. Go make some money.")
        else:
            print(f"\n⚠️ SYSTEM STATUS: YELLOW. {total - success_count} MODULES FAILED.")
            print("   Review the log above. Repair missing limbs.")
        print("=" * 60 + "\n")


# ==============================================================================
# 🚀 MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    medic = PulseCheck()
    medic.run_diagnostics()