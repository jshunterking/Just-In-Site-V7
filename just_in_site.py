from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from monkey_brain import MonkeyBrain

print("------------------------------------------")
print("!!! MONKEYS V9.01.FINAL IS NOW LOADING !!!")
print("!!!    DFNO! BLAST OFF INITIALIZED     !!!")
print("------------------------------------------")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
brain = MonkeyBrain()

# THE ALPHA CONFIG
JUSTIN_HATS = ["ADMIN", "PURCHASING", "PREFAB_MANAGER", "PROJECT_MANAGER"]

@app.get("/", response_class=HTMLResponse)
async def bridge(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "v": "V9.01",
        "name": "Justin (Alpha)",
        "hats": JUSTIN_HATS,
        "level": 6
    })