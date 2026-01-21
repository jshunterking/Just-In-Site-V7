"""
OWL BIDS V7.0
The Strategic Intelligence & Analytics Engine for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the "Coach" for the Estimating Department (Jaguar).
It analyzes historical bid data to predict future outcomes. It answers the
critical question: "Should we bid this, and what margin should we use?"

CORE CAPABILITIES:
1. Win Probability Prediction (0-100%).
2. Competitor Analysis (Know thy enemy).
3. Bid Strategy Recommendation (Margin adjustment).

INTEGRATIONS:
- Bananas (Error Handling)
- Monkey Heart (Logging)
"""

import statistics
import random
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple

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
# 📚 THE HISTORICAL ARCHIVE (Training Data)
# ==============================================================================
# In production, this is queried from 'monkey_brain.db'.
# For V7.0, we use a rich mock dataset to demonstrate the logic.

MOCK_BID_HISTORY = [
    {"id": "B-001", "client": "MERCY HEALTH", "type": "HOSPITAL", "value": 150000, "margin": 15, "outcome": "WON",
     "competitor": "N/A"},
    {"id": "B-002", "client": "MERCY HEALTH", "type": "CLINIC", "value": 45000, "margin": 18, "outcome": "WON",
     "competitor": "N/A"},
    {"id": "B-003", "client": "OHIO STATE", "type": "SCHOOL", "value": 2500000, "margin": 10, "outcome": "LOST",
     "competitor": "ZENITH ELECTRIC"},
    {"id": "B-004", "client": "TARGET CORP", "type": "RETAIL", "value": 85000, "margin": 12, "outcome": "LOST",
     "competitor": "BUDGET ELECTRIC"},
    {"id": "B-005", "client": "MERCY HEALTH", "type": "HOSPITAL", "value": 300000, "margin": 14, "outcome": "WON",
     "competitor": "N/A"},
    {"id": "B-006", "client": "OHIO STATE", "type": "DORM", "value": 1200000, "margin": 8, "outcome": "LOST",
     "competitor": "ZENITH ELECTRIC"},
    {"id": "B-007", "client": "LOCAL DINER", "type": "RETAIL", "value": 12000, "margin": 25, "outcome": "WON",
     "competitor": "N/A"},
    {"id": "B-008", "client": "FACTORY INC", "type": "INDUSTRIAL", "value": 500000, "margin": 20, "outcome": "WON",
     "competitor": "N/A"},
]


# ==============================================================================
# 🦉 OWL BIDS CLASS
# ==============================================================================

class OwlBids:
    """
    The Strategy Engine.

    ATTRIBUTES:
        min_margin_limit (int): The absolute floor we will not bid below (e.g., 5%).
    """

    def __init__(self, min_margin_limit: int = 5):
        self.min_margin_limit = min_margin_limit
        self.history = MOCK_BID_HISTORY

    # ==========================================================================
    # 🔮 THE ORACLE (Win Probability)
    # ==========================================================================

    def predict_win_probability(self, client: str, job_type: str, est_value: int) -> Dict[str, Any]:
        """
        Calculates the likelihood of winning based on 3 factors:
        1. Client Relationship (Do we usually win with them?)
        2. Job Type Expertise (Are we good at Hospitals?)
        3. Job Size (is it too big/small for us?)
        """
        MonkeyHeart.log_system_event("STRATEGY", f"Analyzing Bid: {client} - {job_type}")

        score = 50.0  # Base Probability
        factors = []

        # 1. CLIENT FACTOR
        client_wins = [b for b in self.history if b['client'] == client and b['outcome'] == 'WON']
        client_total = [b for b in self.history if b['client'] == client]

        if client_total:
            win_rate = len(client_wins) / len(client_total)
            if win_rate > 0.7:
                score += 20
                factors.append("Strong Client Relationship (+20)")
            elif win_rate < 0.3:
                score -= 15
                factors.append("Poor Client History (-15)")
        else:
            factors.append("New Client (Neutral)")

        # 2. SECTOR FACTOR
        sector_wins = [b for b in self.history if b['type'] == job_type and b['outcome'] == 'WON']
        if len(sector_wins) >= 2:
            score += 15
            factors.append(f"Expertise in {job_type} (+15)")

        # 3. SIZE FACTOR
        # Just-In-Site Sweet Spot: $10k - $500k
        if 10000 <= est_value <= 500000:
            score += 10
            factors.append("Value in Sweet Spot (+10)")
        elif est_value > 2000000:
            score -= 20
            factors.append("High Value / High Risk (-20)")

        # Clamp Score
        final_score = min(99, max(1, score))

        # Determine "Traffic Light" Status
        status = "YELLOW"
        if final_score > 75:
            status = "GREEN"
        elif final_score < 30:
            status = "RED"

        return {
            "probability": round(final_score, 1),
            "status": status,
            "factors": factors
        }

    # ==========================================================================
    # 🕵️ COMPETITOR INTEL (The Spy)
    # ==========================================================================

    def analyze_competitor(self, competitor_name: str) -> str:
        """
        Returns a dossier on a specific rival.
        """
        losses = [b for b in self.history if b['competitor'] == competitor_name]

        if not losses:
            return "UNKNOWN ENTITY. No history of losses against this rival."

        count = len(losses)
        avg_loss_value = statistics.mean([b['value'] for b in losses])

        return f"DANGEROUS. We have lost {count} jobs to {competitor_name}. Avg Value: ${avg_loss_value:,.2f}. They tend to underbid us on large School/Gov projects."

    # ==========================================================================
    # 🧠 STRATEGY ADVISOR (The Coach)
    # ==========================================================================

    def suggest_bid_strategy(self, base_cost: float, probability_report: Dict) -> Dict:
        """
        Recommends a Margin % based on the Probability Score.
        """
        prob = probability_report['probability']
        base_margin = 15.0  # Standard target

        recommendation = ""
        suggested_margin = base_margin

        if prob >= 80:
            # We are strong. Bid high to maximize profit.
            suggested_margin = 20.0
            recommendation = "DOMINANT POSITION. Increase margin to 20%. Client pays for quality."

        elif 50 <= prob < 80:
            # Standard battle.
            suggested_margin = 15.0
            recommendation = "STANDARD PLAY. Stick to 15%. Don't leave money on the table."

        elif 30 <= prob < 50:
            # We are weak. Cut margin if we really want it.
            suggested_margin = 10.0
            recommendation = "WEAK POSITION. If you need this job to feed the guys, cut to 10%. Otherwise, walk away."

        else:
            # Walk away.
            suggested_margin = 25.0  # Pricing ourselves out intentionally
            recommendation = "DO NOT BID. Probability too low. Submit high 'Courtesy Bid' only."

        # Calculate Final Number
        sell_price = base_cost / (1 - (suggested_margin / 100))

        return {
            "suggested_margin": suggested_margin,
            "sell_price": round(sell_price, 2),
            "profit": round(sell_price - base_cost, 2),
            "strategy_note": recommendation
        }


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦉 OWL BIDS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    strategist = OwlBids()

    # 2. Test Prediction (Mercy Hospital - Strong)
    print("\n[TEST 1] Analyzing 'Mercy Hospital' Bid ($200k)...")
    report_a = strategist.predict_win_probability("MERCY HEALTH", "HOSPITAL", 200000)
    print(f" > Probability: {report_a['probability']}% ({report_a['status']})")
    print(f" > Factors: {report_a['factors']}")

    # 3. Test Prediction (Huge School - Weak)
    print("\n[TEST 2] Analyzing 'Mega School' Bid ($3M)...")
    report_b = strategist.predict_win_probability("UNKNOWN SCHOOL", "SCHOOL", 3000000)
    print(f" > Probability: {report_b['probability']}% ({report_b['status']})")

    # 4. Test Strategy
    print("\n[TEST 3] Generating Strategy for Mercy Bid (Cost $180k)...")
    strat = strategist.suggest_bid_strategy(180000, report_a)
    print(f" > Recommendation: {strat['strategy_note']}")
    print(f" > Target Margin: {strat['suggested_margin']}%")
    print(f" > Sell Price: ${strat['sell_price']:,}")

    # 5. Competitor Check
    print("\n[TEST 4] Intel on 'Zenith Electric'...")
    intel = strategist.analyze_competitor("ZENITH ELECTRIC")
    print(f" > {intel}")

    print("\n" + "=" * 40)
    print("🦉 OWL BIDS SYSTEM: OPERATIONAL")