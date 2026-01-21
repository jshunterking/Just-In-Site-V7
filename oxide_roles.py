import hashlib
import sqlite3
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class OxideRoles:
    """
    OXIDE HIERARCHY: The Grand Construction Matrix.
    Manages the 7 Tiers of Access Control and Theater Permissions.
    """

    # --- THE GRAND HIERARCHY ---
    ROLES = {
        "OVERLORD": {"rank": 100, "theaters": ["ALL"]},
        "EXECUTIVE": {"rank": 90, "theaters": ["ORACLE", "VAULT", "FIELD", "RADAR"]},
        "COMMAND": {"rank": 80, "theaters": ["FIELD", "VAULT", "RADAR"]},
        "SEER": {"rank": 70, "theaters": ["RADAR", "VAULT"]},
        "FIELD_CMDR": {"rank": 60, "theaters": ["FIELD"]},
        "LOGISTICS": {"rank": 50, "theaters": ["VAULT", "FIELD"]},  # Needs Field for delivery locations
        "INFANTRY": {"rank": 20, "theaters": ["FIELD_LITE"]}  # Restricted View
    }

    @staticmethod
    def initialize_auth_table():
        """
        Builds the secure user directory with the new 7-Tier Schema.
        """
        conn = MonkeyBrain.get_connection()
        if not conn: return

        try:
            cursor = conn.cursor()
            # We add 'email' and 'phone' for Raptor Automation alerts
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_auth (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password_hash TEXT,
                    role_code TEXT,
                    full_name TEXT,
                    email TEXT,
                    phone TEXT,
                    active INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # --- SEED THE OWNER (YOU) ---
            # Default: admin123
            default_pass = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute("""
                INSERT OR IGNORE INTO user_auth (username, password_hash, role_code, full_name, email)
                VALUES ('Justin', ?, 'OVERLORD', 'Justin Owner', 'justin@enertechelectric.com')
            """, (default_pass,))

            # --- SEED A DUMMY FOREMAN (TESTING) ---
            cursor.execute("""
                INSERT OR IGNORE INTO user_auth (username, password_hash, role_code, full_name)
                VALUES ('Foreman1', ?, 'FIELD_CMDR', 'Mike Field')
            """, (default_pass,))

            conn.commit()
            print("OXIDE ROLES: Hierarchy Established.")
            conn.close()
        except Exception as e:
            Bananas.report_collision(e, "AUTH_TABLE_INIT_FAILURE")

    @staticmethod
    def login(username, password):
        """
        Verifies credentials and returns the User's Role & Rank.
        """
        try:
            hashed_input = hashlib.sha256(password.encode()).hexdigest()
            query = "SELECT role_code, full_name, user_id FROM user_auth WHERE username = ? AND password_hash = ?"
            user = MonkeyBrain.query_oxide(query, (username, hashed_input))

            if not user.empty:
                role_code = user['role_code'].iloc[0]
                rank = OxideRoles.ROLES.get(role_code, {}).get("rank", 0)

                MonkeyHeart.log_system_event("LOGIN_SUCCESS", f"User: {username} | Role: {role_code}")

                return {
                    "authenticated": True,
                    "role_code": role_code,
                    "rank": rank,
                    "name": user['full_name'].iloc[0],
                    "user_id": user['user_id'].iloc[0]
                }

            return {"authenticated": False}
        except Exception as e:
            Bananas.report_collision(e, "LOGIN_FAILURE")
            return {"authenticated": False}

    @staticmethod
    def get_accessible_theaters(role_code):
        """
        Returns the list of dashboards (Theaters) this user is allowed to see.
        """
        if role_code == "OVERLORD":
            return ["Oracle (Executive)", "Vault (Financial)", "Field (Production)", "Radar (Scouting)",
                    "Settings (System)"]

        perms = OxideRoles.ROLES.get(role_code, {}).get("theaters", [])

        # Translate internal codes to UI names
        ui_map = {
            "ORACLE": "Oracle (Executive)",
            "VAULT": "Vault (Financial)",
            "FIELD": "Field (Production)",
            "RADAR": "Radar (Scouting)",
            "FIELD_LITE": "My Schedule"
        }

        return [ui_map[p] for p in perms if p in ui_map]

    @staticmethod
    def can_view_money(role_code):
        """
        The Financial Firewall.
        Returns True ONLY if the role is allowed to see dollar signs.
        """
        return role_code in ["OVERLORD", "EXECUTIVE", "COMMAND", "SEER", "LOGISTICS"]