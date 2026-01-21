from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class RabbitEstimation:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for Commercial Bidding.
    OXIDE DISSECTION: Aggregating Materials, Labor, Overhead, and Profit.
    Target: 22nd-Century Bid Precision.
    """

    @staticmethod
    def calculate_total_bid(project_id, overhead_percent=15.0, profit_percent=10.0):
        """
        OXIDE: Dissects the total cost of a project by aggregating components.
        Formula: (Materials + Labor) * Overhead * Profit
        """
        try:
            # 1. GRIP MATERIAL TOTALS (Arms/Belly integration)
            # Pulls all materials linked to this project's takeoff
            mat_query = """
                SELECT SUM(unit_cost * quantity) as total_mat 
                FROM universal_inventory ui
                JOIN prefab_components pc ON ui.item_id = pc.material_id
                JOIN prefab_assemblies pa ON pc.assembly_id = pa.assembly_id
                WHERE pa.project_id = ?
            """
            mat_df = MonkeyBrain.query_oxide(mat_query, (project_id,))
            material_cost = mat_df['total_mat'].iloc[0] if not mat_df['total_mat'].isna().all() else 0.0

            # 2. CALCULATE LABOR BURDEN
            # Pulls estimated shop and field hours
            lab_query = "SELECT SUM(est_shop_hours) as total_hours FROM prefab_assemblies WHERE project_id = ?"
            lab_df = MonkeyBrain.query_oxide(lab_query, (project_id,))
            total_hours = lab_df['total_hours'].iloc[0] if not lab_df['total_hours'].isna().all() else 0.0

            # Regional Ohio Labor Rate (Hardcoded for now - move to config in future blocks)
            labor_cost = total_hours * 65.00

            # 3. APPLY OVERHEAD AND PROFIT
            subtotal = material_cost + labor_cost
            overhead_val = subtotal * (overhead_percent / 100)
            profit_val = (subtotal + overhead_val) * (profit_percent / 100)
            final_bid = subtotal + overhead_val + profit_val

            return {
                "project_id": project_id,
                "material_total": round(material_cost, 2),
                "labor_total": round(labor_cost, 2),
                "overhead_applied": round(overhead_val, 2),
                "target_profit": round(profit_val, 2),
                "final_bid_price": round(final_bid, 2),
                "margin_check": "HEALTHY" if profit_percent >= 10 else "RISK"
            }

        except Exception as e:
            Bananas.report_collision(e, "ESTIMATION_CALCULATION_FAILURE")
            return None

    @staticmethod
    def generate_bid_summary(bid_data):
        """
        OXIDE: Visualizes the bid dissection for the Executive Dashboard.
        """
        import streamlit as st
        st.markdown(f"### BID RECAP // PROJECT: {bid_data['project_id']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("DIRECT COSTS", f"${bid_data['material_total'] + bid_data['labor_total']:,}")
        c2.metric("OVERHEAD", f"${bid_data['overhead_applied']:,}")
        c3.metric("FINAL PROPOSAL", f"${bid_data['final_bid_price']:,}", delta=f"{bid_data['target_profit']} PROFIT")