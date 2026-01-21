"""
JUST-IN-SITE V10.01.3 | THE MONKEY SPACE SINGULARITY
Monolith Build: 8-10 Modules per Hat, AI Engine, Manpower, and Bananas Protocol.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3


# --- 1. THE BRAIN (The Single Source of Truth) ---
def init_db():
    conn = sqlite3.connect("monkey_core.db")
    c = conn.cursor()
    # Foundational tables for the 60-Module Matrix
    c.execute('CREATE TABLE IF NOT EXISTS inventory (item TEXT, job_id TEXT, qty REAL, uom TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS manpower (name TEXT, job_id TEXT, burn_rate REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS bids (job_name TEXT, status TEXT, trajectory REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS prefab (qr_id TEXT, stage TEXT, bom TEXT)')
    conn.commit()
    conn.close()


# --- 2. THE ENGINE ---
print("------------------------------------------")
print("!!! JUST-IN-SITE V10.01.3: MONKEY SPACE !!!")
print("!!!    DFNO! ALL SYSTEMS GO-FLIGHT     !!!")
print("------------------------------------------")

app = FastAPI()
init_db()

# MASTER HAT MATRIX
HATS = {
    "ADMIN": ["Neural Hat Manager", "Global Kill-Switch", "Truth Audit Log", "Database Pulse", "Bananas Override",
              "Financial Pulse", "Ghost Mode", "API Command", "Activity Heatmap", "Nitrous Broadcast"],
    "PURCHASING": ["The Buy-Board", "Vendor Radar", "UOM Engine", "Restock Alert", "Copper Index", "Packing Slip OCR",
                   "Scrap Ledger", "Bulk Strategy", "Backorder Watchdog", "Bin Locators"],
    "PROJECT_MANAGER": ["Master Vault", "Submittal Radar", "Change Order Pulse", "Job-Cost Heatmap", "RFI Live-Link",
                        "Labor Velocity", "Manpower Capsule", "Punch-List", "Site Quick-Card", "Utility Ledger"],
    "PREFAB_MANAGER": ["Prefab Orbit", "QR Neural Linker", "BOM Pop-up", "Load Balancer", "Shortage Panic",
                       "3D Viewport", "Label Printer", "QC Flight Check", "Logistics", "History Audit"],
    "ESTIMATOR": ["AI Take-Off", "Pricing Library", "Quote Matrix", "Labor Multiplier", "Scope Generator",
                  "Risk Matrix", "Margin Pulse", "Addenda Log", "Bid Ticker", "Post-Mortem Sync"],
    "FOREMAN": ["Raptor Voice", "Time Approvals", "The Teaching Loop", "Safety Journal", "Markup Sync",
                "Surplus Scanner", "Travel Tracker", "Tool Tethering"]
}


@app.get("/", response_class=HTMLResponse)
async def bridge():
    # Build the Sidebar Navigation based on the Hat Matrix
    sidebar_html = ""
    for role, modules in HATS.items():
        role_color = "text-cyan-400" if role == "ADMIN" else "text-purple-400"
        sidebar_html += f'<div class="px-6 py-2 text-[0.6rem] font-bold {role_color} tracking-widest uppercase border-b border-white/5 mb-2 mt-4">{role.replace("_", " ")}</div>'
        for mod in modules:
            sidebar_html += f'<button onclick="loadModule(\'{mod}\')" class="nav-btn"><span>{mod}</span></button>'

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Just-In-Site | V10.01.3</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
        <style>
            body {{ background: #020617; color: #f8fafc; font-family: 'Rajdhani', sans-serif; overflow: hidden; }}
            .font-orbitron {{ font-family: 'Orbitron', sans-serif; }}
            .neon-text {{ text-shadow: 0 0 20px #22d3ee; color: #fff; }}
            .glass {{ background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(34, 211, 238, 0.15); backdrop-filter: blur(25px); }}
            .sidebar {{ background: #05050f; border-right: 1px solid #1e1b4b; overflow-y: auto; }}
            .nav-btn {{ width: 100%; text-align: left; padding: 10px 24px; font-size: 0.75rem; color: #64748b; transition: 0.2s; }}
            .nav-btn:hover {{ color: #22d3ee; background: rgba(34, 211, 238, 0.05); }}
            .viewport-header {{ border-bottom: 2px solid #22d3ee; }}
        </style>
    </head>
    <body class="flex h-screen">

        <aside class="sidebar w-72 flex flex-col z-20">
            <div class="p-8 border-b border-white/5">
                <h1 class="font-orbitron text-xl font-black italic neon-text">MONKEYS</h1>
                <p class="text-[0.6rem] text-cyan-400 font-bold tracking-[0.4em] uppercase">V10.01.3 // SPACE</p>
            </div>
            <nav class="flex-1">{sidebar_html}</nav>
        </aside>

        <main class="flex-1 p-12 overflow-y-auto">
            <div class="max-w-7xl mx-auto">

                <div class="text-center mb-16">
                    <h1 class="font-orbitron text-8xl font-black text-white italic neon-text uppercase tracking-tighter">Just-In-Site</h1>
                    <p class="text-cyan-400 font-mono text-sm tracking-[0.7em] uppercase mt-4">"The Single Source of Truth"</p>
                </div>

                <div id="module-viewport" class="glass rounded-[40px] p-12 min-h-[600px] relative">
                    <div id="viewport-content">
                        <div class="text-center py-20">
                            <i class="fa-solid fa-satellite text-6xl text-slate-700 mb-6 animate-pulse"></i>
                            <h2 class="font-orbitron text-3xl font-bold italic text-slate-500 uppercase">Select a Module to Uplink</h2>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <div id="bananaModal" class="fixed inset-0 z-[100] bg-black/98 flex flex-col items-center justify-center hidden">
            <div class="text-center p-12 border-4 border-yellow-500 rounded-[50px] glass">
                <i class="fa-solid fa-triangle-exclamation text-9xl text-yellow-500 mb-8"></i>
                <h2 class="font-orbitron text-6xl font-black text-white italic uppercase tracking-tighter">THAT'S BANANAS!</h2>
                <p class="text-yellow-500 font-mono text-lg mt-4 uppercase tracking-widest">Neural Link Interrupted // Reboot Required</p>
                <button onclick="location.reload()" class="mt-12 px-12 py-4 bg-yellow-500 text-black font-black font-orbitron text-sm rounded-full hover:scale-105 transition">REBOOT CORE</button>
            </div>
        </div>

        <script>
            function loadModule(name) {{
                const viewport = document.getElementById('viewport-content');
                // Simulating Module Load
                viewport.innerHTML = `
                    <div class="viewport-header pb-4 mb-8 flex justify-between items-end">
                        <h2 class="font-orbitron text-4xl font-black italic uppercase tracking-tighter text-white">${{name}}</h2>
                        <span class="text-cyan-400 font-mono text-xs uppercase tracking-widest">Module Active // DFNO</span>
                    </div>
                    <div class="grid grid-cols-12 gap-8">
                        <div class="col-span-12 glass p-8 rounded-3xl border-white/5 h-64 flex items-center justify-center">
                            <div class="text-center">
                                <i class="fa-solid fa-microchip text-4xl text-cyan-400/30 mb-4"></i>
                                <p class="text-slate-500 font-mono text-sm uppercase">Initializing Logic for ${{name}}...</p>
                            </div>
                        </div>
                    </div>
                    <button onclick="triggerBananas()" class="mt-8 text-slate-800 text-[0.6rem] uppercase font-bold">Debug: Snag Circuit</button>
                `;
            }}

            function triggerBananas() {{ document.getElementById('bananaModal').classList.remove('hidden'); }}
        </script>
    </body>
    </html>
    """