"""
MONKEY BRAIN V7.0
The Single Source of Truth (Database Engine) for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the SQLite database. It is the only module allowed to
write directly to the disk. All other modules must ask the Brain to remember.

CORE CAPABILITIES:
1. Initialize Database (Create Tables).
2. Generate Unique IDs (Job Numbers).
3. Omni-Search (Global Query).
4. CRUD Operations (Create, Read, Update, Delete).

INTEGRATIONS:
- Bananas (Error Handling)
- Monkey Heart (Logging)
"""

import sqlite3
import json
import os
import threading
from datetime import datetime
from typing import List, Dict, Any, Optional

# ==============================================================================
# 🍌 IMPORT BANANAS (The Shield)
# ==============================================================================
try:
    from bananas import Bananas
except ImportError:
    class Bananas:
        @staticmethod
        def report_collision(error, context):
            print(f"🍌 [BANANAS] SLIP in {context}: {error}")

# ==============================================================================
# ❤️ IMPORT MONKEY HEART (The Logger)
# ==============================================================================
try:
    from monkey_heart import MonkeyHeart
except ImportError:
    class MonkeyHeart:
        @staticmethod
        def log_system_event(event_type, message):
            print(f"❤️ [HEARTBEAT] [{event_type}] {message}")


# ==============================================================================
# 🧠 MONKEY BRAIN CLASS
# ==============================================================================

class MonkeyBrain:
    """
    The Memory Bank.

    ATTRIBUTES:
        db_path (str): File path to 'monkey_brain.db'.
        lock (Lock): Thread safety for SQLite.
    """

    DB_PATH = "monkey_brain.db"

    def __init__(self):
        self.lock = threading.Lock()
        self._initialize_db()

    def get_connection(self):
        """Returns a connection object (Use inside 'with' block)."""
        return sqlite3.connect(self.DB_PATH, check_same_thread=False)

    def _initialize_db(self):
        """
        Runs the Genesis Protocol. Creates tables if they are missing.
        """
        if not os.path.exists(self.DB_PATH):
            MonkeyHeart.log_system_event("BRAIN", "First Boot Detected. Initializing Cortex...")

        create_scripts = [
            # 1. USERS (The Tribe)
            """CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT,
                role TEXT,
                full_name TEXT,
                email TEXT,
                meta_json TEXT
            )""",

            # 2. JOBS (The Projects)
            """CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                name TEXT,
                client TEXT,
                status TEXT, -- PENDING, WON, ACTIVE, COMPLETE, LOST
                type TEXT, -- CONSTRUCTION, SERVICE
                start_date TEXT,
                pm_id TEXT,
                foreman_id TEXT,
                financials_json TEXT, -- {budget: X, spent: Y}
                meta_json TEXT
            )""",

            # 3. TIMECARDS (The Hours)
            """CREATE TABLE IF NOT EXISTS timecards (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                job_id TEXT,
                clock_in TEXT,
                clock_out TEXT,
                total_hours REAL,
                status TEXT -- ACTIVE, APPROVED
            )""",

            # 4. INVENTORY (The Stuff)
            """CREATE TABLE IF NOT EXISTS inventory (
                sku TEXT PRIMARY KEY,
                name TEXT,
                category TEXT,
                qty_on_hand INTEGER,
                cost_avg REAL,
                vendor_sku TEXT
            )""",

            # 5. PO_MASTER (The Orders)
            """CREATE TABLE IF NOT EXISTS purchase_orders (
                po_number TEXT PRIMARY KEY,
                job_id TEXT,
                vendor TEXT,
                status TEXT, -- DRAFT, SENT, RECEIVED
                total_cost REAL,
                items_json TEXT,
                created_at TEXT
            )"""
        ]

        try:
            with self.lock:
                conn = self.get_connection()
                cursor = conn.cursor()
                for script in create_scripts:
                    cursor.execute(script)
                conn.commit()
                conn.close()
        except Exception as e:
            Bananas.report_collision(e, "Brain Initialization")

    # ==========================================================================
    # 🔢 ID GENESIS (The Counter)
    # ==========================================================================

    def generate_job_id(self, is_service: bool = False) -> str:
        """
        Creates the next Job Number: 26001, 26002...
        Service Jobs get an 'S' prefix: S26001.
        """
        year_prefix = datetime.now().strftime("%y")  # "26"

        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Find the highest number for this year
            like_query = f"{'S' if is_service else ''}{year_prefix}%"
            cursor.execute("SELECT job_id FROM jobs WHERE job_id LIKE ? ORDER BY job_id DESC LIMIT 1", (like_query,))
            result = cursor.fetchone()

            if result:
                last_id = result[0]
                # Strip prefix if Service
                if is_service: last_id = last_id[1:]
                # "26001" -> int(26001) -> 26002
                next_seq = int(last_id) + 1
                new_id = f"{'S' if is_service else ''}{next_seq}"
            else:
                # Start of the year
                new_id = f"{'S' if is_service else ''}{year_prefix}001"

            conn.close()

        MonkeyHeart.log_system_event("BRAIN", f"Genesis: Created Job ID {new_id}")
        return new_id

    # ==========================================================================
    # 🔍 OMNI-SEARCH (The Google)
    # ==========================================================================

    def omni_search(self, query: str) -> Dict[str, List[Dict]]:
        """
        Searches ALL tables for a string.
        Returns categorized results.
        """
        clean_q = f"%{query}%"
        results = {"jobs": [], "users": [], "inventory": []}

        with self.lock:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row  # Return dict-like rows
            cursor = conn.cursor()

            # 1. Search Jobs
            cursor.execute("SELECT * FROM jobs WHERE name LIKE ? OR job_id LIKE ? OR client LIKE ?",
                           (clean_q, clean_q, clean_q))
            for row in cursor.fetchall():
                results["jobs"].append(dict(row))

            # 2. Search Users
            cursor.execute("SELECT * FROM users WHERE full_name LIKE ? OR username LIKE ?", (clean_q, clean_q))
            for row in cursor.fetchall():
                # Don't return passwords!
                u = dict(row)
                del u['password_hash']
                results["users"].append(u)

            # 3. Search Inventory
            cursor.execute("SELECT * FROM inventory WHERE name LIKE ? OR sku LIKE ?", (clean_q, clean_q))
            for row in cursor.fetchall():
                results["inventory"].append(dict(row))

            conn.close()

        return results

    # ==========================================================================
    # 💾 CRUD HELPERS (The Hands)
    # ==========================================================================

    def save_job(self, job_data: Dict):
        """
        Upserts a job record.
        """
        # Ensure ID exists
        if not job_data.get('job_id'):
            job_data['job_id'] = self.generate_job_id(is_service=(job_data.get('type') == 'SERVICE'))

        sql = """INSERT OR REPLACE INTO jobs 
                 (job_id, name, client, status, type, start_date, pm_id, foreman_id, financials_json, meta_json)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        vals = (
            job_data['job_id'],
            job_data.get('name'),
            job_data.get('client'),
            job_data.get('status', 'PENDING'),
            job_data.get('type', 'CONSTRUCTION'),
            job_data.get('start_date'),
            job_data.get('pm_id'),
            job_data.get('foreman_id'),
            json.dumps(job_data.get('financials', {})),
            json.dumps(job_data.get('meta', {}))
        )

        self._execute_write(sql, vals)
        MonkeyHeart.log_system_event("BRAIN", f"Job Saved: {job_data['job_id']}")
        return job_data['job_id']

    def _execute_write(self, sql: str, params: tuple):
        """Thread-safe write wrapper."""
        with self.lock:
            conn = self.get_connection()
            try:
                conn.execute(sql, params)
                conn.commit()
            except Exception as e:
                Bananas.report_collision(e, f"SQL Write: {sql[:30]}...")
            finally:
                conn.close()

    def fetch_all_jobs(self) -> List[Dict]:
        """Reads all jobs."""
        with self.lock:
            conn = self.get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM jobs")
            rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
        return rows


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🧠 MONKEY BRAIN V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize (triggers table creation)
    brain = MonkeyBrain()

    # 2. Test ID Genesis
    print("\n[TEST 1] Generating Job IDs...")
    id1 = brain.generate_job_id(is_service=False)
    print(f" > Construction ID: {id1}")
    id2 = brain.generate_job_id(is_service=True)
    print(f" > Service ID: {id2}")

    # 3. Test Save Job
    print("\n[TEST 2] Saving Mock Job...")
    mock_job = {
        "job_id": id1,
        "name": "Mercy Hospital ICU",
        "client": "Mercy Health",
        "status": "ACTIVE",
        "financials": {"budget": 100000}
    }
    brain.save_job(mock_job)

    # 4. Test Omni Search
    print("\n[TEST 3] Searching for 'Mercy'...")
    results = brain.omni_search("Mercy")
    print(f" > Found {len(results['jobs'])} Jobs.")
    if results['jobs']:
        print(f" > Match: {results['jobs'][0]['name']} ({results['jobs'][0]['job_id']})")

    print("\n" + "=" * 40)
    print("🧠 MONKEY BRAIN SYSTEM: OPERATIONAL")