import pandas as pd
from datetime import datetime
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class MonkeyLegs:
    """
    LOGISTICS: The mobility of the system from the warehouse to the site.
    OXIDE PROTOCOL: Tracking manifests, delivery status, and field arrivals.
    Target: 50,000-line Supply Chain Integrity.
    """

    @staticmethod
    def initialize_logistics_tables():
        """
        OXIDE: Dissects and builds the logistics tracking tables.
        """
        conn = MonkeyBrain.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # MANIFEST TABLE: Tracking the movement of 'Arms' (Materials)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logistics_manifests (
                    manifest_id TEXT PRIMARY KEY,
                    project_id TEXT,
                    driver_name TEXT,
                    vehicle_id TEXT,
                    status TEXT DEFAULT 'PENDING', -- PENDING, EN_ROUTE, DELIVERED
                    timestamp_departure DATETIME,
                    timestamp_arrival DATETIME,
                    FOREIGN KEY(project_id) REFERENCES core_projects(project_id)
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            Bananas.report_collision(e, "LOGISTICS_SCHEMA_CRASH")

    @staticmethod
    def deploy_delivery(project_id, driver, vehicle):
        """
        OXIDE: Initiates a physical movement event.
        Returns a Manifest ID for tracking.
        """
        manifest_id = f"TRK-{datetime.now().strftime('%m%d%y')}-{project_id[:4]}"

        try:
            cmd = """
                INSERT INTO logistics_manifests (manifest_id, project_id, driver_name, vehicle_id, timestamp_departure)
                VALUES (?, ?, ?, ?, ?)
            """
            MonkeyBrain.execute_oxide(cmd, (manifest_id, project_id, driver, vehicle, datetime.now()))

            MonkeyHeart.log_system_event("DELIVERY_DEPLOYED", f"Manifest: {manifest_id} | Driver: {driver}")
            return manifest_id

        except Exception as e:
            Bananas.report_collision(e, "LEGS_DEPLOYMENT_FAILURE")
            return None

    @staticmethod
    def get_fleet_pulse():
        """
        Retrieves real-time status of all field movements.
        Target: Executive 'Buy-In' Dashboard.
        """
        query = "SELECT * FROM logistics_manifests WHERE status != 'DELIVERED'"
        return MonkeyBrain.query_oxide(query)

    @staticmethod
    def confirm_arrival(manifest_id):
        """
        Closes the loop on a delivery event.
        """
        cmd = "UPDATE logistics_manifests SET status = 'DELIVERED', timestamp_arrival = ? WHERE manifest_id = ?"
        MonkeyBrain.execute_oxide(cmd, (datetime.now(), manifest_id))

        Bananas.notify("DELIVERY_CONFIRMED", f"Manifest {manifest_id} successfully landed.")