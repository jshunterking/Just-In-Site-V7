"""
JUST-IN-SITE V7.0 | WEB SERVER API + UI
The Full Stack Application with Login Security.

AUTHOR: Justin (King Kong) & Gemini (The Architect)
DATE: 2026-01-20
"""

from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

# --- IMPORT LIMBS (Safe Mode) ---
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
templates = Jinja2Templates(directory="templates")

# Initialize Systems
clock = RabbitTime() if RabbitTime else None
brain = PantherBrain() if PantherBrain else None
paws = RabbitPaws() if RabbitPaws else None
voice = RaptorVoice() if RaptorVoice else None


# --- MODELS ---
class LoginRequest(BaseModel):
    username: str
    password: str


class ClockInRequest(BaseModel):
    user_id: str
    job_id: str
    lat: float
    lon: float


# --- SECURITY MIDDLEWARE ---
def verify_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token or token != "v7-secure-uplink":
        return False
    return True


# --- UI ROUTES ---

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Serve the 22nd Century Login Screen."""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve Dashboard (Protected)."""
    # Check if user has the 'key' (cookie)
    if not verify_cookie(request):
        return RedirectResponse(url="/login")

    return templates.TemplateResponse("index.html", {"request": request})


# --- AUTH API ---

@app.post("/auth/login")
def login(data: LoginRequest, response: Response):
    """
    Validates credentials.
    HARDCODED FOR PROTOTYPE: User 'Justin' / Pass 'admin'
    """
    if data.username.lower() == "justin" and data.password == "admin":
        # Set a cookie that lasts for 24 hours
        response.set_cookie(key="access_token", value="v7-secure-uplink", max_age=86400)
        return {"message": "Access Granted"}
    else:
        raise HTTPException(status_code=401, detail="Invalid Credentials")


@app.get("/auth/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return RedirectResponse(url="/login")


# --- API ROUTES (The Engine) ---

@app.post("/rabbit/clock-in")
def api_clock_in(data: ClockInRequest):
    if not clock: raise HTTPException(status_code=503, detail="System Offline")
    result = clock.clock_in(data.user_id, data.job_id, data.lat, data.lon)
    if result['success']:
        return result
    else:
        raise HTTPException(status_code=400, detail=result['reason'])


@app.get("/rabbit/status/{user_id}")
def api_get_status(user_id: str):
    if not clock: return {"status_message": "System Offline"}
    return {"status_message": clock.get_status(user_id)}