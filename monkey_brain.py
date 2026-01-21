"""
MONKEY BRAIN V9.01.2 | THE RE-WELDED CHASSIS
Single Source of Truth for Roles, Inventory, and Assemblies.
Optimized for PyCharm Structural Integrity.
"""
import sqlite3
import os

# Use a local path for the database to ensure write permissions in PyCharm
DB_FILE = "monkey_core.db"


class MonkeyBrain:
    """The central data-limb for the Monkey OS."""

    def __init__(self):
        """Initialize the brain and ensure all neural pathways exist."""
        self._init_db()

    def _get_connection(self):
        """Establish a secure link to the SQLite ledger."""
        conn = sqlite3.connect(DB_FILE, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Build the foundational tables for the Singularity."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 1. THE HAT REGISTRY (Roles & Permissions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY, 
                hats TEXT, 
                level INTEGER, 
                last_active TEXT
            )
        ''')

        # 2. GRANULAR INVENTORY (The Paws Module)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                item_name TEXT, 
                job_id TEXT, 
                quantity REAL, 
                uom TEXT, 
                min_threshold REAL, 
                bin_location TEXT, 
                is_scrap INTEGER DEFAULT 0
            )
        ''')

        # 3. TEACHING TIME-CLOCK (The Rabbit Module)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_slips (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                worker_id TEXT, 
                job_id TEXT, 
                phase_code TEXT, 
                hours REAL, 
                status TEXT DEFAULT 'PENDING', 
                rejection_note TEXT, 
                is_overtime INTEGER DEFAULT 0, 
                timestamp TEXT
            )
        ''')

        # 4. THE VAULT (The Panther Module)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                file_name TEXT, 
                job_id TEXT, 
                version INTEGER DEFAULT 1, 
                submittal_deadline TEXT, 
                markups TEXT
            )
        ''')

        # 5. PREFAB ASSEMBLIES (The Neural Linker)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assemblies (
                qr_id TEXT PRIMARY KEY, 
                job_id TEXT, 
                bom_list TEXT, 
                stage TEXT DEFAULT 'STAGED', 
                history TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def execute_write(self, query: str, params: tuple = ()):
        """Write data to the ledger and commit the transaction."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
        finally:
            conn.close()

    def execute_read(self, query: str, params: tuple = ()):
        """Read data from the ledger and return as a list of dicts."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()