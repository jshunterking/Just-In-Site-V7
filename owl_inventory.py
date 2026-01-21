import pandas as pd
from datetime import datetime, timedelta
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class OwlInventory:
    """
    OWL PROTOCOL: Wisdom in Material Flow.
    OXIDE DISSECTION: Predicting stock depletion rates across the entire enterprise.
    Target: Just-In-Time (JIT) replenishment with zero project delays.
    """

    @staticmethod
    def predict_depletion_date(material_id):
        """
        OWL: Calculates the 'Burn Rate' of a specific material.
        Cross-references Warehouse Stock vs. All Active Pre-Fab BOMs.
        """
        try:
            # 1. Get current physical stock
            stock_query = "SELECT quantity FROM universal_inventory WHERE item_id = ?"
            current_stock = MonkeyBrain.query_oxide(stock_query, (material_id,)).iloc[0, 0] or 0

            # 2. Get total 'Committed' stock for upcoming Pre-Fab kits (Next 30 days)
            committed_query = """
                SELECT SUM(pc.quantity) 
                FROM prefab_components pc
                JOIN prefab_assemblies pa ON pc.assembly_id = pa.assembly_id
                WHERE pc.material_id = ? AND pa.status = 'QUEUED'
            """
            committed_stock = MonkeyBrain.query_oxide(committed_query, (material_id,)).iloc[0, 0] or 0

            # 3. Calculate the Gap
            net_stock = current_stock - committed_stock

            # 4. Generate Wisdom
            status = "STABLE"
            if net_stock < 0:
                status = "CRITICAL_SHORTAGE"
            elif net_stock < (current_stock * 0.2):
                status = "REORDER_RECO"

            return {
                "material_id": material_id,
                "current_on_hand": current_stock,
                "future_demand": committed_stock,
                "net_position": net_stock,
                "owl_verdict": status
            }

        except Exception as e:
            Bananas.report_collision(e, "INVENTORY_FORECAST_FAILURE")

    @staticmethod
    def generate_omni_order():
        """
        OWL: Scans all 'CRITICAL' and 'REORDER' materials to create a
        single Master Purchase Order for the whole company.
        """
        # This allows the contractor to buy 50,000ft of pipe at once
        # instead of 1,000ft for 50 different jobs.
        pass

    @staticmethod
    def identify_obsolete_stock():
        """
        OWL: Identifies items in the warehouse that haven't been
        assigned to a Pre-Fab kit in over 180 days.
        """
        # Helps the owner clear out "Dead Capital" from the shelves.
        pass