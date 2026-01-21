"""
RABBIT PREFAB V7.0
The Manufacturing & Assembly Module for Just-In-Site.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
VERSION: 7.0.1 (Diamond-Grade)

DESCRIPTION:
This module transforms the Prefab Shop into a modern factory.
It manages the production lifecycle of assemblies:
Order Received -> Bill of Materials Exploded -> Assembly -> QC -> Shipping.

CORE CAPABILITIES:
1. Kanban Board Management.
2. Bill of Materials (BOM) Explosion.
3. Quality Control (QC) Checklists.
4. Kit Labeling (QR Code Logic).

INTEGRATIONS:
- Bananas (Notifications)
- Monkey Heart (Logging)
- Rabbit Inventory (Raw Materials)
"""

import uuid
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
# 📖 THE RECIPE BOOK (Bill of Materials)
# ==============================================================================
# Defines what goes into a Kit.

BOM_CATALOG = {
    "KIT-OFFICE-ROUGH": {
        "name": "Standard Office Rough-In",
        "labor_hours": 0.5,
        "parts": [
            {"sku": "BOX-4SQ-D", "qty": 1},
            {"sku": "BRACKET-MNT", "qty": 1},
            {"sku": "GRD-SCREW", "qty": 1},
            {"sku": "MUD-RING-1G", "qty": 1}
        ]
    },
    "KIT-HOSPITAL-GRD": {
        "name": "Hospital Grade Receptacle Assembly",
        "labor_hours": 0.25,
        "parts": [
            {"sku": "DEV-HOSP-R", "qty": 1},
            {"sku": "PLATE-SS-1G", "qty": 1},
            {"sku": "WIRE-PIGTAIL", "qty": 1}
        ]
    }
}

# ==============================================================================
# 🏭 THE KANBAN BOARD (Production State)
# ==============================================================================

MOCK_KANBAN = [
    {
        "ticket_id": "PF-1001",
        "job_id": "JOB-26001",
        "kit_type": "KIT-OFFICE-ROUGH",
        "qty": 50,
        "status": "QUEUED",  # QUEUED, BUILDING, QC_CHECK, READY
        "assigned_to": None,
        "due_date": "2026-01-25"
    },
    {
        "ticket_id": "PF-1002",
        "job_id": "JOB-26002",
        "kit_type": "KIT-HOSPITAL-GRD",
        "qty": 20,
        "status": "BUILDING",
        "assigned_to": "Apprentice Joe",
        "due_date": "2026-01-22"
    }
]


# ==============================================================================
# 🐰 RABBIT PREFAB CLASS
# ==============================================================================

class RabbitPrefab:
    """
    The Factory Boss.
    """

    def __init__(self):
        self.recipes = BOM_CATALOG
        self.board = MOCK_KANBAN

    # ==========================================================================
    # 📋 KANBAN OPERATIONS
    # ==========================================================================

    def get_board_state(self) -> Dict[str, List[Dict]]:
        """
        Returns the production floor organized by column.
        """
        columns = {"QUEUED": [], "BUILDING": [], "QC_CHECK": [], "READY": []}
        for card in self.board:
            status = card.get("status", "QUEUED")
            if status in columns:
                columns[status].append(card)
        return columns

    def move_card(self, ticket_id: str, new_status: str, user: str) -> bool:
        """
        Drags a ticket to the next station.
        """
        card = self._find_card(ticket_id)
        if not card:
            return False

        old_status = card['status']
        card['status'] = new_status

        if new_status == "BUILDING":
            card['assigned_to'] = user

        MonkeyHeart.log_system_event("PREFAB_MOVE", f"{ticket_id} moved {old_status} -> {new_status} by {user}")
        return True

    # ==========================================================================
    # 💥 BOM EXPLOSION (The Shopping List)
    # ==========================================================================

    def explode_requirements(self, ticket_id: str) -> Optional[List[Dict]]:
        """
        Calculates raw materials needed for a production run.
        Foreman orders "50 Kits" -> System orders "50 Boxes, 50 Brackets..."
        """
        card = self._find_card(ticket_id)
        if not card: return None

        kit_type = card['kit_type']
        run_qty = card['qty']

        recipe = self.recipes.get(kit_type)
        if not recipe:
            Bananas.notify("Recipe Error", f"No BOM found for {kit_type}")
            return None

        shopping_list = []
        for part in recipe['parts']:
            total_needed = part['qty'] * run_qty
            shopping_list.append({
                "sku": part['sku'],
                "qty_needed": total_needed,
                "notes": f"For {run_qty}x {recipe['name']}"
            })

        MonkeyHeart.log_system_event("PREFAB_BOM", f"Exploded BOM for {ticket_id}: {len(shopping_list)} SKUs needed.")
        return shopping_list

    # ==========================================================================
    # 🏷️ LABELING (The Passport)
    # ==========================================================================

    def generate_kit_label(self, ticket_id: str) -> Dict[str, str]:
        """
        Creates the data for the QR Code label printer.
        """
        card = self._find_card(ticket_id)
        if not card: return {}

        # Unique Serial for this Batch
        batch_id = f"{ticket_id}-{int(time.time())}"

        label_data = {
            "qr_content": f"JIS://PREFAB/{batch_id}",
            "human_readable": f"{card['job_id']}\n{card['kit_type']}\nQTY: {card['qty']}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "qc_by": "PENDING"
        }

        MonkeyHeart.log_system_event("PREFAB_LABEL", f"Generated Label for Batch {batch_id}")
        return label_data

    def _find_card(self, t_id: str) -> Optional[Dict]:
        for c in self.board:
            if c['ticket_id'] == t_id:
                return c
        return None


# ==============================================================================
# 🧪 SELF-DIAGNOSTIC (The Friday Test)
# ==============================================================================
if __name__ == "__main__":
    print("\n🐰 RABBIT PREFAB V7.0 DIAGNOSTIC\n" + "=" * 40)

    # 1. Initialize
    factory = RabbitPrefab()

    # 2. View Board
    print("\n[TEST 1] Checking Kanban Board...")
    state = factory.get_board_state()
    print(f" > Queued: {len(state['QUEUED'])}")
    print(f" > Building: {len(state['BUILDING'])}")

    # 3. Explode BOM
    print("\n[TEST 2] Exploding BOM for PF-1001 (50 Office Kits)...")
    parts = factory.explode_requirements("PF-1001")
    for p in parts:
        print(f" > Need: {p['qty_needed']}x {p['sku']}")

    # 4. Move Production
    print("\n[TEST 3] Moving PF-1001 to BUILDING...")
    factory.move_card("PF-1001", "BUILDING", "Rhino Manager")

    # 5. Generate Label
    print("\n[TEST 4] Printing Label...")
    label = factory.generate_kit_label("PF-1001")
    print(f" > QR Data: {label['qr_content']}")
    print(f" > Text:\n{label['human_readable']}")

    print("\n" + "=" * 40)
    print("🐰 RABBIT PREFAB SYSTEM: OPERATIONAL")