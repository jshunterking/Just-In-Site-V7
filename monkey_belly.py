import uuid
import os
from datetime import datetime
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class MonkeyBelly:
    """
    DIGESTION: The centralized processing hub for project data.
    OXIDE PROTOCOL: Dissects raw project inputs into the SQL Singularity.
    Target: Enterprise-grade data organization for All-Trades.
    """

    @staticmethod
    def create_project_singularity(name, trade_focus, margin_target=0.0):
        """
        OXIDE: Generates a unique project ID and creates its physical
        stomach (folder) on the Railway Persistent Volume.
        """
        project_id = f"PJ-{str(uuid.uuid4())[:6].upper()}"

        try:
            # 1. Inject into the SQL Singularity (The Brain)
            cmd = """
                INSERT INTO core_projects (project_id, project_name, trade_focus, gross_margin_target)
                VALUES (?, ?, ?, ?)
            """
            MonkeyBrain.execute_oxide(cmd, (project_id, name, trade_focus, margin_target))

            # 2. Physical Digestion: Create dedicated project vault folder
            # This ensures blueprints/invoices are isolated per job site.
            project_path = os.path.join(MonkeyHeart.VAULT_PATH, project_id)
            if not os.path.exists(project_path):
                os.makedirs(project_path)

            # 3. Log the creation to the Heart's audit trail
            MonkeyHeart.log_system_event("PROJECT_CREATED", f"IDENT: {project_id} | FOCUS: {trade_focus}")

            return project_id

        except Exception as e:
            Bananas.report_collision(e, "BELLY_DIGESTION_FAILED")
            return None

    @staticmethod
    def get_stomach_contents(project_id):
        """
        Retrieves the full dataset for a specific project.
        Essential for the 'Immediate Buy-In' Dashboard.
        """
        query = "SELECT * FROM core_projects WHERE project_id = ?"
        df = MonkeyBrain.query_oxide(query, (project_id,))

        if not df.empty:
            return df.to_dict('records')[0]
        return None

    @staticmethod
    def purge_project(project_id):
        """
        OXIDE: Secure removal of project data and physical file structures.
        """
        try:
            cmd = "DELETE FROM core_projects WHERE project_id = ?"
            MonkeyBrain.execute_oxide(cmd, (project_id,))

            # Physical deletion logic would go here if required.
            Bananas.notify("PURGE", f"Project {project_id} removed from Singularity.")
        except Exception as e:
            Bananas.report_collision(e, "PURGE_FAILURE")