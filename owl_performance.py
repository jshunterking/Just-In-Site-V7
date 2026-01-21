import pandas as pd
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class OwlPerformance:
    """
    OWL PROTOCOL: Wisdom in Human Capital.
    OXIDE DISSECTION: Benchmarking field production against estimating standards.
    Target: Identifying top-performing crews and optimizing labor placement.
    """

    @staticmethod
    def calculate_production_efficiency(emp_id):
        """
        OWL: Compares the 'Earned Value' of a worker's tasks
        against the 'Actual Hours' logged.
        """
        try:
            # 1. Get Actual Hours (Block 22)
            actual_query = "SELECT SUM(hours_worked) FROM labor_logs WHERE emp_id = ?"
            actual_hrs = MonkeyBrain.query_oxide(actual_query, (emp_id,)).iloc[0, 0] or 0

            if actual_hrs == 0: return {"score": 0, "status": "INSUFFICIENT_DATA"}

            # 2. Get Earned Hours (Estimated hours for completed tasks)
            # This links to the 'Belly' and the 'Rabbit_Estimation' (Block 15)
            earned_query = """
                SELECT SUM(pa.est_shop_hours) 
                FROM prefab_assemblies pa
                JOIN labor_logs l ON pa.project_id = l.project_id
                WHERE l.emp_id = ? AND pa.status = 'COMPLETED'
            """
            earned_hrs = MonkeyBrain.query_oxide(earned_query, (emp_id,)).iloc[0, 0] or 0

            # 3. Efficiency Ratio ( > 1.0 means they are beating the bid)
            efficiency_ratio = round(earned_hrs / actual_hrs, 2)

            return {
                "emp_id": emp_id,
                "efficiency_ratio": efficiency_ratio,
                "tier": "A-PLAYER" if efficiency_ratio >= 1.1 else "STANDARD",
                "wisdom": "Beating the estimate" if efficiency_ratio > 1.0 else "Needs Review"
            }

        except Exception as e:
            Bananas.report_collision(e, "PERFORMANCE_CALC_FAILURE")

    @staticmethod
    def rank_foremen_by_margin(limit=5):
        """
        OWL: Ranks the top Foremen based on the actual Gross Margin
        of the projects they've closed out (Block 28).
        """
        query = """
            SELECT e.full_name, AVG(p.gross_margin_target) as avg_margin
            FROM employee_roster e
            JOIN core_projects p ON e.emp_id = p.lead_foreman_id
            WHERE p.status = 'COMPLETED'
            GROUP BY e.full_name
            ORDER BY avg_margin DESC
            LIMIT ?
        """
        return MonkeyBrain.query_oxide(query, (limit,))

    @staticmethod
    def identify_training_gaps(trade_focus):
        """
        OWL: Finds crews with consistently low efficiency in specific trades
        to suggest targeted training (e.g., Conduit Bending or Fire Alarm).
        """
        pass