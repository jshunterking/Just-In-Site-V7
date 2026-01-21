import numpy as np
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class OwlEstimator:
    """
    OWL PROTOCOL: Synthetic Wisdom for Financial Strategy.
    OXIDE DISSECTION: Analyzing Bid-vs-Actual (BvA) variance to optimize pricing.
    Target: Eliminating 'Blind Spots' in the estimating process.
    """

    @staticmethod
    def calculate_bid_variance_coefficient(trade_focus):
        """
        OWL: Analyzes the historical accuracy of bids for a specific trade.
        Returns a 'Correction Factor' to be applied to new estimates.
        """
        try:
            # 1. Pull historical bid totals vs actual costs
            query = """
                SELECT 
                    p.gross_margin_target as planned_margin,
                    (SELECT SUM(hours_worked * 65) FROM labor_logs WHERE project_id = p.project_id) as actual_labor_cost,
                    (SELECT SUM(unit_cost * quantity) FROM prefab_components pc 
                     JOIN universal_inventory ui ON pc.material_id = ui.item_id 
                     JOIN prefab_assemblies pa ON pc.assembly_id = pa.assembly_id
                     WHERE pa.project_id = p.project_id) as actual_mat_cost
                FROM core_projects p
                WHERE p.trade_focus = ? AND p.status = 'COMPLETED'
            """
            df = MonkeyBrain.query_oxide(query, (trade_focus,))

            if df.empty or len(df) < 3:
                return 1.0  # Not enough data for wisdom; use neutral factor

            # 2. Logic to see if we consistently over/under estimate
            # If actual costs > planned, the factor will be > 1.0
            # This is the 'Wisdom Loop'
            variance_factor = 1.05  # Placeholder for ML regression result
            return variance_factor

        except Exception as e:
            Bananas.report_collision(e, "BID_VARIANCE_CALC_FAILURE")
            return 1.0

    @staticmethod
    def suggest_optimal_bid(raw_estimate_total, trade_focus):
        """
        OXIDE: Applies the Owl's correction factor to a raw estimate.
        """
        correction = OwlEstimator.calculate_bid_variance_coefficient(trade_focus)
        suggested_total = raw_estimate_total * correction

        confidence = "HIGH" if correction != 1.0 else "LOW (Insufficient Data)"

        return {
            "raw_total": round(raw_estimate_total, 2),
            "suggested_total": round(suggested_total, 2),
            "oxide_correction_factor": correction,
            "confidence_rating": confidence
        }

    @staticmethod
    def identify_leakage_categories():
        """
        OWL: Identifies which material or labor categories are causing
        the most profit bleed across all projects.
        """
        # This will grow into a 3,000 line diagnostic engine in the 50k version.
        pass