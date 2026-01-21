"""
MONKEY BRAIN V8.1 | NEURAL SCHEMA
The Single Source of Truth for Roles, Inventory, and Assemblies.
"""
import sqlite3
import os

DB_FILE = os.path.join("/data" if os.path.exists("/data") else ".", "monkey_core.db")


class MonkeyBrain:
    def __init__(self):
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(DB_FILE)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # 1. USER REGISTRY (Multi-Hat Support)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                full_name TEXT,
                hats TEXT, -- Stored as JSON: ["ADMIN", "PURCHASING"]
                level INTEGER
            )
        ''')

        # 2. TIME SLIPS (Approval Workflow)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_slips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_id TEXT,
                job_id TEXT,
                hours REAL,
                status TEXT DEFAULT 'PENDING'
            )
        ''')

        # 3. INVENTORY LEDGER (Job-Tethered)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                job_id TEXT,
                quantity REAL
            )
        ''')

        # 4. ASSEMBLY VAULT (QR Digital Twins)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assemblies (
                qr_id TEXT PRIMARY KEY,
                assembly_name TEXT,
                doc_url TEXT,
                batch_target INTEGER
            )
        ''')

        conn.commit()
        conn.close()

    def execute_write(self, query, params=()):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def execute_read(self, query, params=()):
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]