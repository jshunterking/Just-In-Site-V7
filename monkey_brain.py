"""
MONKEY BRAIN V9.0 | THE UNIVERSAL CHASSIS
The persistent memory for all 44+ Operational Modules.
"""
import sqlite3
import os
import json

DB_FILE = os.path.join("/data" if os.path.exists("/data") else ".", "monkey_core.db")


class MonkeyBrain:
    def __init__(self):
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # 1. THE HAT REGISTRY (Roles & Permissions)
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, hats TEXT, level INTEGER, last_active TEXT
        )''')

        # 2. GRANULAR INVENTORY (Points 1, 3, 5, 8, 9)
        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, job_id TEXT, 
            quantity REAL, uom TEXT, min_threshold REAL, bin_location TEXT, 
            is_scrap INTEGER DEFAULT 0
        )''')

        # 3. TEACHING TIME-CLOCK (Points 12, 13, 15, 17, 18, 19)
        cursor.execute('''CREATE TABLE IF NOT EXISTS time_slips (
            id INTEGER PRIMARY KEY AUTOINCREMENT, worker_id TEXT, job_id TEXT, 
            phase_code TEXT, hours REAL, status TEXT DEFAULT 'PENDING', 
            rejection_note TEXT, is_overtime INTEGER DEFAULT 0, timestamp TEXT
        )''')

        # 4. THE VAULT (Points 22, 35, 36, 39)
        cursor.execute('''CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, job_id TEXT, 
            version INTEGER DEFAULT 1, submittal_deadline TEXT, markups TEXT
        )''')

        # 5. PREFAB ASSEMBLIES (Points 22, 23, 24, 25, 26, 30)
        cursor.execute('''CREATE TABLE IF NOT EXISTS assemblies (
            qr_id TEXT PRIMARY KEY, job_id TEXT, bom_list TEXT, 
            stage TEXT DEFAULT 'STAGED', history TEXT
        )''')

        conn.commit()
        conn.close()

    def execute_write(self, q, p=()):
        conn = self._get_connection()
        try:
            c = conn.cursor();
            c.execute(q, p);
            conn.commit()
        finally:
            conn.close()

    def execute_read(self, q, p=()):
        conn = self._get_connection()
        try:
            c = conn.cursor();
            c.execute(q, p)
            return [dict(row) for row in c.fetchall()]
        finally:
            conn.close()