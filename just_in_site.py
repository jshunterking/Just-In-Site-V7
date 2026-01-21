"""
JUST-IN-SITE V7.1 | GOLDEN MASTER ENGINE
Full Stack: Auth, Logic, UI, and API.
"""
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

# --- IMPORT LIMBS (Safe Mode) ---
try:
    from rabbit_time import RabbitTime
    from panther_brain import PantherBrain
    from rabbit_paws import RabbitPaws
    from raptor_voice import RaptorVoice
except ImportError:
    RabbitTime = None; PantherBrain = None; RabbitPaws = None; RaptorVoice = None

# --- SETUP ---
app = FastAPI(title="Just-In-Site V7.1")
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

class ClockOutRequest(BaseModel):
    user_id: str

class MaterialRequest(BaseModel):
    user_id: str
    job_id: str
    sku: str
    qty: int

# --- SECURITY ---
def verify_cookie(request: Request):
    token = request.cookies.get("access_token")
    return token == "v7-secure-uplink"

# --- UI ROUTES ---
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if not verify_cookie(request): return RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request})

# --- AUTH API ---
@app.post("/auth/login")
def login(data: LoginRequest, response: Response):
    # HARDCODED CREDENTIALS
    if data.username.lower() == "justin" and data.password == "admin":
        response.set_cookie(key="access_token", value="v7-secure-uplink", max_age=86400)
        return {"message": "Access Granted"}
    raise HTTPException(status_code=401, detail="Invalid Credentials")

@app.get("/auth/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return RedirectResponse(url="/login")

# --- DATA API ---
@app.get("/api/jobs")
def get_jobs():
    return [
        {"id": "JOB-MERCY-001", "name": "Mercy Hospital - ER Reno"},
        {"id": "JOB-STEEL-004", "name": "Cleveland Cliffs - Blast Furnace"},
        {"id": "JOB-RES-299",   "name": "Smith Residence - Service"},
        {"id": "JOB-SHOP-000",  "name": "Pre-Fab Shop"}
    ]

# 🐇 RABBIT OPERATIONS
@app.post("/rabbit/clock-in")
def api_clock_in(data: ClockInRequest):
    if not clock: raise HTTPException(status_code=503, detail="Offline")
    res = clock.clock_in(data.user_id, data.job_id, data.lat, data.lon)
    if res['success']: return res
    raise HTTPException(status_code=400, detail=res['reason'])

@app.post("/rabbit/clock-out")
def api_clock_out(data: ClockOutRequest):
    if not clock: raise HTTPException(status_code=503, detail="Offline")
    res = clock.clock_out(data.user_id)
    if res['success']: return res
    raise HTTPException(status_code=400, detail=res['reason'])

@app.get("/rabbit/status/{user_id}")
def api_get_status(user_id: str):
    if not clock: return {"status_message": "System Offline", "clocked_in": False}
    msg = clock.get_status(user_id)
    return {"status_message": msg, "clocked_in": "CLOCKED IN" in msg}

@app.post("/rabbit/requisition")
def api_create_req(data: MaterialRequest):
    if not paws: raise HTTPException(status_code=503, detail="Offline")
    items = [{"sku": data.sku, "qty": data.qty, "est_cost": 0.00}]
    return paws.create_requisition(data.job_id, data.user_id, items)

# 🐆 PANTHER OPERATIONS
@app.get("/panther/tickets")
def get_tickets():
    if not brain: return []
    return brain.tickets