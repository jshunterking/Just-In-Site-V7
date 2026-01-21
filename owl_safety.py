import pandas as pd
from datetime import datetime
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas

class OwlSafety:
    """
    OWL PROTOCOL: Wisdom in Human Preservation.
    OXIDE DISSECTION: Predicting job site risk based on fatigue and environmental load.
    Target: Zero-Incident Culture through predictive intervention.
    """

    @staticmethod
    def calculate_site_risk_score(project_id):
        """
        OWL: Analyzes three core pillars of risk:
        1. Fatigue (Consecutive days worked / Overtime)
        2. Environment (Ohio Temperature Extremes)
        3. Compliance (Toolbox Talk Frequency)
        """
        try:
            # 1. Fatigue Analysis (Pulling from Block 22)
            labor_query = """
                SELECT hours_worked FROM labor_logs 
                WHERE project_id = ? AND work_date >= date('now', '-7 days')
            """
            hours_df = MonkeyBrain.query_oxide(labor_query, (project_id,))
            fatigue_factor = 1.0
            if not hours_df.empty:
                avg_hours = hours_df['hours_worked'].mean()
                if avg_hours > 10: fatigue_factor = 1.4 # High OT = High Risk

            # 2. Environmental Stress (Pulling from Block 24)
            weather_query = "SELECT weather_temp FROM daily_reports WHERE project_id = ? ORDER BY report_date DESC LIMIT 1"
            weather_df = MonkeyBrain.query_oxide(weather_query, (project_id,))
            temp_factor = 1.0
            if not weather_df.empty:
                temp_str = weather_df['weather_temp'].iloc[0]
                temp = int(''.join(filter(str.isdigit, temp_str)))
                if temp < 20 or temp > 95: temp_factor = 1.3 # Extreme cold/heat stress

            # 3. Compliance Pulse (Pulling from Block 18)
            safety_query = "SELECT COUNT(*) FROM compliance_records WHERE project_id = ? AND type = 'OSHA_TOOLBOX' AND last_updated >= date('now', '-7 days')"
            safety_meetings = MonkeyBrain.query_oxide(safety_query, (project_id,)).iloc[0,0]
            compliance_buffer = 0.8 if safety_meetings >= 5 else 1.2 # Frequent talks lower risk

            final_risk_score = round(10 * fatigue_factor * temp_factor * compliance_buffer, 1)

            return {
                "risk_score": final_risk_score, # 1-100 scale
                "threat_level": "ELEVATED" if final_risk_score > 15 else "STABLE",
                "primary_driver": "FATIGUE" if fatigue_factor > 1 else "ENVIRONMENTAL",
                "recommendation": "MANDATORY SAFETY STAND-DOWN" if final_risk_score > 20 else "CONTINUE OPS"
            }

        except Exception as e:
            Bananas.report_collision(e, "SAFETY_RISK_CALC_FAILURE")

    @staticmethod
    def identify_high_risk_workers():
        """
        OWL: Identifies individuals who have exceeded 60 hours in a 7-day period.
        Directly addresses the 'Fatigue Kill' statistics in construction.
        """
        query = """
            SELECT emp_id, SUM(hours_worked) as weekly_total 
            FROM labor_logs 
            WHERE work_date >= date('now', '-7 days')
            GROUP BY emp_id HAVING weekly_total > 60
        """
        return MonkeyBrain.query_oxide(query)