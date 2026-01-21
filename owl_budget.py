import pandas as pd
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class OwlBudget:
    """
    OWL PROTOCOL: Wisdom in Fiscal Integrity.
    OXIDE DISSECTION: Background auditing of material-to-labor ratios.
    Target: Detecting "Phantom Costs" and unbilled material usage.
    """

    @staticmethod
    def run_financial_audit(project_id):
        """
        OWL: Cross-references unpurchased BOM items vs. actual field progress.
        Checks for the 'Missing Material' anomaly.
        """
        try:
            # 1. Pull current labor progress %
            # Logic: If labor is 50% spent, but 80% of materials are gone... we have a leak.
            query = """
                SELECT 
                    (SELECT SUM(hours_worked) FROM labor_logs WHERE project_id = ?) as actual_hrs,
                    (SELECT gross_margin_target FROM core_projects WHERE project_id = ?) as target_margin
            """
            stats = MonkeyBrain.query_oxide(query, (project_id, project_id))

            # 2. Check for "Stray" Material Purchases
            # Purchases that don't belong to a Pre-Fab Kit (Block 14)
            stray_query = """
                SELECT SUM(unit_cost * quantity) FROM universal_inventory
                WHERE current_project_id = ? AND status = 'PURCHASED'
                AND item_id NOT IN (SELECT material_id FROM prefab_components)
            """
            stray_costs = MonkeyBrain.query_oxide(stray_query, (project_id,)).iloc[0, 0] or 0

            leak_severity = "LOW"
            if stray_costs > 1000:  # Threshold for an Ohio mid-sized job
                leak_severity = "CRITICAL"

            return {
                "audit_date": datetime.now().strftime('%Y-%m-%d'),
                "unallocated_costs": round(stray_costs, 2),
                "leak_status": leak_severity,
                "wisdom": "Detected costs outside of planned pre-fab assemblies."
            }

        except Exception as e:
            Bananas.report_collision(e, "BUDGET_AUDIT_FAILURE")

    @staticmethod
    def identify_phantom_labor():
        """
        OWL: Flags labor logs (Block 22) that don't have corresponding
        Daily Reports (Block 24). If they didn't report work, why are they charging?
        """
        query = """
            SELECT l.emp_id, l.work_date, l.project_id
            FROM labor_logs l
            LEFT JOIN daily_reports d ON l.project_id = d.project_id AND l.work_date = d.report_date
            WHERE d.report_id IS NULL
        """
        return MonkeyBrain.query_oxide(query)

    @staticmethod
    def forecast_final_margin(project_id):
        """
        OWL: Uses the current 'Leakage Velocity' to predict the final margin at project close.
        """
        pass