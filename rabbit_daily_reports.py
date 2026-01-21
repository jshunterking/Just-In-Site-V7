import pandas as pd
from datetime import datetime
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class RabbitDailyReports:
    """
    RABBIT PROTOCOL: Speed in Field Documentation.
    OXIDE DISSECTION: Managing daily logs, weather, and crew counts.
    Target: The 'Single Source of Truth' for what happened on site.
    """

    @staticmethod
    def initialize_daily_tables():
        """
        OXIDE: Dissects the database to hold daily field logs.
        """
        conn = MonkeyBrain.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_reports (
                    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id TEXT,
                    report_date DATE,
                    weather_conditions TEXT,
                    crew_count INTEGER,
                    notes TEXT,
                    delay_minutes INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            Bananas.report_collision(e, "DAILY_SCHEMA_CRASH")

    @staticmethod
    def log_report(project_id, weather, notes, delay=0):
        """
        RABBIT: Rapidly inserts a daily log into the Belly.
        """
        try:
            cmd = """
                INSERT INTO daily_reports (project_id, report_date, weather_conditions, notes, delay_minutes)
                VALUES (?, ?, ?, ?, ?)
            """
            # Use today's date
            today = datetime.now().strftime('%Y-%m-%d')
            MonkeyBrain.execute_oxide(cmd, (project_id, today, weather, notes, delay))

            MonkeyHeart.log_system_event("DAILY_LOG_CREATED", f"Report filed for {project_id}")
            return True
        except Exception as e:
            Bananas.report_collision(e, "DAILY_LOG_FAILURE")
            return False

    @staticmethod
    def get_project_history(project_id):
        """
        RABBIT: Retrieves all past reports for a specific job.
        """
        query = "SELECT * FROM daily_reports WHERE project_id = ? ORDER BY report_date DESC"
        return MonkeyBrain.query_oxide(query, (project_id,))