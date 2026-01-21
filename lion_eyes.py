"""
LION EYES V7.0
The Business Intelligence & Analytics Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module provides the "Vision" for the Project Manager. While the Spine
holds the data, the Eyes interpret it. It is responsible for Forecasting,
Variance Analysis, and visual reporting.

CORE CAPABILITIES:
1. Cost At Completion (CAC) Forecasting.
2. Variance Analysis (Budget vs Actual by Phase).
3. Executive Summary Generation.

INTEGRATIONS:
- Bananas (Alerts)
- Monkey Heart (Data Source)
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
# 🧿 THE DATA FEED (Mock Financials)
# ==============================================================================

MOCK_FINANCIALS = {
    "JOB-26001": {
        "budget_total": 100000.00,
        "spent_total": 45000.00,
        "percent_complete": 40.0,  # Physical completion reported by field
        "phases": [
            {"code": "ROUGH", "budget": 40000, "spent": 38000, "complete_pct": 90},  # Bad: Overspending
            {"code": "WIRE", "budget": 30000, "spent": 5000, "complete_pct": 20},  # Good
            {"code": "FINISH", "budget": 30000, "spent": 2000, "complete_pct": 5}
        ]
    }
}


# ==============================================================================
# 🦁 LION EYES CLASS
# ==============================================================================

class LionEyes:
    """
    The Analyst.
    """

    def __init__(self):
        self.data = MOCK_FINANCIALS

    # ==========================================================================
    # 🔮 THE CRYSTAL BALL (Forecasting)
    # ==========================================================================

    def predict_outcome(self, job_id: str) -> Dict[str, Any]:
        """
        Calculates Cost At Completion (CAC) based on current performance.

        Formula: CAC = Spent / Percent Complete
        (If we spent $45k to get 40% done, 100% will cost $112.5k)
        """
        job = self.data.get(job_id)
        if not job:
            return {"error": "Job not found"}

        spent = job['spent_total']
        pct = job['percent_complete'] / 100.0
        budget = job['budget_total']

        if pct == 0:
            return {"cac": budget, "variance": 0, "status": "JUST_STARTED"}

        # Forecast
        cac = spent / pct
        variance = budget - cac

        status = "ON_TARGET"
        if variance < -5000:
            status = "PROJECTED_LOSS"
        elif variance > 5000:
            status = "PROJECTED_PROFIT"

        MonkeyHeart.log_system_event("LION_FORECAST", f"Forecast for {job_id}: CAC ${cac:,.2f} (Var: ${variance:,.2f})")

        return {
            "job_id": job_id,
            "original_budget": budget,
            "current_spend": spent,
            "physical_percent": job['percent_complete'],
            "forecast_final_cost": round(cac, 2),
            "projected_variance": round(variance, 2),
            "status": status
        }

    # ==========================================================================
    # 🔥 THE HEATMAP (Variance Analysis)
    # ==========================================================================

    def analyze_phases(self, job_id: str) -> List[Dict]:
        """
        Looks at specific cost codes to see where the leak is.
        """
        job = self.data.get(job_id)
        if not job: return []

        analysis = []
        for phase in job['phases']:
            # Calculate Phase Performance
            # Expected Spend = Budget * % Complete
            expected_spend = phase['budget'] * (phase['complete_pct'] / 100.0)
            actual_spend = phase['spent']

            # Diff: If Actual > Expected, we are bleeding.
            diff = expected_spend - actual_spend

            health = "GREEN"
            if diff < -1000:
                health = "RED"  # Bleeding
            elif diff < 0:
                health = "YELLOW"

            analysis.append({
                "code": phase['code'],
                "budget": phase['budget'],
                "actual": actual_spend,
                "should_be_spent": round(expected_spend, 2),
                "variance": round(diff, 2),
                "health": health
            })

        return analysis

    # ==========================================================================
    # 📑 EXECUTIVE SNAPSHOT
    # ==========================================================================

    def get_executive_summary(self, job_id: str) -> str:
        """
        Generates a plain-english status report.
        """
        forecast = self.predict_outcome(job_id)
        phases = self.analyze_phases(job_id)

        # Identify problem areas
        red_flags = [p['code'] for p in phases if p['health'] == "RED"]

        summary = [
            f"EXECUTIVE SUMMARY: {job_id}",
            f"DATE: {datetime.now().strftime('%Y-%m-%d')}",
            "-" * 40,
            f"STATUS: {forecast['status'].replace('_', ' ')}",
            f"PROGRESS: {forecast['physical_percent']}% Complete",
            f"FINANCIALS: Spent ${forecast['current_spend']:,.0f} of ${forecast['original_budget']:,.0f}",
            f"FORECAST: Trending to finish at ${forecast['forecast_final_cost']:,.0f}",
            "-" * 40,
        ]

        if forecast['projected_variance'] < 0:
            summary.append(f"WARNING: Projected Overrun of ${abs(forecast['projected_variance']):,.0f}.")
        else:
            summary.append(f"GOOD NEWS: Projected Savings of ${forecast['projected_variance']:,.0f}.")

        if red_flags:
            summary.append(f"ATTENTION NEEDED: High costs detected in {', '.join(red_flags)}.")
        else:
            summary.append("OPERATIONS: All phases performing within tolerance.")

        return "\n".join(summary)


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦁 LION EYES V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    analyst = LionEyes()

    # 2. Test Forecast
    print("\n[TEST 1] Forecasting JOB-26001...")
    # Scenario: Budget 100k, Spent 45k, Progress 40%.
    # Pace is bad. 45k/0.4 = 112.5k CAC. Overrun 12.5k.
    res = analyst.predict_outcome("JOB-26001")
    print(f" > CAC: ${res['forecast_final_cost']:,.2f}")
    print(f" > Variance: ${res['projected_variance']:,.2f}")
    print(f" > Status: {res['status']}")

    # 3. Test Heatmap
    print("\n[TEST 2] Analyzing Phases...")
    # Rough-in: Budget 40k, Spent 38k, Progress 90%.
    # Should have spent 36k (40*0.9). Spent 38k. Variance -2k (RED).
    heatmap = analyst.analyze_phases("JOB-26001")
    for row in heatmap:
        print(f" > {row['code']}: {row['health']} (Var: ${row['variance']})")

    # 4. Executive Summary
    print("\n[TEST 3] Generating Report...")
    print(analyst.get_executive_summary("JOB-26001"))

    print("\n" + "=" * 40)
    print("🦁 LION EYES SYSTEM: OPERATIONAL")