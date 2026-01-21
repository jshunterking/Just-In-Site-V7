from datetime import datetime
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class RabbitBilling:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for Revenue Capture.
    OXIDE DISSECTION: Automated G702/G703 style progress invoicing.
    Target: 100% Cash Flow Accuracy for Multi-Month Projects.
    """

    @staticmethod
    def initialize_billing_tables():
        """
        OXIDE: Dissects the database to support AIA-style billing periods.
        """
        conn = MonkeyBrain.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # BILLING_APPLICATIONS: The monthly "Apps for Payment"
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS billing_apps (
                    app_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id TEXT,
                    app_number INTEGER,
                    period_ending DATE,
                    work_completed_total REAL,
                    stored_materials REAL DEFAULT 0.0,
                    retainage_percent REAL DEFAULT 10.0,
                    status TEXT DEFAULT 'DRAFT', -- DRAFT, SUBMITTED, PAID
                    FOREIGN KEY(project_id) REFERENCES core_projects(project_id)
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            Bananas.report_collision(e, "BILLING_SCHEMA_CRASH")

    @staticmethod
    def create_pay_app(project_id, work_value, materials_value):
        """
        OXIDE: Generates a new progress billing application.
        Automatically calculates retainage to protect the 'Belly'.
        """
        try:
            # Calculate Retainage (standard 10% for Ohio construction)
            total_progress = work_value + materials_value
            retainage_amount = total_progress * 0.10
            net_billing = total_progress - retainage_amount

            cmd = """
                INSERT INTO billing_apps (project_id, work_completed_total, stored_materials, status)
                VALUES (?, ?, ?, 'DRAFT')
            """
            MonkeyBrain.execute_oxide(cmd, (project_id, work_value, materials_value))

            Bananas.notify("BILLING_DRAFTED", f"Pay App for {project_id} generated. Net: ${net_billing:,.2f}")
            return net_billing
        except Exception as e:
            Bananas.report_collision(e, "BILLING_GENERATION_FAILURE")
            return 0.0

    @staticmethod
    def get_financial_health(project_id):
        """
        Compares 'Billed to Date' vs 'Actual Costs' from the Brain/Belly.
        Target: Executive 'Buy-In' for over/under billing detection.
        """
        query = """
            SELECT SUM(work_completed_total) as total_billed,
                   (SELECT SUM(hours_worked * 65) FROM labor_logs WHERE project_id = ?) as total_costs
            FROM billing_apps WHERE project_id = ?
        """
        return MonkeyBrain.query_oxide(query, (project_id, project_id))

    @staticmethod
    def finalize_billing_period(app_id):
        """
        OXIDE: Locks the billing application for submission to the client.
        """
        cmd = "UPDATE billing_apps SET status = 'SUBMITTED' WHERE app_id = ?"
        MonkeyBrain.execute_oxide(cmd, (app_id,))