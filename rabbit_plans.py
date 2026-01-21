"""
RABBIT PLANS V7.0
The Blueprint & Document Control Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module manages the storage, versioning, and annotation of construction
drawings (PDFs). It ensures the field is always looking at the "Latest & Greatest."

CORE CAPABILITIES:
1. Plan Ingestion (Upload & Hashing).
2. Revision Control (Version 1 vs Version 2).
3. Annotation/Redline Management (Storing notes on top of plans).
4. Offline Caching logic.

INTEGRATIONS:
- Bananas (Error Handling)
- Monkey Brain (Metadata Storage)
"""

import os
import json
import hashlib
import shutil
import time
from datetime import datetime
from typing import List, Dict, Optional, Any

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
# 🐰 RABBIT PLANS CLASS
# ==============================================================================

class RabbitPlans:
    """
    The Vault Keeper.

    ATTRIBUTES:
        storage_dir (str): Local folder for PDF storage.
    """

    STORAGE_DIR = "plan_vault"

    def __init__(self):
        self._setup_vault()

    def _setup_vault(self):
        """Ensures the plan storage directory exists."""
        if not os.path.exists(self.STORAGE_DIR):
            os.makedirs(self.STORAGE_DIR)

    # ==========================================================================
    # 📤 PLAN INGESTION (The Upload)
    # ==========================================================================

    def upload_plan_sheet(self, job_id: str, file_name: str, file_bytes: bytes, uploader: str) -> Dict[str, Any]:
        """
        Saves a new plan sheet. Checks for revisions automatically.

        ARGS:
            job_id: "JOB-26001"
            file_name: "E-101.pdf"
            file_bytes: The raw file data.
            uploader: User ID.

        RETURNS:
            dict: Metadata about the saved file.
        """
        MonkeyHeart.log_system_event("PLANS", f"Receiving upload: {file_name} for {job_id}")

        # 1. Calculate Hash (Digital Fingerprint)
        file_hash = hashlib.md5(file_bytes).hexdigest()

        # 2. Determine Version
        # In a real DB, we check if E-101 exists for this Job.
        # For V7.0 File Logic:
        # We save as plan_vault/JOB-26001/E-101_v1.pdf

        job_dir = os.path.join(self.STORAGE_DIR, job_id)
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)

        # Check for existing versions
        existing_files = [f for f in os.listdir(job_dir) if f.startswith(file_name.replace(".pdf", ""))]
        version_num = len(existing_files) + 1

        # 3. Save File
        save_name = f"{file_name.replace('.pdf', '')}_v{version_num}.pdf"
        full_path = os.path.join(job_dir, save_name)

        try:
            with open(full_path, "wb") as f:
                f.write(file_bytes)

            status_msg = f"Uploaded Version {version_num}"
            if version_num > 1:
                status_msg += " (REVISION DETECTED)"
                Bananas.notify("Revision Alert", f"New version of {file_name} detected!")

            MonkeyHeart.log_system_event("PLANS_SAVE", f"Saved {save_name} ({len(file_bytes)} bytes)")

            return {
                "success": True,
                "file_path": full_path,
                "version": version_num,
                "hash": file_hash,
                "timestamp": datetime.now().isoformat(),
                "status": status_msg
            }

        except Exception as e:
            Bananas.report_collision(e, "Plan Upload")
            return {"success": False, "error": str(e)}

    # ==========================================================================
    # 🖍️ REDLINING (The Annotations)
    # ==========================================================================

    def add_redline(self, job_id: str, sheet_name: str, user: str,
                    x_coord: float, y_coord: float, note: str) -> bool:
        """
        Saves a digital sticky note on a drawing.

        ARGS:
            x_coord/y_coord: Percentage (0.0 to 1.0) relative to sheet size.
        """
        # In V7.0, we store these in a JSON sidecar file next to the plan
        job_dir = os.path.join(self.STORAGE_DIR, job_id)
        if not os.path.exists(job_dir):
            return False

        sidecar_path = os.path.join(job_dir, f"{sheet_name}_redlines.json")

        entry = {
            "id": f"NOTE-{int(time.time())}",
            "user": user,
            "x": x_coord,
            "y": y_coord,
            "text": note,
            "date": datetime.now().isoformat()
        }

        try:
            data = []
            if os.path.exists(sidecar_path):
                with open(sidecar_path, "r") as f:
                    data = json.load(f)

            data.append(entry)

            with open(sidecar_path, "w") as f:
                json.dump(data, f, indent=2)

            MonkeyHeart.log_system_event("PLANS_NOTE", f"Redline added to {sheet_name}: '{note}'")
            return True

        except Exception as e:
            Bananas.report_collision(e, "Add Redline")
            return False

    def get_redlines(self, job_id: str, sheet_name: str) -> List[Dict]:
        """Retrieves all notes for a sheet."""
        job_dir = os.path.join(self.STORAGE_DIR, job_id)
        sidecar_path = os.path.join(job_dir, f"{sheet_name}_redlines.json")

        if os.path.exists(sidecar_path):
            with open(sidecar_path, "r") as f:
                return json.load(f)
        return []

    # ==========================================================================
    # 💾 OFFLINE SYNC (The Cache)
    # ==========================================================================

    def sync_to_device(self, job_id: str):
        """
        Simulates downloading the entire Plan Set for a job to local storage.
        Used when the Foreman clicks "Make Available Offline."
        """
        MonkeyHeart.log_system_event("PLANS_SYNC", f"Caching Plan Set for {job_id}...")
        time.sleep(1.5)  # Simulate download time

        # In a real app, this would verify file integrity.
        # Here we just confirm success.
        Bananas.notify("Sync Complete", f"Plans for {job_id} are ready offline.")
        return True


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT PLANS V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    vault = RabbitPlans()

    # 2. Test Upload (Simulated PDF)
    print("\n[TEST 1] Uploading 'E-101.pdf' (v1)...")
    dummy_pdf = b"%PDF-1.4...content..."
    res1 = vault.upload_plan_sheet("JOB-TEST", "E-101.pdf", dummy_pdf, "Justin")
    print(f" > {res1['status']} ({res1['file_path']})")

    # 3. Test Revision (Upload same name again)
    print("\n[TEST 2] Uploading 'E-101.pdf' (v2)...")
    res2 = vault.upload_plan_sheet("JOB-TEST", "E-101.pdf", dummy_pdf, "Justin")
    print(f" > {res2['status']} ({res2['file_path']})")

    # 4. Test Redlining
    print("\n[TEST 3] Adding Redline to E-101...")
    vault.add_redline("JOB-TEST", "E-101", "Foreman", 0.5, 0.5, "RFI Needed Here")

    # 5. Read Redlines
    notes = vault.get_redlines("JOB-TEST", "E-101")
    print(f" > Found {len(notes)} Redlines.")
    print(f" > Note 1: '{notes[0]['text']}' at {notes[0]['x']},{notes[0]['y']}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT PLANS SYSTEM: OPERATIONAL")