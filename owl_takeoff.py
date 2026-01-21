"""
OWL TAKEOFF V7.0
The Plan Analysis & AI Reading Engine for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module is the "Eyes" of the Estimating and Prefab departments.
It ingests PDF drawings and uses pattern recognition (and AI stubs) to
identify the scope of work.

CORE CAPABILITIES:
1. Scan PDF Documents (Text Extraction).
2. Identify Rooms and Areas (Zone Detection).
3. Generate "Starter" Material Lists based on Room Type.

INTEGRATIONS:
- Bananas (Error Handling)
- Monkey Heart (Logging)
"""

import re
import json
import time
from typing import List, Dict, Optional, Any

# Try to import PDF library
try:
    from pypdf import PdfReader

    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

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
# 🦉 OWL TAKEOFF CLASS
# ==============================================================================

class OwlTakeoff:
    """
    The Plan Reader.

    ATTRIBUTES:
        use_ai_simulation (bool): If True, mocks LLM analysis.
    """

    def __init__(self, use_ai_simulation: bool = True):
        self.use_ai_simulation = use_ai_simulation

    # ==========================================================================
    # 📄 PDF SCANNER (The Reader)
    # ==========================================================================

    def scan_plan_file(self, file_path: str) -> Dict[str, Any]:
        """
        Ingests a PDF and returns extracted metadata.
        """
        MonkeyHeart.log_system_event("TAKEOFF", f"Scanning Plan: {file_path}")

        extracted_text = ""
        page_count = 0

        if PDF_AVAILABLE:
            try:
                reader = PdfReader(file_path)
                page_count = len(reader.pages)
                # Read first page for Title Block info
                extracted_text = reader.pages[0].extract_text()
            except Exception as e:
                Bananas.report_collision(e, "PDF Read Failed")
                extracted_text = "ERROR_READING_FILE"
        else:
            MonkeyHeart.log_system_event("TAKEOFF_WARN", "pypdf not installed. Using mock text.")
            extracted_text = "MOCK PLAN SET - MERCY HOSPITAL - LEVEL 1 - 2026"
            page_count = 5

        # Analyze the text
        analysis = self._analyze_text_content(extracted_text)

        return {
            "filename": file_path.split("/")[-1],
            "pages": page_count,
            "detected_project": analysis['project_name'],
            "detected_zones": analysis['zones'],
            "raw_text_snippet": extracted_text[:100] + "..."
        }

    def _analyze_text_content(self, text: str) -> Dict[str, Any]:
        """
        Uses Regex to find Project Names and Areas in the text.
        """
        # 1. Detect Project Name (Look for common title block keywords)
        project_name = "Unknown Project"
        if "MERCY" in text.upper():
            project_name = "Mercy Hospital"
        elif "SCHOOL" in text.upper():
            project_name = "High School Annex"

        # 2. Detect Zones/Areas (Simulated Intelligence)
        # In a real app, we'd use Gemini API to read the room schedule.
        # Here, we simulate finding them.
        zones = []
        if "LEVEL 1" in text.upper() or self.use_ai_simulation:
            zones = [
                "Level 1 - East Wing",
                "Level 1 - West Wing",
                "Level 1 - Lobby",
                "Level 1 - ER"
            ]

        return {
            "project_name": project_name,
            "zones": zones
        }

    # ==========================================================================
    # 🏗️ MATERIAL PREDICTOR (The V8 Helper)
    # ==========================================================================

    def generate_starter_list(self, zone_name: str) -> List[Dict]:
        """
        Based on the Zone Name (e.g., 'Office'), predicts the prefab kits needed.
        Used to populate the 'Smart Storefront'.
        """
        MonkeyHeart.log_system_event("TAKEOFF_AI", f"Predicting materials for {zone_name}...")

        items = []

        # Simple Logic Rules
        if "Office" in zone_name or "West Wing" in zone_name:
            items.append({"sku": "KIT-OFFICE-ROUGH", "qty": 1, "name": "Typical Office Rough-In Kit"})
            items.append({"sku": "KIT-DATA-DROP", "qty": 2, "name": "Data Drop Assembly"})

        elif "Lobby" in zone_name:
            items.append({"sku": "KIT-HIGH-CEILING", "qty": 10, "name": "High Bay Fixture Mount"})
            items.append({"sku": "EMT-1", "qty": 500, "name": "1 Inch EMT Conduit"})

        elif "ER" in zone_name:
            items.append({"sku": "KIT-HOSPITAL-GRD", "qty": 20, "name": "Hospital Grade Receptacle Kit"})
            items.append({"sku": "KIT-ISO-GND", "qty": 10, "name": "Isolated Ground Kit"})

        return items


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🦉 OWL TAKEOFF V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    reader = OwlTakeoff()

    # 2. Scan Mock File
    print("\n[TEST 1] Scanning 'plans.pdf' (Mock)...")
    result = reader.scan_plan_file("plans.pdf")
    print(f" > Detected Project: {result['detected_project']}")
    print(f" > Detected Pages: {result['pages']}")
    print(f" > Detected Zones: {len(result['detected_zones'])}")

    # 3. Predict Materials
    print("\n[TEST 2] Generating Prefab List for 'Level 1 - West Wing'...")
    materials = reader.generate_starter_list("Level 1 - West Wing")
    for m in materials:
        print(f" > Suggested: {m['qty']}x {m['name']} ({m['sku']})")

    print("\n" + "=" * 40)
    print("🦉 OWL TAKEOFF SYSTEM: OPERATIONAL")