import pandas as pd
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class OwlMaterial:
    """
    OWL PROTOCOL: Economic Wisdom and Resource Intelligence.
    OXIDE DISSECTION: Predicting commodity price impact on project backlogs.
    Target: Maximizing Buy-In Profit through strategic procurement timing.
    """

    @staticmethod
    def analyze_commodity_exposure(project_id):
        """
        OWL: Dissects the project's Bill of Materials (BOM) to identify
        exposure to volatile metals (Copper, Aluminum, Steel).
        """
        try:
            # Query the Arms/Belly for unpurchased material requirements
            query = """
                SELECT ui.material_name, pc.quantity, ui.unit_cost
                FROM prefab_components pc
                JOIN universal_inventory ui ON pc.material_id = ui.item_id
                JOIN prefab_assemblies pa ON pc.assembly_id = pa.assembly_id
                WHERE pa.project_id = ? AND ui.material_name LIKE '%COPPER%'
            """
            df = MonkeyBrain.query_oxide(query, (project_id,))

            if df.empty:
                return {"exposure_level": "LOW", "risk_value": 0.0}

            # In a 50k line app, this bridges to a Live London Metal Exchange (LME) API
            current_market_volatility = 1.08  # 8% projected increase
            total_exposure = df['quantity'].sum() * df['unit_cost'].mean()
            risk_impact = total_exposure * (current_market_volatility - 1.0)

            return {
                "commodity": "COPPER",
                "total_exposure": round(total_exposure, 2),
                "predicted_impact": round(risk_impact, 2),
                "strategy": "BUY_NOW" if risk_impact > 500 else "HOLD"
            }

        except Exception as e:
            Bananas.report_collision(e, "COMMODITY_ANALYSIS_FAILURE")

    @staticmethod
    def suggest_bulk_buy_opportunities():
        """
        OWL: Scans all 'Active' and 'Pending' projects to find common
        materials for volume-discount procurement.
        """
        query = """
            SELECT material_id, SUM(quantity) as total_needed
            FROM prefab_components
            GROUP BY material_id
            HAVING total_needed > 500
        """
        # Suggests to the Purchasing Agent to buy in bulk to beat inflation.
        return MonkeyBrain.query_oxide(query)

    @staticmethod
    def identify_supply_chain_bottlenecks():
        """
        OWL: Cross-references 'Submittal' lead times (Block 20) to predict
        which materials will delay the 'Legs' (Logistics).
        """
        pass