from datetime import datetime
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class RabbitCRM:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for Market Intelligence.
    OXIDE DISSECTION: Tracking GCs, Architects, and Owners to find the 'Ideal Client'.
    Target: Data-driven bidding based on historical customer profitability.
    """

    @staticmethod
    def initialize_crm_tables():
        """
        OXIDE: Dissects the database to support client profiles and lead tracking.
        """
        conn = MonkeyBrain.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # CLIENT_DIRECTORY: The master list of companies you bid to
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS client_directory (
                    client_id TEXT PRIMARY KEY,
                    company_name TEXT,
                    client_type TEXT, -- GC, OWNER, ARCHITECT
                    primary_contact TEXT,
                    email TEXT,
                    payment_terms INTEGER DEFAULT 30, -- Net 30, 45, etc.
                    reliability_rating REAL DEFAULT 5.0 -- 1.0 to 5.0 scale
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            Bananas.report_collision(e, "CRM_SCHEMA_CRASH")

    @staticmethod
    def log_client(name, c_type, contact, email, terms=30):
        """
        OXIDE: Onboards a new entity into the CRM burrow.
        """
        client_id = f"CL-{name[:3].upper()}-{datetime.now().strftime('%f')[:4]}"
        try:
            cmd = """
                INSERT INTO client_directory (client_id, company_name, client_type, primary_contact, email, payment_terms)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            MonkeyBrain.execute_oxide(cmd, (client_id, name, c_type, contact, email, terms))
            return client_id
        except Exception as e:
            Bananas.report_collision(e, "CLIENT_LOG_FAILURE")
            return None

    @staticmethod
    def get_client_profitability(client_id):
        """
        OXIDE: Cross-references the 'Belly' and 'Billing' to see if this client
        is actually making the company money.
        Target: Executive 'Buy-In' for bid/no-bid decisions.
        """
        query = """
            SELECT 
                c.company_name,
                SUM(p.gross_margin_target) / COUNT(p.project_id) as avg_planned_margin,
                (SELECT COUNT(*) FROM core_projects WHERE client_id = ?) as project_count
            FROM client_directory c
            LEFT JOIN core_projects p ON c.client_id = p.client_id
            WHERE c.client_id = ?
        """
        # Note: This assumes a 'client_id' column was added to core_projects in the Belly.
        return MonkeyBrain.query_oxide(query, (client_id, client_id))

    @staticmethod
    def update_reliability(client_id, rating):
        """
        Allows the PM to 'grade' a GC after a project ends.
        """
        cmd = "UPDATE client_directory SET reliability_rating = ? WHERE client_id = ?"
        MonkeyBrain.execute_oxide(cmd, (rating, client_id))