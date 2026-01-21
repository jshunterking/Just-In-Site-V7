"""
JUST-IN-SITE V7.0 | WEB SERVER API (SAFE MODE)
The connectivity layer. Robust against missing files.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# --- IMPORT THE LIMBS (Safely) ---
try:
    from rabbit_time import RabbitTime
except ImportError:
    RabbitTime = None
    print("⚠️ MISSING: rabbit_time.py")

try:
    from panther_brain import PantherBrain
except ImportError:
    PantherBrain = None
    print("⚠️ MISSING: panther_brain.py")

try:
    from rabbit_paws import RabbitPaws
except ImportError:
    RabbitPaws = None
    print("⚠️ MISSING: rabbit_paws.py")

try:
    from raptor_voice import RaptorVoice
except ImportError:
    RaptorVoice = None
    print("⚠️ MISSING: raptor_voice.py")

# --- INITIALIZE THE APP ---
app = FastAPI(
    title="Just-In-Site V7.0 API",
    description="The Central Nervous System for Field & Service Operations.",
    version="7.0.3"
)

# --- WAKE UP THE SYSTEMS (If they exist) ---
clock = RabbitTime() if RabbitTime else None
brain = PantherBrain() if PantherBrain else None
paws = RabbitPaws() if RabbitPaws else None
voice = RaptorVoice() if RaptorVoice else None


# --- DATA MODELS ---
class ClockInRequest(BaseModel):
    user_id: str
    job_id: str
    lat: float
    lon: float


class VoiceCommandRequest(BaseModel):
    user_id: str
    audio_transcript: str


class MaterialRequest(BaseModel):
    user_id: str
    job_id: str
    sku: str
    qty: int


# --- THE ENDPOINTS ---

@app.get("/")
def home():
    """Heartbeat check."""
    # Build a status report of what is actually running
    status = {
        "system": "Just-In-Site V7.0",
        "status": "ONLINE",
        "modules": {
            "RabbitTime": "🟢 ONLINE" if clock else "🔴 MISSING",
            "PantherBrain": "🟢 ONLINE" if brain else "🔴 MISSING",
            "RabbitPaws": "🟢 ONLINE" if paws else "🔴 MISSING",
            "RaptorVoice": "🟢 ONLINE" if voice else "🔴 MISSING",
        }
    }
    return status


# 🐇 RABBIT: TIME CLOCK
@app.post("/rabbit/clock-in")
def api_clock_in(data: ClockInRequest):
    if not clock:
        raise HTTPException(status_code=503, detail="Rabbit Time module is missing.")

    result = clock.clock_in(data.user_id, data.job_id, data.lat, data.lon)
    if result['success']:
        return result
    else:
        raise HTTPException(status_code=400, detail=result['reason'])


@app.get("/rabbit/status/{user_id}")
def api_get_status(user_id: str):
    if not clock:
        return "System Offline"
    return {"status_message": clock.get_status(user_id)}


# 🐇 RABBIT: MATERIAL
@app.post("/rabbit/requisition")
def api_create_req(data: MaterialRequest):
    if not paws:
        raise HTTPException(status_code=503, detail="Rabbit Paws module is missing.")
    # Mock cost for now
    items = [{"sku": data.sku, "qty": data.qty, "est_cost": 50.00}]
    result = paws.create_requisition(data.job_id, data.user_id, items)
    return result


# 🐆 PANTHER: TICKETS
@app.get("/panther/tickets")
def get_tickets():
    if not brain:
        return []
    return brain.tickets


# 🦕 RAPTOR: VOICE
@app.post("/raptor/command")
def process_voice(data: VoiceCommandRequest):
    if not voice:
        raise HTTPException(status_code=503, detail="Raptor Voice module is missing.")
    result = voice.process_voice_command(data.user_id, data.audio_transcript)
    return result