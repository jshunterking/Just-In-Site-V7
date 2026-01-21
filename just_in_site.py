"""
JUST-IN-SITE V7.0 | WEB SERVER API + UI
The Full Stack Application.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional

# --- IMPORT LIMBS ---
try:
    from rabbit_time import RabbitTime
    from panther_brain import PantherBrain
    from rabbit_paws import RabbitPaws
    from raptor_voice import RaptorVoice
except ImportError:
    RabbitTime = None
    PantherBrain = None
    RabbitPaws = None
    RaptorVoice = None

# --- APP SETUP ---
app = FastAPI(title="Just-In-Site V7.0")

# Setup Templates (This points to your new folder)
templates = Jinja2Templates(directory="templates")

# Initialize Systems
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

# --- THE UI ROUTE (The Face) ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the dashboard HTML.
    """
    return templates.TemplateResponse("index.html", {"request": request})

# --- THE API ROUTES (The Engine) ---

@app.post("/rabbit/clock-in")
def api_clock_in(data: ClockInRequest):
    if not clock: raise HTTPException(status_code=503, detail="System Offline")
    result = clock.clock_in(data.user_id, data.job_id, data.lat, data.lon)
    if result['success']: return result
    else: raise HTTPException(status_code=400, detail=result['reason'])

@app.get("/rabbit/status/{user_id}")
def api_get_status(user_id: str):
    if not clock: return {"status_message": "System Offline"}
    return {"status_message": clock.get_status(user_id)}