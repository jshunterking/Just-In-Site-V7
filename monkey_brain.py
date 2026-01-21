"""
MONKEY BRAIN V7.1 (GOLDEN MASTER)
The Database Connection Module.
"""
import sqlite3
import os

# Detect Railway Volume vs Local
if os.path.exists("/data"):
    print("🧠 [MONKEY BRAIN] Detected Railway Volume. Using /data/just_in_site.db")
    DB_FOLDER = "/data"
else:
    print("🧠 [MONKEY BRAIN] Local Environment. Using ./just_in_site.db")
    DB_FOLDER = "."

DB_FILE = os.path.join(DB_FOLDER, "just_in_site.db")


class MonkeyBrain:
    def __init__(self):
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(DB_FILE)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # TIME CLOCK
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_clock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                job_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                hours REAL,
                status TEXT DEFAULT 'ACTIVE'
            )
        ''')
        # PURCHASE ORDERS
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                po_number TEXT,
                job_id TEXT,
                amount REAL,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def execute_write(self, query, params=()):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def execute_read_one(self, query, params=()):
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None