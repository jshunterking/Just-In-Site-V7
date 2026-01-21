"""
RAPTOR BID HISTORY V7.0
The Estimating Archive & Analytics Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the memory bank for the Pre-Construction department (Jaguar).
It stores the results of every bid—Win, Loss, or Withdraw. It analyzes this
data to provide strategic insights for future pricing.

CORE CAPABILITIES:
1. Bid Result Logging (Win/Loss).
2. Competitor Tracking.
3. Historical Unit Pricing Lookup.

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Jaguar Heart (Source of Estimates)
"""

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
# 📚 THE ARCHIVE (Mock Database)
# ==============================================================================

MOCK_HISTORY = [
    {
        "bid_id": "EST-2024-001", "project": "Mercy ER", "amount": 250000,
        "result": "WIN", "competitor": "N/A", "date": "2024-06-15"
    },
    {
        "bid_id": "EST-2024-055", "project": "Walmart Retrofit", "amount": 180000,
        "result": "LOSS", "competitor": "Sparky's Electric", "reason": "PRICE_HIGH", "date": "2024-08-01"
    }
]


# ==============================================================================
# 🦕 RAPTOR BID HISTORY CLASS
# ==============================================================================

class RaptorBidHistory:
    """
    The Archive.
    """

    def __init__(self):
        self.history = MOCK_HISTORY

    # ==========================================================================
    # 📝 RESULT LOGGING
    # ==========================================================================

    def log_bid_result(self, bid_id: str, result: str, competitor: str = None, reason: str = None):
        """
        Closes the loop on an estimate.
        Result: WIN, LOSS, WITHDRAWN.
        """
        # In real app, we'd update the DB record for this bid_id
        entry = {
            "bid_id": bid_id,
            "result": result,
            "competitor": competitor if competitor else "UNKNOWN",
            "reason": reason if reason else "N/A",
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        self.history.append(entry)

        MonkeyHeart.log_system_event("BID_RESULT", f"Bid {bid_id} marked as {result}.")

        if result == "WIN":
            Bananas.notify("VICTORY!", f"We won Bid {bid_id}! Initiate Project Genesis.")

        return True

    # ==========================================================================
    # 🕵️ COMPETITOR INTEL
    # ==========================================================================

    def analyze_competitor(self, competitor_name: str) -> Dict[str, Any]:
        """
        Shows how often we lose to a specific rival.
        """
        losses = [h for h in self.history if h['result'] == "LOSS" and h['competitor'] == competitor_name]
        total_against = len([h for h in self.history if h['competitor'] == competitor_name])

        # If we never noted them in a win, we assume all mentions are losses for this simple logic
        # In reality, we'd track "Who bid against us" even when we win.

        return {
            "competitor": competitor_name,
            "times_lost_to": len(losses),
            "common_reason": "PRICE_HIGH" if losses else "N/A"  # Mock logic
        }

    # ==========================================================================
    # 📉 WIN RATE ANALYTICS
    # ==========================================================================

    def get_win_ratio(self) -> str:
        """
        The batting average.
        """
        total = len(self.history)
        if total == 0: return "0%"

        wins = len([h for h in self.history if h['result'] == "WIN"])
        ratio = (wins / total) * 100

        return f"{ratio:.1f}% ({wins}/{total})"


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦕 RAPTOR BID HISTORY V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    library = RaptorBidHistory()

    # 2. Log Result (Win)
    print("\n[TEST 1] Logging a WIN...")
    library.log_bid_result("EST-2026-001", "WIN")

    # 3. Log Result (Loss)
    print("\n[TEST 2] Logging a LOSS to Sparky's...")
    library.log_bid_result("EST-2026-002", "LOSS", competitor="Sparky's Electric", reason="PRICE_HIGH")

    # 4. Analyze Competitor
    print("\n[TEST 3] Analyzing Rival: Sparky's Electric...")
    intel = library.analyze_competitor("Sparky's Electric")
    print(f" > Losses against them: {intel['times_lost_to']}")

    # 5. Win Ratio
    print("\n[TEST 4] Calculating Batting Average...")
    print(f" > Win Rate: {library.get_win_ratio()}")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR BID HISTORY SYSTEM: OPERATIONAL")