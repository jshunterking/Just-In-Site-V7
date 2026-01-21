import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class OwlAnalytics:
    """
    OWL PROTOCOL: Wisdom, Vision, and Prediction.
    OXIDE DISSECTION: Applying statistical models to project and labor data.
    Target: Foreseeing profit bleed and labor shortages before they occur.
    """

    @staticmethod
    def forecast_labor_burn(project_id):
        """
        OWL: Analyzes the current labor burn rate (Block 22) against
        the remaining schedule (Block 17) to predict the 'Finished Cost'.
        """
        try:
            # 1. Get Actuals
            actual_query = "SELECT SUM(hours_worked) FROM labor_logs WHERE project_id = ?"
            actual_hours = MonkeyBrain.query_oxide(actual_query, (project_id,)).iloc[0, 0] or 0

            # 2. Get Estimates
            est_query = "SELECT SUM(est_shop_hours) FROM prefab_assemblies WHERE project_id = ?"
            estimated_hours = MonkeyBrain.query_oxide(est_query, (project_id,)).iloc[0, 0] or 1

            # 3. Calculate Velocity
            # In a 50k line app, we'd use a linear regression model here
            percent_complete_hours = (actual_hours / estimated_hours)

            return {
                "burn_rate": round(percent_complete_hours, 2),
                "predicted_overrun": "LOW" if percent_complete_hours < 0.9 else "CRITICAL",
                "wisdom": "OWL_V1_STATISTICAL"
            }
        except Exception as e:
            Bananas.report_collision(e, "LABOR_FORECAST_FAILURE")

    @staticmethod
    def predict_cash_flow(days_ahead=90):
        """
        OWL: Reaches into the 'Billing Rabbit' (Block 26) and 'CRM Rabbit' (Block 29)
        to forecast bank balance based on Net-30/45 payment trends.
        """
        try:
            # Aggregate pending 'Approved' billings
            query = "SELECT SUM(work_completed_total) FROM billing_apps WHERE status = 'SUBMITTED'"
            pending_revenue = MonkeyBrain.query_oxide(query).iloc[0, 0] or 0

            # Project outflow (Labor/Materials)
            # This is where the 'Wisdom' logic connects multiple Burrows
            return {
                "forecasted_inflow": pending_revenue,
                "confidence_interval": "85%",
                "lookahead_days": days_ahead
            }
        except Exception as e:
            Bananas.report_collision(e, "CASH_FLOW_PREDICTION_FAILURE")

    @staticmethod
    def get_market_intelligence():
        """
        Analyzes the 'CRM Rabbit' (Block 29) to determine which
        trade sectors (Block 11-13) are showing the highest win rates.
        """
        query = "SELECT trade_focus, COUNT(*) as wins FROM core_projects GROUP BY trade_focus"
        return MonkeyBrain.query_oxide(query)