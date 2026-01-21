"""
JUST-IN-SITE V10.0.1 | THE GALAXY CORE
Monolith Build: AI Take-Off, Manpower, Kanban, and Estimating.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3


# --- 1. THE BRAIN ---
def init_db():
    conn = sqlite3.connect("monkey_core.db")
    c = conn.cursor()
    # Tables for new modules
    c.execute('CREATE TABLE IF NOT EXISTS takeoffs (id INTEGER PRIMARY KEY, drawing_name TEXT, status TEXT)')
    c.execute(
        'CREATE TABLE IF NOT EXISTS manpower (id INTEGER PRIMARY KEY, worker_name TEXT, job_id TEXT, status TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS bids (id INTEGER PRIMARY KEY, job_name TEXT, bid_amt REAL, actual_amt REAL)')
    conn.commit()
    conn.close()


# --- 2. THE ENGINE ---
print("------------------------------------------")
print("!!! JUST-IN-SITE V10.0.1: GALAXY CORE  !!!")
print("!!!    DFNO! BATTLESTATIONS ACTIVE     !!!")
print("------------------------------------------")

app = FastAPI()
init_db()

# THE ALPHA CONFIG
JUSTIN_HATS = ["ADMIN", "PURCHASING", "PREFAB_MANAGER", "PROJECT_MANAGER", "ESTIMATOR"]


@app.get("/", response_class=HTMLResponse)
async def bridge():
    # Sidebar Navigation with New Modules
    nav_links = [
        {"id": "takeoff", "label": "AI Auto Take-Off", "icon": "fa-robot", "color": "text-blue-400"},
        {"id": "manpower", "label": "Manpower Capsule", "icon": "fa-users-viewfinder", "color": "text-orange-400"},
        {"id": "kanban", "label": "Prefab Orbit", "icon": "fa-gears", "color": "text-purple-400"},
        {"id": "estimator", "label": "Bid Trajectory", "icon": "fa-chart-line", "color": "text-green-400"},
        {"id": "vault", "label": "The Vault", "icon": "fa-vault", "color": "text-slate-400"}
    ]

    nav_html = "".join([f"""
        <button onclick="showModule('{n['id']}')" class="nav-btn">
            <i class="fa-solid {n['icon']} {n['color']}"></i>
            <span>{n['label']}</span>
        </button>
    """ for n in nav_links])

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Just-In-Site | V10.0.1</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
        <style>
            body {{ background: #020617; color: #f8fafc; font-family: 'Rajdhani', sans-serif; overflow: hidden; }}
            .font-orbitron {{ font-family: 'Orbitron', sans-serif; }}
            .neon-text {{ text-shadow: 0 0 15px #22d3ee; }}
            .glass {{ background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(34, 211, 238, 0.1); backdrop-filter: blur(20px); }}
            .sidebar {{ background: #070712; border-right: 1px solid #1e1b4b; }}
            .nav-btn {{ width: 100%; display: flex; align-items: center; padding: 14px 24px; gap: 12px; color: #94a3b8; transition: 0.2s; border-left: 3px solid transparent; }}
            .nav-btn:hover {{ background: rgba(34, 211, 238, 0.05); color: #fff; border-left-color: #22d3ee; }}
            .kanban-col {{ background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; padding: 20px; min-height: 400px; }}
        </style>
    </head>
    <body class="flex h-screen">

        <aside class="sidebar w-72 flex flex-col z-20">
            <div class="p-8 border-b border-white/5">
                <h1 class="font-orbitron text-xl font-black text-white italic neon-text">MONKEYS</h1>
                <p class="text-[0.6rem] text-cyan-400 font-bold tracking-[0.4em] uppercase">V10.0.1 // ALPHA</p>
            </div>
            <nav class="flex-1 mt-4">{nav_html}</nav>
        </aside>

        <main class="flex-1 p-12 overflow-y-auto">
            <div class="max-w-7xl mx-auto">

                <div class="text-center mb-12">
                    <h1 class="font-orbitron text-6xl font-black text-white italic neon-text uppercase">Just-In-Site</h1>
                    <p class="text-cyan-400 font-mono text-xs tracking-[0.6em] uppercase mt-2">"The Single Source of Truth"</p>
                </div>

                <div id="viewport">
                    <div id="module-kanban" class="space-y-6">
                        <div class="flex justify-between items-center">
                            <h2 class="font-orbitron text-2xl font-bold italic tracking-tighter">PREFAB PRODUCTION ORBIT</h2>
                            <button onclick="triggerBananas()" class="text-[0.6rem] text-slate-600 uppercase font-bold hover:text-red-500">Force Error</button>
                        </div>
                        <div class="grid grid-cols-4 gap-6">
                            <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-slate-500 mb-4 tracking-widest uppercase">Launchpad</h3><div class="glass p-4 rounded-xl text-xs mb-2">MERCY-RACK-01</div></div>
                            <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-blue-500 mb-4 tracking-widest uppercase">Assembly</h3><div class="glass p-4 rounded-xl text-xs mb-2 border-l-2 border-blue-500">STEEL-SPIDER-A</div></div>
                            <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-purple-500 mb-4 tracking-widest uppercase">Flight Check</h3></div>
                            <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-green-500 mb-4 tracking-widest uppercase">In Orbit</h3></div>
                        </div>
                    </div>
                </div>

            </div>
        </main>

        <div id="bananaError" class="fixed inset-0 z-[100] bg-black/95 flex flex-col items-center justify-center hidden text-center p-10">
            <i class="fa-solid fa-triangle-exclamation text-8xl text-yellow-500 mb-8 animate-bounce"></i>
            <h2 class="font-orbitron text-4xl font-black text-white italic mb-2 uppercase tracking-tighter">THAT'S BANANAS!</h2>
            <p class="text-yellow-500 font-mono text-sm max-w-md">The neural link hit a snag. The Monkeys are currently resetting the circuit breakers. Stand by for orbital re-entry.</p>
            <button onclick="hideBananas()" class="mt-10 px-8 py-3 bg-yellow-600 text-black font-bold font-orbitron text-xs rounded-full">REBOOT NEURAL CORE</button>
        </div>

        <script>
            function showModule(id) {{
                // Logic to switch viewports
                console.log("Switching to " + id);
            }}

            function triggerBananas() {{
                document.getElementById('bananaError').classList.remove('hidden');
            }}

            function hideBananas() {{
                document.getElementById('bananaError').classList.add('hidden');
            }}
        </script>
    </body>
    </html>
    """