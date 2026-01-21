from datetime import datetime
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class RabbitManpower:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for Labor Management.
    OXIDE DISSECTION: Managing employee profiles, certifications, and crew assignments.
    Target: 100% Visibility into field labor utilization and compliance.
    """

    @staticmethod
    def initialize_manpower_tables():
        """
        OXIDE: Dissects the database to support employee records and daily labor logs.
        """
        conn = MonkeyBrain.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # EMPLOYEE_ROSTER: The master list of field and shop staff
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employee_roster (
                    emp_id TEXT PRIMARY KEY,
                    full_name TEXT,
                    trade_rank TEXT, -- Apprentice, Journeyman, Foreman
                    hourly_rate REAL,
                    certifications TEXT, -- JSON string of OSHA, Lift, etc.
                    status TEXT DEFAULT 'ACTIVE'
                )
            """)

            # LABOR_LOGS: Daily hour tracking per project
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS labor_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id TEXT,
                    emp_id TEXT,
                    hours_worked REAL,
                    work_date DATE,
                    description TEXT,
                    FOREIGN KEY(project_id) REFERENCES core_projects(project_id),
                    FOREIGN KEY(emp_id) REFERENCES employee_roster(emp_id)
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            Bananas.report_collision(e, "MANPOWER_SCHEMA_CRASH")

    @staticmethod
    def register_employee(name, rank, rate, certs="[]"):
        """
        OXIDE: Injects a new field operative into the roster.
        """
        emp_id = f"EMP-{name[:3].upper()}-{datetime.now().strftime('%S%f')[:4]}"
        try:
            cmd = """
                INSERT INTO employee_roster (emp_id, full_name, trade_rank, hourly_rate, certifications)
                VALUES (?, ?, ?, ?, ?)
            """
            MonkeyBrain.execute_oxide(cmd, (emp_id, name, rank, rate, certs))
            return emp_id
        except Exception as e:
            Bananas.report_collision(e, "EMPLOYEE_REGISTRATION_FAILURE")
            return None

    @staticmethod
    def log_daily_labor(project_id, emp_id, hours, desc=""):
        """
        OXIDE: Records field production hours.
        Feeds directly into the 'Belly' for real-time cost tracking.
        """
        try:
            cmd = """
                INSERT INTO labor_logs (project_id, emp_id, hours_worked, work_date, description)
                VALUES (?, ?, ?, ?, ?)
            """
            MonkeyBrain.execute_oxide(cmd, (project_id, emp_id, hours, datetime.now().date(), desc))

            Bananas.notify("LABOR_SYNC", f"Logged {hours} hrs for {emp_id} on {project_id}")
        except Exception as e:
            Bananas.report_collision(e, "LABOR_LOGGING_FAILURE")

    @staticmethod
    def get_project_manpower_pulse(project_id):
        """
        Retrieves total labor spend vs. estimates for the Executive Dashboard.
        """
        query = """
            SELECT SUM(l.hours_worked * e.hourly_rate) as total_labor_cost
            FROM labor_logs l
            JOIN employee_roster e ON l.emp_id = e.emp_id
            WHERE l.project_id = ?
        """
        return MonkeyBrain.query_oxide(query, (project_id,))