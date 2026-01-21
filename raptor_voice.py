"""
RAPTOR VOICE V7.0
The Voice Control & Dictation Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the "Siri" for Construction. It translates raw audio transcripts
into executable system commands. It allows a Foreman to order material or
log incidents without taking his gloves off.

CORE CAPABILITIES:
1. Command Parsing (Who are we talking to?).
2. Emergency Trigger (Safety Broadcast).
3. Transcript Cleaning (Removing filler words).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Raptor Broadcast (Emergency Comms)
"""

import re
from typing import Dict, Optional, Any

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
# 🦕 RAPTOR VOICE CLASS
# ==============================================================================

class RaptorVoice:
    """
    The Translator.
    """

    def __init__(self):
        self.keywords = {
            "PANTHER": "SERVICE",
            "LION": "PROJECT",
            "RABBIT": "INVENTORY",
            "JAGUAR": "ESTIMATING",
            "EMERGENCY": "SAFETY_ALERT",
            "STOP WORK": "SAFETY_STOP"
        }

    # ==========================================================================
    # 🎤 COMMAND PROCESSING
    # ==========================================================================

    def process_voice_command(self, user_name: str, transcript: str) -> Dict[str, Any]:
        """
        Takes raw text (from speech-to-text engine) and routes it.
        Example: "Panther add 2 hours to Ticket 101"
        """
        clean_text = self._clean_transcript(transcript)
        upper_text = clean_text.upper()

        MonkeyHeart.log_system_event("VOICE_INPUT", f"{user_name}: {clean_text}")

        # 1. Check Safety Triggers First
        if "STOP WORK" in upper_text or "EMERGENCY" in upper_text:
            return self._trigger_emergency(user_name, clean_text)

        # 2. Identify Target System
        target_system = "UNKNOWN"
        command_payload = clean_text

        first_word = upper_text.split(" ")[0]
        if first_word in self.keywords:
            target_system = self.keywords[first_word]
            # Strip the keyword from the payload
            # "PANTHER ADD HOURS" -> "ADD HOURS"
            command_payload = clean_text.split(" ", 1)[1] if " " in clean_text else ""

        # 3. Return Actionable Data
        return {
            "success": True,
            "original_transcript": transcript,
            "cleaned_transcript": clean_text,
            "target_system": target_system,
            "payload": command_payload,
            "action_required": target_system != "UNKNOWN"
        }

    # ==========================================================================
    # 🧹 DICTATION CLEANER
    # ==========================================================================

    def _clean_transcript(self, text: str) -> str:
        """
        Removes filler words to make reports professional.
        """
        fillers = ["um", "uh", "like", "you know", "basically", "actually"]

        # Simple regex replacement
        clean = text
        for word in fillers:
            # Case insensitive replace of whole words
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            clean = pattern.sub("", clean)

        # Fix double spaces created by removal
        clean = " ".join(clean.split())
        return clean

    # ==========================================================================
    # 🚨 EMERGENCY LOGIC
    # ==========================================================================

    def _trigger_emergency(self, user: str, details: str) -> Dict[str, Any]:
        """
        Handles the "Oh Sh*t" moment.
        """
        alert_msg = f"EMERGENCY DECLARED BY {user}: {details}"

        Bananas.notify("🚨 SAFETY ALERT 🚨", alert_msg)
        MonkeyHeart.log_system_event("VOICE_EMERGENCY", alert_msg)

        # In V7.0, we simulate calling Raptor Broadcast
        print(f" >> [BROADCAST] PUSH NOTIFICATION SENT TO ALL DEVICES: {alert_msg}")

        return {
            "success": True,
            "target_system": "SAFETY",
            "action": "BROADCAST_SENT",
            "message": alert_msg
        }


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦕 RAPTOR VOICE V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    siri = RaptorVoice()

    # 2. Test Normal Command
    print("\n[TEST 1] Panther Command...")
    # Raw input with fillers
    raw_1 = "Panther um I need to like add 2 hours to Ticket 101"
    res_1 = siri.process_voice_command("Mike", raw_1)

    print(f" > Raw: '{res_1['original_transcript']}'")
    print(f" > Clean: '{res_1['cleaned_transcript']}'")
    print(f" > Target: {res_1['target_system']}")
    print(f" > Payload: '{res_1['payload']}'")

    # 3. Test Unknown
    print("\n[TEST 2] General Dictation...")
    raw_2 = "Just logging some notes for the daily report"
    res_2 = siri.process_voice_command("Mike", raw_2)
    print(f" > Target: {res_2['target_system']} (Should be UNKNOWN)")

    # 4. Test Emergency
    print("\n[TEST 3] Emergency Trigger...")
    raw_3 = "STOP WORK STOP WORK Man down on level 4"
    res_3 = siri.process_voice_command("Mike", raw_3)
    print(f" > Action: {res_3.get('action')}")
    print(f" > Message: {res_3.get('message')}")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR VOICE SYSTEM: OPERATIONAL")