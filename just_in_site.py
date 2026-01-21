"""
JUST-IN-SITE V8.1 | OMNI-ENGINE
"""
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from raptor_voice import RaptorVoice
from monkey_brain import MonkeyBrain

app = FastAPI()
templates = Jinja2Templates(directory="templates")
brain = MonkeyBrain()
voice = RaptorVoice()

# ALPHA USER (Justin)
USERS = {
    "justin": {
        "name": "Justin (Alpha)",
        "hats": ["ADMIN", "PURCHASING", "PREFAB_MANAGER", "FIELD_FOREMAN"],
        "level": 6
    }
}

class VoiceRequest(BaseModel):
    command_text: str

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_id = request.cookies.get("active_user")
    user = USERS.get(user_id)
    if not user: return RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request, "name": user["name"], "hats": user["hats"], "level": user["level"]})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/auth/login")
def login(response: Response):
    response.set_cookie(key="active_user", value="justin", max_age=86400)
    return {"status": "Uplink Secure"}

@app.post("/inventory/voice-adjust")
async def voice_adjust(data: VoiceRequest):
    parsed = voice.parse_inventory_command(data.command_text)
    # This would call brain.adjust_inventory_ledger(parsed)
    return {"status": "SUCCESS", "parsed": parsed}

@app.get("/api/vault/files")
def get_vault():
    return [{"filename": "MERCY_OR3_Racks.pdf"}, {"filename": "STEEL_MILL_Spider.pdf"}]