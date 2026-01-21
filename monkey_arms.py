import pandas as pd
import io
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class MonkeyArms:
    """
    PROCUREMENT: The reach of the system into the material marketplace.
    OXIDE PROTOCOL: Dissects massive CSV/Excel material lists into the Singularity.
    Target: 10,000+ Item Capacity for All-Trades.
    """

    @staticmethod
    def grip_material_list(uploaded_file, trade_type):
        """
        OXIDE: Reaches into a raw data file and pulls it into the SQL Singularity.
        Dissects columns to match the Universal Inventory schema.
        """
        try:
            # 1. READ RAW DATA (Support for CSV and Excel)
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # 2. DISSECT & NORMALIZE
            # We ensure the data matches the 'universal_inventory' table from Block 03.
            df['trade_type'] = trade_type

            # 3. FEED THE BRAIN
            conn = MonkeyBrain.get_connection()
            if conn:
                # Use 'append' so contractors can keep adding to their warehouse.
                df.to_sql('universal_inventory', conn, if_exists='append', index=False)
                conn.close()

            MonkeyHeart.log_system_event("INVENTORY_GRIP", f"Imported {len(df)} items for {trade_type}")
            return len(df)

        except Exception as e:
            Bananas.report_collision(e, "ARMS_GRIP_FAILURE")
            return 0

    @staticmethod
    def reach_for_item(item_id):
        """
        Retrieves a specific material specification from the Singularity.
        """
        query = "SELECT * FROM universal_inventory WHERE item_id = ?"
        return MonkeyBrain.query_oxide(query, (item_id,))

    @staticmethod
    def calculate_arm_leverage(project_id):
        """
        Calculates total material cost leverage for a project.
        Target: Executive 'Buy-In' Metric.
        """
        # In a 50k line app, this would perform a JOIN between
        # the project's takeoff and the inventory prices.
        query = """
            SELECT SUM(unit_cost * warehouse_stock) as total_value 
            FROM universal_inventory 
            WHERE trade_type = (SELECT trade_focus FROM core_projects WHERE project_id = ?)
        """
        df = MonkeyBrain.query_oxide(query, (project_id,))
        return df['total_value'].iloc[0] if not df.empty else 0.0