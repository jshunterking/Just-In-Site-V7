"""
RAPTOR MARKETING V7.0
The Lead Generation & CRM Intelligence Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the "Top of Funnel." It tracks potential customers (Leads),
scores them based on value, and measures the effectiveness of advertising
campaigns. It ensures we aren't wasting money on ads that don't work.

CORE CAPABILITIES:
1. Lead Ingestion & Scoring.
2. Campaign ROI Analysis.
3. Automated Follow-Up (Drip).

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Logging)
- Panther Mouth (Revenue Validation)
"""

import time
import uuid
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
# 🎯 THE FUNNEL (Mock Database)
# ==============================================================================

MOCK_LEADS = [
    {"id": "L-001", "name": "Mercy Hospital Extension", "source": "REFERRAL", "value": 500000, "score": 95,
     "status": "NEGOTIATING"},
    {"id": "L-002", "name": "Mrs. Smith Ceiling Fan", "source": "FACEBOOK_AD", "value": 350, "score": 10,
     "status": "NEW"}
]

MOCK_CAMPAIGNS = {
    "FACEBOOK_AD": {"cost": 500.00, "revenue": 1200.00},
    "BILLBOARD_I80": {"cost": 2000.00, "revenue": 0.00}
}


# ==============================================================================
# 🦕 RAPTOR MARKETING CLASS
# ==============================================================================

class RaptorMarketing:
    """
    The Lure.
    """

    def __init__(self):
        self.leads = MOCK_LEADS
        self.campaigns = MOCK_CAMPAIGNS

    # ==========================================================================
    # 🎣 LEAD SCORING
    # ==========================================================================

    def ingest_lead(self, name: str, source: str, estimated_value: float) -> Dict[str, Any]:
        """
        Takes a raw inquiry and assigns a priority score.
        """
        # Score Logic
        score = 0
        if estimated_value > 100000:
            score += 50
        elif estimated_value > 1000:
            score += 20
        else:
            score += 5

        if source == "REFERRAL":
            score += 40
        elif source == "WEBSITE":
            score += 20

        # Create Lead
        lead_id = f"L-{len(self.leads) + 100}"
        new_lead = {
            "id": lead_id,
            "name": name,
            "source": source,
            "value": estimated_value,
            "score": score,
            "status": "NEW",
            "created_at": datetime.now().isoformat()
        }

        self.leads.append(new_lead)

        # Log
        MonkeyHeart.log_system_event("MARKETING_LEAD", f"New Lead: {name} (Score: {score})")

        if score > 80:
            Bananas.notify("HOT LEAD 🔥", f"{name} is a high-value target (${estimated_value:,.0f}).")

        return new_lead

    # ==========================================================================
    # 💰 CAMPAIGN ROI
    # ==========================================================================

    def get_campaign_performance(self) -> List[Dict]:
        """
        Analyzes which ads are making money.
        """
        report = []
        for name, data in self.campaigns.items():
            cost = data['cost']
            revenue = data['revenue']
            profit = revenue - cost
            roi = (profit / cost) * 100 if cost > 0 else 0

            status = "WINNER" if roi > 0 else "LOSER"

            report.append({
                "campaign": name,
                "spend": cost,
                "return": revenue,
                "roi_pct": round(roi, 1),
                "status": status
            })

        return report

    # ==========================================================================
    # 💧 THE DRIP (Automation)
    # ==========================================================================

    def run_drip_campaign(self) -> int:
        """
        Finds stale leads and sends follow-ups.
        """
        stale_count = 0
        # Mocking check for leads > 7 days old
        for lead in self.leads:
            if lead['status'] == "NEW" and lead['score'] < 50:  # Don't auto-drip huge clients, call them.
                # Simulate sending email
                print(f" >> [EMAIL BOT] Sending 'Just checking in' to {lead['name']}...")
                lead['status'] = "CONTACTED"
                stale_count += 1

        if stale_count > 0:
            MonkeyHeart.log_system_event("MARKETING_DRIP", f"Auto-emailed {stale_count} stale leads.")

        return stale_count


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦕 RAPTOR MARKETING V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    lure = RaptorMarketing()

    # 2. Test Ingest (Hot Lead)
    print("\n[TEST 1] Ingesting 'Walmart Retrofit' (Referral)...")
    hot = lure.ingest_lead("Walmart Retrofit", "REFERRAL", 250000)
    print(f" > Score: {hot['score']} (Status: {hot['status']})")

    # 3. Test Ingest (Cold Lead)
    print("\n[TEST 2] Ingesting 'Fix Doorbell' (Facebook)...")
    cold = lure.ingest_lead("Fix Doorbell", "FACEBOOK_AD", 150)
    print(f" > Score: {cold['score']}")

    # 4. Test ROI
    print("\n[TEST 3] Checking Campaign ROI...")
    stats = lure.get_campaign_performance()
    for camp in stats:
        print(f" > {camp['campaign']}: {camp['roi_pct']}% ROI ({camp['status']})")

    # 5. Test Drip
    print("\n[TEST 4] Running Drip Engine...")
    sent = lure.run_drip_campaign()
    print(f" > Emails Sent: {sent}")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR MARKETING SYSTEM: OPERATIONAL")