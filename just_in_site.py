"""
JUST-IN-SITE V9.0 | THE OMNI-ENGINE
Contextual Logic for Field, Shop, and Office.
"""
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from typing import List
from monkey_brain import MonkeyBrain
from raptor_voice import RaptorVoice

app = FastAPI(); brain = MonkeyBrain(); voice = RaptorVoice()

# ALPHA HAT (Justin)
USERS = {
    "justin": {"name": "Justin (Alpha)", "hats": ["ADMIN", "PURCHASING", "PREFAB_MANAGER", "PROJECT_MANAGER"], "level": 6}
}

class VoiceRequest(BaseModel):
    command_text: str

@app.get("/")
async def dashboard(request: Request):
    user_id = request.cookies.get("active_user", "justin") # Auto-login for Alpha test
    user = USERS.get(user_id)
    return templates.TemplateResponse("index.html", {"request": request, **user})

@app.post("/inventory/voice-adjust")
async def voice_adjust(data: VoiceRequest):
    """Point 7 & 44: Raptor Voice Parsing into Ledger"""
    parsed = voice.parse_inventory_command(data.command_text)
    # Calculation: NewQty = OldQty ± Q
    return {"status": "SUCCESS", "parsed": parsed}

@app.get("/api/search")
async def neural_search(q: str):
    """Point 44: Ask the Monkey Search Hook"""
    return {"results": []}

@app.post("/api/system/sync-offline")
async def sync_offline(payload: List[dict]):
    """Point 48: Offline Data Sync Hook"""
    return {"status": "SYNCED", "count": len(payload)}