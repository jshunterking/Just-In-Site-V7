import hashlib
import sqlite3
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart


class GenesisProtocol:
    """
    GENESIS: THE BIG BANG.
    Run this ONCE to seed the Single Source of Truth with real operational data.
    """

    @staticmethod
    def ignite():
        print("--- INITIATING GENESIS PROTOCOL ---")

        # 1. WIPE THE SLATE (Optional - keeps the DB clean for the fresh start)
        # We drop the tables so we can rebuild them with perfect schemas
        conn = MonkeyBrain.get_connection()
        cursor = conn.cursor()

        tables = ["user_auth", "core_projects", "universal_inventory", "daily_reports"]
        for t in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {t}")
            print(f"GENESIS: Wiped Table [{t}]")

        conn.commit()
        conn.close()

        # 2. REBUILD THE STRUCTURES (The Bones)
        print("GENESIS: Re-initializing Neural Pathways...")
        MonkeyBrain.initialize_database()  # Rebuilds Projects/Inventory

        # We need to import these to trigger their specific table builds
        from oxide_roles import OxideRoles
        OxideRoles.initialize_auth_table()

        from rabbit_daily_reports import RabbitDailyReports
        RabbitDailyReports.initialize_daily_tables()

        # 3. SEED THE HUMANS (The Crew)
        print("GENESIS: Awakening the Crew...")

        # Helper to hash passwords
        def get_hash(pw):
            return hashlib.sha256(pw.encode()).hexdigest()

        # THE ROSTER
        users = [
            # (Username, Password, Role, Full Name, Email)
            ("Justin", "admin123", "OVERLORD", "Justin (Owner)", "justin@enertech.com"),
            ("ForemanMike", "site2026", "FIELD_CMDR", "Mike The Foreman", "mike@enertech.com"),
            ("EstimatorSarah", "bidwin", "SEER", "Sarah Pre-Con", "sarah@enertech.com"),
            ("ApprenticeJoe", "learn", "INFANTRY", "Joe Apprentice", "joe@enertech.com")
        ]

        conn = MonkeyBrain.get_connection()
        cursor = conn.cursor()

        for u, p, r, n, e in users:
            cursor.execute("""
                INSERT INTO user_auth (username, password_hash, role_code, full_name, email)
                VALUES (?, ?, ?, ?, ?)
            """, (u, get_hash(p), r, n, e))

        # 4. SEED THE PROJECTS (The Active Jobs)
        print("GENESIS: Loading Active Projects...")
        projects = [
            # (ID, Name, Status, Client, Margin Target)
            ("PROJ-2026-01", "Mercy Health Generator Upgrade", "ACTIVE", "Mercy Health", 0.28),
            ("PROJ-2026-02", "Liberty School LED Retrofit", "ACTIVE", "Liberty Local Schools", 0.35),
            ("PROJ-2026-03", "Downtown Lofts (Phase 2)", "BIDDING", "Simco Management", 0.22)
        ]

        for pid, name, status, client, margin in projects:
            cursor.execute("""
                INSERT INTO core_projects (project_id, project_name, status, client_id, gross_margin_target)
                VALUES (?, ?, ?, ?, ?)
            """, (pid, name, status, client, margin))

        # 5. SEED THE INVENTORY (The Arms)
        print("GENESIS: Stocking the Warehouse...")
        inventory = [
            ("MAT-001", "3/4 EMT Conduit (10ft)", 500, 4.50, "WAREHOUSE"),
            ("MAT-002", "4SQ Box (Deep)", 200, 1.25, "WAREHOUSE"),
            ("MAT-003", "THHN #12 Solid (Black)", 15, 65.00, "TRUCK-1"),  # Spools
            ("MAT-004", "Wire Nut (Red/Yellow)", 5000, 0.08, "SITE-A")
        ]

        for item, desc, qty, cost, loc in inventory:
            cursor.execute("""
                INSERT INTO universal_inventory (item_id, description, quantity, unit_cost, location)
                VALUES (?, ?, ?, ?, ?)
            """, (item, desc, qty, cost, loc))

        conn.commit()
        conn.close()
        print("--- GENESIS COMPLETE. WELCOME TO THE NEW REALITY. ---")


if __name__ == "__main__":
    GenesisProtocol.ignite()