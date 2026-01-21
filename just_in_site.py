"""
JUST-IN-SITE V7.0 | WEB SERVER API
The connectivity layer. This replaces the old text console.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# --- IMPORT THE LIMBS ---
# These are the logic modules you already built.
try:
    from rabbit_time import RabbitTime
    from panther_brain import PantherBrain
    from rabbit_paws import RabbitPaws
    from raptor_voice import RaptorVoice
except ImportError as e:
    print(f"❌ MISSING LIMB: {e}")
    # We continue so the server can start, but endpoints might fail
    pass

# --- INITIALIZE THE APP ---
app = FastAPI(
    title="Just-In-Site V7.0 API",
    description="The Central Nervous System for Field & Service Operations.",
    version="7.0.2"
)

# --- WAKE UP THE SYSTEMS ---
# These run once when the server starts
clock = RabbitTime()
brain = PantherBrain()
paws = RabbitPaws()
voice = RaptorVoice()


# --- DATA MODELS (The Forms) ---
# These define what data the frontend MUST send us.

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


# --- THE ENDPOINTS (The Routes) ---

@app.get("/")
def home():
    """Heartbeat check."""
    return {
        "system": "Just-In-Site V7.0",
        "status": "ONLINE",
        "location": "Youngstown, OH",
        "timestamp": "2026-01-20"
    }


# 🐇 RABBIT: TIME CLOCK
@app.post("/rabbit/clock-in")
def api_clock_in(data: ClockInRequest):
    """
    Receives GPS data and attempts to clock the user in.
    """
    result = clock.clock_in(data.user_id, data.job_id, data.lat, data.lon)

    if result['success']:
        return result
    else:
        # If geo-fence fails or already clocked in, return 400 Bad Request
        raise HTTPException(status_code=400, detail=result['reason'])


@app.get("/rabbit/status/{user_id}")
def api_get_status(user_id: str):
    """
    Checks if a specific user is clocked in.
    """
    return {"status_message": clock.get_status(user_id)}


# 🐇 RABBIT: MATERIAL
@app.post("/rabbit/requisition")
def api_create_req(data: MaterialRequest):
    """
    Field user requesting material.
    """
    # Mock cost for now
    items = [{"sku": data.sku, "qty": data.qty, "est_cost": 50.00}]
    result = paws.create_requisition(data.job_id, data.user_id, items)
    return result


# 🐆 PANTHER: TICKETS
@app.get("/panther/tickets")
def get_tickets():
    """
    Returns the list of active service tickets.
    """
    return brain.tickets


# 🦕 RAPTOR: VOICE
@app.post("/raptor/command")
def process_voice(data: VoiceCommandRequest):
    """
    The AI Voice Processor.
    """
    result = voice.process_voice_command(data.user_id, data.audio_transcript)
    return result