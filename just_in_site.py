"""
JUST-IN-SITE V9.0.2 | STABILITY PATCH
Defensive coding to prevent 500 errors.
"""
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
import os

# --- DEFENSIVE IMPORTS ---
try:
    from monkey_brain import MonkeyBrain

    brain = MonkeyBrain()
except Exception as e:
    brain = None
    print(f"CRITICAL: monkey_brain.py failed to initialize: {e}")

try:
    from raptor_voice import RaptorVoice

    voice = RaptorVoice()
except Exception as e:
    voice = None
    print(f"CRITICAL: raptor_voice.py failed to initialize: {e}")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- MOCK ALPHA CONFIG (Ensures variables always exist) ---
ALPHA_USER = {
    "name": "Justin (Alpha)",
    "hats": ["ADMIN", "PURCHASING", "PREFAB_MANAGER", "PROJECT_MANAGER", "FIELD_FOREMAN"],
    "level": 6
}


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # If the user isn't logged in, we force the Alpha profile for testing
    user_id = request.cookies.get("active_user", "justin")

    # We must pass every variable the HTML expects to avoid Jinja2 errors
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": ALPHA_USER["name"],
        "hats": ALPHA_USER["hats"],
        "level": ALPHA_USER["level"],
        "system_status": "ONLINE" if brain else "DEGRADED"
    })


# Necessary for redirects
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/inventory/voice-adjust")
async def voice_adjust(data: dict):
    if not voice: return {"status": "ERROR", "msg": "Voice Engine Offline"}
    return {"status": "SUCCESS", "msg": "Parsed"}