"""
RAPTOR LEADS V7.0
The Business Development Engine for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the "Hunter." It scans external bid networks (simulated in V7.0)
to find new project opportunities. It applies a filtering logic to discard
irrelevant jobs (like plumbing) and highlights high-value Electrical targets.

CORE CAPABILITIES:
1. Scrape (Simulated) Bid Networks.
2. Filter by Trade (Electrical/Low Voltage).
3. Score Leads (Distance + Value).
4. Auto-Promote to "Estimating Pipeline."

INTEGRATIONS:
- Bananas (Error Handling)
- Monkey Heart (Logging)
- Raptor Maps (Distance Calculation)
"""

import time
import json
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional

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
# 🕸️ THE MOCK BID NETWORK (The Internet Simulation)
# ==============================================================================
# In a real app, we would use Beautiful Soup or Selenium here.
# For V7.0, we generate realistic Ohio-based construction leads.

OHIO_CITIES = [
    ("Youngstown", 10), ("Cleveland", 60), ("Akron", 45),
    ("Warren", 15), ("Boardman", 5), ("Columbus", 150), ("Canton", 55)
]

PROJECT_TYPES = [
    "Hospital Renovation", "High School Annex", "Retail Fit-Out",
    "Warehouse LED Retrofit", "Data Center New Build", "Apartment Complex",
    "Water Treatment Plant", "Fire Station No. 5"
]

TRADES =

TRADES = ["Electrical", "Plumbing", "HVAC", "General Construction", "Roofing"]


# ==============================================================================
# 🦖 RAPTOR LEADS CLASS
# ==============================================================================

class RaptorLeads:
    """
    The Lead Hunter.

    ATTRIBUTES:
        search_radius_miles (int): Max distance we are willing to travel.
        min_value (int): Minimum job size ($).
    """

    def __init__(self, search_radius_miles: int = 75, min_value: int = 10000):
        self.search_radius_miles = search_radius_miles
        self.min_value = min_value
        self.found_leads = []  # Temporary storage for the session

    def hunt_for_leads(self) -> List[Dict]:
        """
        Main execution method. Scans the 'internet' and returns filtered,
        scored leads.
        """
        MonkeyHeart.log_system_event("LEADS", "Initiating Hunt Protocol...")

        # 1. Simulate scraping delay
        time.sleep(2)

        # 2. Generate Raw Data (The Noise)
        raw_leads = self._simulate_network_traffic(count=20)

        # 3. Filter & Score (The Intelligence)
        qualified_leads = []
        for lead in raw_leads:
            if self._is_relevant(lead):
                score = self._calculate_score(lead)
                lead['score'] = score
                lead['status'] = 'NEW'
                qualified_leads.append(lead)

        # Sort by Score (Highest first)
        qualified_leads.sort(key=lambda x: x['score'], reverse=True)

        self.found_leads = qualified_leads
        MonkeyHeart.log_system_event("LEADS", f"Hunt Complete. Found {len(qualified_leads)} Targets.")

        if len(qualified_leads) > 0:
            Bananas.notify("Raptor Leads", f"Found {len(qualified_leads)} new Electrical jobs!")

        return qualified_leads

    def _simulate_network_traffic(self, count: int) -> List[Dict]:
        """
        Generates random noise (some electrical, some plumbing, some far away).
        """
        leads = []
        for _ in range(count):
            city, dist = random.choice(OHIO_CITIES)
            trade = random.choice(TRADES)

            # Weighted random value
            est_value = random.randint(5000, 5000000)

            lead = {
                "id": f"LEAD-{uuid.uuid4().hex[:6].upper()}",
                "title": f"{random.choice(PROJECT_TYPES)} - {trade} Package",
                "location": f"{city}, OH",
                "distance_miles": dist,
                "primary_trade": trade,
                "est_value": est_value,
                "due_date": (datetime.now() + timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d"),
                "source": random.choice(["Builders Exchange", "Blue Book", "Dodge Data"]),
                "description": "Full scope renovation including demo and new install."
            }
            leads.append(lead)
        return leads

    def _is_relevant(self, lead: Dict) -> bool:
        """
        The Filter. Returns True if we should look at this job.
        """
        # Rule 1: Trade must be Electrical
        if lead['primary_trade'] != "Electrical":
            return False

        # Rule 2: Must be within radius
        if lead['distance_miles'] > self.search_radius_miles:
            return False

        # Rule 3: Must be worth our time
        if lead['est_value'] < self.min_value:
            return False

        return True

    def _calculate_score(self, lead: Dict) -> int:
        """
        Assigns a 0-100 Score based on desirability.
        """
        score = 50  # Base score

        # Distance Penalty (Closer is better)
        if lead['distance_miles'] < 20:
            score += 20
        elif lead['distance_miles'] > 60:
            score -= 15

        # Value Bonus (Bigger is better, up to a point)
        if lead['est_value'] > 100000: score += 10
        if lead['est_value'] > 1000000: score += 10

        # Source Weight (We trust Builders Exchange more)
        if lead['source'] == "Builders Exchange": score += 5

        # Cap at 100
        return min(100, max(0, score))

    def promote_to_pipeline(self, lead_id: str) -> Dict:
        """
        Moves a lead from "Raw List" to "Active Estimate".
        This would trigger the Job Setup in 'monkey_brain'.
        """
        target = next((l for l in self.found_leads if l['id'] == lead_id), None)

        if target:
            target['status'] = 'PROMOTED'
            MonkeyHeart.log_system_event("LEADS", f"Promoted {target['title']} to Estimating.")
            return {
                "success": True,
                "job_name": target['title'],
                "est_value": target['est_value']
            }
        else:
            Bananas.report_collision("Lead ID not found in session", "promote_to_pipeline")
            return {"success": False}


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦖 RAPTOR LEADS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    hunter = RaptorLeads(search_radius_miles=80)

    # 2. Run Hunt
    print("\n[TEST 1] Scanning Ohio Networks...")
    targets = hunter.hunt_for_leads()

    # 3. Print Results
    print(f"\nFound {len(targets)} Relevant Targets:")
    for t in targets:
        print(f" > [{t['score']}/100] {t['title']} ({t['location']} - ${t['est_value']:,})")

    # 4. Test Promotion
    if targets:
        print("\n[TEST 2] Promoting Top Lead...")
        top_lead = targets[0]
        res = hunter.promote_to_pipeline(top_lead['id'])
        print(f" > Result: {res['success']} - New Estimate Created for '{res['job_name']}'")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR LEADS SYSTEM: OPERATIONAL")