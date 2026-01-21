"""
RAPTOR PORTAL V7.0
The External Gateway for Clients and Subcontractors.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages "Guest Mode" access. It allows users outside the company
(Clients, GCs, Subcontractors) to interact with the system securely.

CORE CAPABILITIES:
1. Generate Secure View Tokens (Magic Links).
2. Render "Client Mode" Dashboard (Read-Only).
3. Handle Subcontractor Document Uploads.

INTEGRATIONS:
- Bananas (Error Handling)
- Monkey Brain (Data Retrieval)
"""

import time
import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# ==============================================================================
# 🍌 IMPORT BANANAS (The Shield)
# ==============================================================================
try:
    from bananas import Bananas
except ImportError:
    class Bananas:
        @staticmethod
        def notify(title, message):
            print(f"🍌 [BANANAS] TOAST: {title} - {message}")

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
# 🦖 RAPTOR PORTAL CLASS
# ==============================================================================

class RaptorPortal:
    """
    The Guest House.

    ATTRIBUTES:
        active_tokens (dict): In-memory store of valid guest tokens.
        token_lifetime_hours (int): How long a link works (default 48h).
    """

    def __init__(self, token_lifetime_hours: int = 48):
        self.token_lifetime_hours = token_lifetime_hours
        # In production, this would be in the Database (Monkey Brain).
        # For V7.0 Demo, we use a session dictionary.
        self.active_tokens = {}

    # ==========================================================================
    # 🎟️ TOKEN GENERATOR (The Ticket Booth)
    # ==========================================================================

    def generate_access_link(self, job_id: str, viewer_role: str, viewer_name: str) -> str:
        """
        Creates a magic link for a specific external user.

        ARGS:
            job_id: The Project they are allowed to see.
            viewer_role: 'CLIENT' (Read Only) or 'SUB' (Upload Only).
            viewer_name: "Mercy Admin" or "Joe Plumber".

        RETURNS:
            str: The full URL (Mocked).
        """
        token = f"tk_{uuid.uuid4().hex}"
        expiration = datetime.now() + timedelta(hours=self.token_lifetime_hours)

        self.active_tokens[token] = {
            "job_id": job_id,
            "role": viewer_role,
            "name": viewer_name,
            "expires_at": expiration,
            "created_at": datetime.now()
        }

        MonkeyHeart.log_system_event("PORTAL_ACCESS", f"Generated {viewer_role} token for {viewer_name} on {job_id}")

        # In real app: return f"https://app.justinsite.com/portal?token={token}"
        return f"http://localhost:8501/?portal_token={token}"

    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Checks if a guest is allowed in.
        """
        data = self.active_tokens.get(token)

        if not data:
            return {"valid": False, "error": "Invalid Token"}

        if datetime.now() > data['expires_at']:
            return {"valid": False, "error": "Token Expired"}

        return {
            "valid": True,
            "job_id": data['job_id'],
            "role": data['role'],
            "name": data['name']
        }

    # ==========================================================================
    # 👁️ CLIENT DASHBOARD (The Showroom)
    # ==========================================================================

    def render_client_view(self, job_data: Dict) -> Dict:
        """
        Sanitizes internal project data for external viewing.
        Removes profit margins, internal notes, and labor issues.

        ARGS:
            job_data: The full internal project dictionary.

        RETURNS:
            dict: The "Clean" version for the client.
        """
        MonkeyHeart.log_system_event("PORTAL_VIEW", f"Rendering Client View for {job_data.get('name')}")

        # 1. Calculate Public Progress
        # If we are 60% burned on budget, we might show 50% complete to client to be safe.
        percent_complete = job_data.get('percent_complete', 0)

        # 2. Filter Photos
        # Only show photos tagged "PUBLIC"
        public_photos = [p for p in job_data.get('photos', []) if p.get('tag') == 'PUBLIC']

        return {
            "project_name": job_data.get('name'),
            "status": "ON SCHEDULE" if not job_data.get('critical_flag') else "ATTENTION NEEDED",
            "percent_complete": percent_complete,
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "safety_days_without_incident": job_data.get('safety_days', 0),
            "approved_photos": public_photos,
            "message_from_pm": "Rough-in is 80% complete. Inspections scheduled for Tuesday."
        }

    # ==========================================================================
    # 📥 SUB DROP BOX (The Intake)
    # ==========================================================================

    def handle_sub_upload(self, token: str, file_name: str, file_type: str) -> bool:
        """
        Allows a Subcontractor to upload a file (Quote/Insurance).
        """
        access = self.validate_token(token)
        if not access['valid'] or access['role'] != 'SUB':
            Bananas.notify("Portal Security", "Unauthorized Upload Attempt")
            return False

        # Mock File Save Logic
        job_id = access['job_id']
        sub_name = access['name']

        MonkeyHeart.log_system_event("PORTAL_UPLOAD",
                                     f"Received {file_name} ({file_type}) from {sub_name} for {job_id}")

        # In V7.0 real implementation, this calls monkey_brain to save file
        return True


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦖 RAPTOR PORTAL V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    portal = RaptorPortal()

    # 2. Generate Client Link
    print("\n[TEST 1] Generating Link for Mercy Hospital Admin...")
    link = portal.generate_access_link("JOB-26001", "CLIENT", "Mercy Admin")
    print(f" > Link: {link}")

    # Extract token
    token = link.split("=")[1]

    # 3. Validate Token
    print("\n[TEST 2] Validating Token...")
    access = portal.validate_token(token)
    print(f" > Access Granted: {access['valid']}")
    print(f" > Viewer: {access['name']}")

    # 4. Render View
    print("\n[TEST 3] Rendering Client Dashboard...")
    mock_job = {
        "name": "Mercy Hospital ICU",
        "percent_complete": 45,
        "safety_days": 120,
        "internal_margin": 25,  # Should be hidden
        "photos": [{"id": 1, "tag": "PUBLIC"}, {"id": 2, "tag": "INTERNAL"}]
    }
    view = portal.render_client_view(mock_job)
    print(f" > Status Shown: {view['status']}")
    print(f" > Photos Shown: {len(view['approved_photos'])} (Should be 1)")
    if "internal_margin" not in view:
        print(" > SECURITY CHECK PASSED: Internal data hidden.")
    else:
        print(" > SECURITY FAILURE: Hidden data exposed!")

    print("\n" + "=" * 40)
    print("🦕 RAPTOR PORTAL SYSTEM: OPERATIONAL")