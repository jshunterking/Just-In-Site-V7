"""
MONKEY BRAIN V7.0 (RAILWAY VOLUME EDITION)
The Database Connection Module.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
"""

import sqlite3
import os

# --- CRITICAL CHANGE FOR RAILWAY VOLUME ---
# On Railway, if you attach a volume to '/data', the OS creates that folder.
# If '/data' exists, we save the DB there (Persistent).
# If not (like on your laptop), we save it in the current folder (Local).

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
        """
        Creates the tables if they are missing.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # 1. TIME CLOCK TABLE
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

        # 2. PURCHASE ORDER TABLE
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

    # --- GENERIC SQL EXECUTORS ---

    def execute_write(self, query, params=()):
        """
        Run INSERT, UPDATE, DELETE.
        Returns the ID of the new row.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def execute_read_one(self, query, params=()):
        """
        Get a single row as a dictionary.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def execute_read_all(self, query, params=()):
        """
        Get a list of rows.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]