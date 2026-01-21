import pandas as pd
from datetime import datetime, timedelta
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class RabbitScheduling:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for Project Timelines.
    OXIDE DISSECTION: Critical Path Method (CPM) and Labor Leveling.
    Target: Eliminating job-site "Dead Time" through synchronized scheduling.
    """

    @staticmethod
    def initialize_schedule_tables():
        """
        OXIDE: Dissects the database to support task dependencies and milestones.
        """
        conn = MonkeyBrain.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # SCHEDULE_TASKS: The timeline nodes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schedule_tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id TEXT,
                    task_name TEXT,
                    start_date DATE,
                    end_date DATE,
                    assigned_crew TEXT,
                    dependency_id INTEGER, -- Link to a task that must finish first
                    FOREIGN KEY(project_id) REFERENCES core_projects(project_id)
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            Bananas.report_collision(e, "SCHEDULING_SCHEMA_CRASH")

    @staticmethod
    def add_milestone(project_id, name, start, duration_days, depends_on=None):
        """
        OXIDE: Injects a new node into the project timeline.
        """
        try:
            start_dt = datetime.strptime(start, '%Y-%m-%d')
            end_dt = start_dt + timedelta(days=duration_days)

            cmd = """
                INSERT INTO schedule_tasks (project_id, task_name, start_date, end_date, dependency_id)
                VALUES (?, ?, ?, ?, ?)
            """
            MonkeyBrain.execute_oxide(cmd, (project_id, name, start_dt.date(), end_dt.date(), depends_on))

            return True
        except Exception as e:
            Bananas.report_collision(e, "MILESTONE_INJECTION_FAILURE")
            return False

    @staticmethod
    def get_project_gantt_data(project_id):
        """
        Retrieves a formatted dataframe for timeline visualization.
        Essential for the 'Executive Buy-In' of project timelines.
        """
        query = "SELECT task_name as Task, start_date as Start, end_date as Finish, assigned_crew as Resource FROM schedule_tasks WHERE project_id = ? ORDER BY start_date"
        return MonkeyBrain.query_oxide(query, (project_id,))

    @staticmethod
    def calculate_labor_burn(project_id):
        """
        OXIDE: Analyzes the schedule to predict weekly manpower requirements.
        """
        # This will blow up into a 1,500 line algorithm in the 50k version.
        pass