from datetime import datetime
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class RabbitSubcontractor:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for Sub-Tier Management.
    OXIDE DISSECTION: Tracking Subcontractor agreements, COIs, and Billing.
    Target: Eliminating risk from 3rd-party labor and specialized vendors.
    """

    @staticmethod
    def initialize_subcontractor_tables():
        """
        OXIDE: Dissects the database to support external contract tracking.
        """
        conn = MonkeyBrain.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # SUBCONTRACTOR_DIRECTORY: Master list of external firms
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subcontractor_directory (
                    sub_id TEXT PRIMARY KEY,
                    company_name TEXT,
                    contact_person TEXT,
                    trade_specialty TEXT,
                    coi_expiry DATE,
                    status TEXT DEFAULT 'QUALIFIED' -- QUALIFIED, PENDING_COI, BLACKLISTED
                )
            """)

            # SUB_CONTRACTS: Specific agreements tied to projects
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sub_contracts (
                    contract_id TEXT PRIMARY KEY,
                    project_id TEXT,
                    sub_id TEXT,
                    contract_amount REAL,
                    billed_to_date REAL DEFAULT 0.0,
                    FOREIGN KEY(project_id) REFERENCES core_projects(project_id),
                    FOREIGN KEY(sub_id) REFERENCES subcontractor_directory(sub_id)
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            Bananas.report_collision(e, "SUBCONTRACTOR_SCHEMA_CRASH")

    @staticmethod
    def register_sub(name, specialty, coi_date):
        """
        OXIDE: Onboards a new sub-tier partner.
        """
        sub_id = f"SUB-{name[:3].upper()}-{datetime.now().strftime('%y%m%d')}"
        try:
            cmd = """
                INSERT INTO subcontractor_directory (sub_id, company_name, trade_specialty, coi_expiry)
                VALUES (?, ?, ?, ?)
            """
            MonkeyBrain.execute_oxide(cmd, (sub_id, name, specialty, coi_date))
            return sub_id
        except Exception as e:
            Bananas.report_collision(e, "SUB_REGISTRATION_FAILURE")
            return None

    @staticmethod
    def check_sub_compliance(sub_id):
        """
        OXIDE: Reaches into the directory to verify insurance status.
        Triggers the 'Ears' (Block 09) if the sub is working without a COI.
        """
        query = "SELECT company_name, coi_expiry FROM subcontractor_directory WHERE sub_id = ?"
        df = MonkeyBrain.query_oxide(query, (sub_id,))

        if not df.empty:
            expiry = datetime.strptime(df['coi_expiry'].iloc[0], '%Y-%m-%d').date()
            if expiry < datetime.now().date():
                Bananas.notify("COMPLIANCE_ALARM", f"Subcontractor {df['company_name'].iloc[0]} has EXPIRED COI.")
                return False
        return True

    @staticmethod
    def get_sub_financial_summary(project_id):
        """
        Retrieves total sub-tier exposure for the 'Belly' metrics.
        """
        query = """
            SELECT s.company_name, c.contract_amount, c.billed_to_date
            FROM sub_contracts c
            JOIN subcontractor_directory s ON c.sub_id = s.sub_id
            WHERE c.project_id = ?
        """
        return MonkeyBrain.query_oxide(query, (project_id,))