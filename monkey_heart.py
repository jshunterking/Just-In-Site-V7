"""
MONKEY HEART V7.0
The Central Logging & Health Monitoring System for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the first of the "Vital Organs." It is referenced by almost
every other module (Raptors, Rabbits, Owls) to record what is happening.
It manages the "Audit Trail" - the legal and technical history of the company.

CORE CAPABILITIES:
1. System Event Logging (Debug/Info/Error).
2. Financial Audit Logging (Money Movement).
3. Security Logging (Login/Auth Failures).
4. Heartbeat (Uptime Proof).

INTEGRATIONS:
- Native Python Logging
- JSON File Handler (for structured data)
"""

import logging
import json
import os
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any


# ==============================================================================
# ❤️ MONKEY HEART CLASS
# ==============================================================================

class MonkeyHeart:
    """
    The Pulse of the System.

    ATTRIBUTES:
        log_dir (str): Where the .log files live.
        session_id (str): Unique ID for this specific run of the software.
    """

    # Static config
    LOG_DIR = "logs"
    SESSION_ID = f"SES-{uuid.uuid4().hex[:8].upper()}"

    def __init__(self):
        self._setup_directories()
        self._configure_logger()
        self.log_system_event("HEART", f"System Startup. Session: {self.SESSION_ID}")

    def _setup_directories(self):
        """Ensures the log directory exists."""
        if not os.path.exists(self.LOG_DIR):
            os.makedirs(self.LOG_DIR)

    def _configure_logger(self):
        """Sets up the Python logging facility."""
        # We use a daily log file format: monkeys_2026-01-20.log
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.LOG_DIR, f"monkeys_{today}.jsonl")

        # We write raw JSON lines for easy parsing later
        self.log_file_path = log_file

    # ==========================================================================
    # 📝 LOGGING METHODS (The Recorder)
    # ==========================================================================

    @staticmethod
    def log_system_event(event_type: str, message: str, user: str = "SYSTEM", severity: str = "INFO"):
        """
        The standard log function used by all modules.

        ARGS:
            event_type: "VOICE", "MAPS", "AUTH", etc.
            message: "User clicked button."
            user: Who did it?
            severity: "INFO", "WARNING", "ERROR", "CRITICAL"
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session": MonkeyHeart.SESSION_ID,
            "category": "SYSTEM",
            "type": event_type,
            "severity": severity,
            "user": user,
            "message": message
        }
        MonkeyHeart._write_entry(entry)

    @staticmethod
    def log_financial_event(job_id: str, amount: float, description: str, user: str):
        """
        High-priority logging for money.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session": MonkeyHeart.SESSION_ID,
            "category": "FINANCIAL",
            "job_id": job_id,
            "amount": amount,
            "user": user,
            "message": description,
            "severity": "AUDIT"
        }
        MonkeyHeart._write_entry(entry)
        # In V7.0, we also print Money logs to console for visibility
        print(f"💰 [AUDIT] {job_id}: ${amount} - {description}")

    @staticmethod
    def log_security_event(event_type: str, details: str, status: str):
        """
        Logging for Auth/Login attempts.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session": MonkeyHeart.SESSION_ID,
            "category": "SECURITY",
            "type": event_type,
            "status": status,
            "message": details,
            "severity": "HIGH" if status == "FAILURE" else "INFO"
        }
        MonkeyHeart._write_entry(entry)

    @classmethod
    def _write_entry(cls, entry: Dict):
        """
        Internal writer. Appends JSON line to file and prints to console.
        """
        # 1. Console Output (The Developer View)
        # We use Icons to make the console readable
        icon = "ℹ️"
        if entry.get("severity") == "ERROR":
            icon = "❌"
        elif entry.get("severity") == "WARNING":
            icon = "⚠️"
        elif entry.get("severity") == "AUDIT":
            icon = "💰"
        elif entry.get("category") == "SECURITY":
            icon = "🔒"

        log_msg = f"{icon} [{entry['type']}] {entry['message']}"
        print(log_msg)

        # 2. File Output (The Persistent Record)
        # In V7.0, check directory existence again just in case
        if not os.path.exists(cls.LOG_DIR):
            os.makedirs(cls.LOG_DIR)

        today = datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(cls.LOG_DIR, f"monkeys_{today}.jsonl")

        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            # If logging fails, we are in deep trouble. Print to stderr.
            print(f"!!! CRITICAL FAILURE: CANNOT WRITE LOGS: {e}")

    # ==========================================================================
    # 💓 THE PULSE (Uptime Check)
    # ==========================================================================

    def beat(self):
        """
        Called periodically to indicate the system is alive.
        """
        self.log_system_event("HEARTBEAT", "System Alive.", severity="DEBUG")


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n❤️ MONKEY HEART V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    heart = MonkeyHeart()

    # 2. Test Standard Log
    print("\n[TEST 1] Standard Log...")
    heart.log_system_event("TEST", "This is a test message.", user="Justin")

    # 3. Test Financial Log
    print("\n[TEST 2] Financial Audit...")
    heart.log_financial_event("JOB-26001", 500.00, "Bought Wire", user="Foreman Mike")

    # 4. Test Security Log
    print("\n[TEST 3] Security Alert...")
    heart.log_security_event("LOGIN", "Invalid Password for 'admin'", "FAILURE")

    # 5. Verify File
    print("\n[TEST 4] Verifying Log File...")
    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join("logs", f"monkeys_{today}.jsonl")
    if os.path.exists(path):
        print(f" > Log file found: {path}")
        with open(path, "r") as f:
            lines = f.readlines()
            print(f" > Total Entries: {len(lines)}")
            print(f" > Last Entry: {lines[-1].strip()}")
    else:
        print(" > ERROR: Log file not created.")

    print("\n" + "=" * 40)
    print("❤️ MONKEY HEART SYSTEM: OPERATIONAL")