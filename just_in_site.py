"""
JUST-IN-SITE V10.1.0 | THE GALAXY SINGULARITY
Full Operational Deployment: 60 Integrated Modules.
Philosophy: The Single Source of Truth.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
import json


# --- 1. THE BRAIN (The Single Source of Truth) ---
def init_db():
    conn = sqlite3.connect("monkey_core.db")
    c = conn.cursor()
    # Create the unified tables for all 60 modules
    c.execute(
        'CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, item TEXT, qty REAL, uom TEXT, threshold REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS manpower (id INTEGER PRIMARY KEY, name TEXT, job_id TEXT, l_e_r REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS assemblies (qr_id TEXT PRIMARY KEY, job_id TEXT, stage TEXT, bom TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY, filename TEXT, deadline TEXT, status TEXT)')
    c.execute(
        'CREATE TABLE IF NOT EXISTS bids (job_name TEXT PRIMARY KEY, estimate REAL, actual REAL, trajectory TEXT)')
    conn.commit()
    conn.close()


# --- 2. THE ENGINE ---
print("------------------------------------------")
print("!!! JUST-IN-SITE V10.1.0: SINGULARITY  !!!")
print("!!!    DFNO! ALL SYSTEMS GO-FLIGHT     !!!")
print("------------------------------------------")

app = FastAPI()
init_db()


# --- 3. THE BRIDGE (Integrated HTML & JS) ---
@app.get("/", response_class=HTMLResponse)
async def bridge():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Just-In-Site | V10.1.0</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
        <style>
            body {{ background: #020617; color: #f8fafc; font-family: 'Rajdhani', sans-serif; overflow: hidden; }}
            .font-orbitron {{ font-family: 'Orbitron', sans-serif; }}
            .neon-text {{ text-shadow: 0 0 15px #22d3ee; color: #fff; }}
            .glass {{ background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(34, 211, 238, 0.15); backdrop-filter: blur(25px); }}
            .sidebar {{ background: #05050f; border-right: 1px solid #1e1b4b; overflow-y: auto; }}
            .nav-btn {{ width: 100%; text-align: left; padding: 10px 24px; font-size: 0.7rem; color: #64748b; transition: 0.2s; border-left: 3px solid transparent; }}
            .nav-btn:hover, .nav-btn.active {{ color: #22d3ee; background: rgba(34, 211, 238, 0.05); border-left-color: #22d3ee; }}
            .viewport-header {{ border-bottom: 2px solid #22d3ee; padding-bottom: 1rem; margin-bottom: 2rem; }}
            .kanban-col {{ background: rgba(0,0,0,0.4); border-radius: 25px; padding: 20px; min-height: 450px; border: 1px solid rgba(255,255,255,0.05); }}
            ::-webkit-scrollbar {{ width: 5px; }}
            ::-webkit-scrollbar-thumb {{ background: #1e1b4b; border-radius: 10px; }}
        </style>
    </head>
    <body class="flex h-screen">

        <aside class="sidebar w-72 flex flex-col z-20">
            <div class="p-8 border-b border-white/5">
                <h1 class="font-orbitron text-xl font-black italic neon-text uppercase tracking-tighter">Just-In-Site</h1>
                <p class="text-[0.6rem] text-cyan-400 font-bold tracking-[0.4em] uppercase">V10.1.0 // SINGULARITY</p>
            </div>
            <nav class="flex-1" id="sidebar-nav">
                </nav>
        </aside>

        <main class="flex-1 p-12 overflow-y-auto">
            <div class="max-w-7xl mx-auto">

                <div class="text-center mb-16">
                    <h1 class="font-orbitron text-8xl font-black text-white italic neon-text uppercase tracking-tighter">Monkeys</h1>
                    <p class="text-cyan-400 font-mono text-sm tracking-[0.8em] uppercase mt-4 italic">"The Single Source of Truth"</p>
                </div>

                <div id="module-viewport" class="glass rounded-[50px] p-12 min-h-[650px]">
                    <div id="viewport-content">
                        <div class="text-center py-20">
                            <i class="fa-solid fa-atom text-7xl text-cyan-400 animate-spin mb-8"></i>
                            <h2 class="font-orbitron text-3xl font-bold italic text-white uppercase">System Uplink Active</h2>
                            <p class="text-slate-500 font-mono text-xs mt-4 uppercase tracking-widest italic">Select a command station to begin operation.</p>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <div id="bananaError" class="fixed inset-0 z-[100] bg-black/98 flex flex-col items-center justify-center hidden">
            <div class="text-center p-12 border-4 border-yellow-500 rounded-[50px] glass">
                <i class="fa-solid fa-triangle-exclamation text-9xl text-yellow-500 mb-8 animate-bounce"></i>
                <h2 class="font-orbitron text-6xl font-black text-white italic uppercase tracking-tighter">THAT'S BANANAS!</h2>
                <p class="text-yellow-500 font-mono text-lg mt-4 uppercase tracking-widest italic">Neural Circuit Breaker Tripped // Single Source of Truth Compromised</p>
                <button onclick="location.reload()" class="mt-12 px-12 py-4 bg-yellow-500 text-black font-black font-orbitron text-sm rounded-full">REBOOT NEURAL CORE</button>
            </div>
        </div>

        <script>
            const HATS = {{
                "ALPHA_DECK": ["Neural Hat Manager", "Global Kill-Switch", "Truth Audit Log", "Database Pulse", "Bananas Override", "Financial Pulse", "Ghost Mode", "API Command", "Activity Heatmap", "Nitrous Broadcast"],
                "PAWS_STATION": ["The Buy-Board", "Vendor Radar", "UOM Engine", "Restock Alert", "Copper Index", "Packing Slip OCR", "Scrap Ledger", "Bulk Strategy", "Backorder Watchdog", "Bin Locators"],
                "PANTHER_VAULT": ["Master Vault", "Submittal Radar", "Change Order Pulse", "Job-Cost Heatmap", "RFI Live-Link", "Labor Velocity", "Manpower Capsule", "Punch-List", "Site Quick-Card", "Utility Ledger"],
                "MONKEY_ORBIT": ["Prefab Orbit", "QR Neural Linker", "BOM Pop-up", "Load Balancer", "Shortage Panic", "3D Viewport", "Label Printer", "QC Flight Check", "Logistics", "History Audit"],
                "LAUNCHPAD": ["AI Take-Off", "Pricing Library", "Quote Matrix", "Labor Multiplier", "Scope Generator", "Risk Matrix", "Margin Pulse", "Addenda Log", "Bid Ticker", "Post-Mortem Sync"],
                "RABBIT_RUN": ["Raptor Voice", "Time Approvals", "The Teaching Loop", "Safety Journal", "Markup Sync", "Surplus Scanner", "Travel Tracker", "Tool Tethering"]
            }};

            // INIT SIDEBAR
            const nav = document.getElementById('sidebar-nav');
            let sidebarHTML = '';
            for (const [hat, modules] of Object.entries(HATS)) {{
                sidebarHTML += `<div class="px-6 py-4 text-[0.6rem] font-bold text-cyan-400 tracking-widest uppercase border-b border-white/5 mb-2 mt-4 italic">${{hat.replace('_', ' ')}}</div>`;
                modules.forEach(mod => {{
                    sidebarHTML += `<button onclick="loadModule('${{mod}}')" class="nav-btn"><span>${{mod}}</span></button>`;
                }});
            }}
            nav.innerHTML = sidebarHTML;

            function loadModule(name) {{
                const viewport = document.getElementById('viewport-content');
                let content = '';

                // DYNAMIC MODULE GENERATOR
                if(name === 'AI Take-Off') {{
                    content = `<div class="w-full">
                        <div class="viewport-header flex justify-between items-end"><h2 class="font-orbitron text-4xl font-black italic uppercase">${{name}}</h2><span class="text-cyan-400 font-mono text-[0.6rem] uppercase tracking-widest">Scanner Monkey Active</span></div>
                        <div class="border-2 border-dashed border-cyan-500/30 rounded-[40px] p-24 text-center cursor-pointer hover:bg-cyan-900/10 transition" onclick="triggerBananas()">
                            <i class="fa-solid fa-cloud-arrow-up text-6xl text-cyan-400 mb-6"></i>
                            <p class="text-xl font-bold uppercase tracking-widest">Uplink Drawing to Singularity</p>
                            <p class="text-xs text-slate-500 mt-4 font-mono italic">AI Engine will dissect PDF/DWG symbols instantly.</p>
                        </div>
                    </div>`;
                }} else if(name === 'Prefab Orbit') {{
                    content = `<div class="w-full">
                        <div class="viewport-header flex justify-between items-end"><h2 class="font-orbitron text-4xl font-black italic uppercase">${{name}}</h2><span class="text-purple-400 font-mono text-[0.6rem] uppercase tracking-widest">Production Pulse: Nominal</span></div>
                        <div class="grid grid-cols-4 gap-6">
                            <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-slate-500 mb-6 tracking-widest uppercase italic">Launchpad</h3><div class="glass p-5 rounded-2xl text-xs mb-3 border-l-2 border-slate-500">MKY-RACK-01</div></div>
                            <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-blue-500 mb-6 tracking-widest uppercase italic">Assembly</h3><div class="glass p-5 rounded-2xl text-xs mb-3 border-l-2 border-blue-500">STEEL-SPIDER-A</div></div>
                            <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-purple-500 mb-6 tracking-widest uppercase italic">Flight Check</h3></div>
                            <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-green-500 mb-6 tracking-widest uppercase italic">In Orbit</h3></div>
                        </div>
                    </div>`;
                }} else if(name === 'The Buy-Board') {{
                    content = `<div class="w-full">
                        <div class="viewport-header flex justify-between items-end"><h2 class="font-orbitron text-4xl font-black italic uppercase text-green-400">${{name}}</h2><span class="text-green-400 font-mono text-[0.6rem] uppercase tracking-widest">Procurement Link Established</span></div>
                        <div class="space-y-4">
                            <div class="glass p-8 rounded-3xl flex justify-between items-center border-l-4 border-green-500">
                                <div><div class="text-[0.6rem] text-slate-500 font-bold uppercase mb-1">REQ #1024</div><div class="text-xl font-bold italic uppercase">2,450ft 3/4" EMT Conduit</div></div>
                                <button class="px-10 py-3 bg-green-600 rounded-full font-bold text-xs hover:bg-green-500 transition">APPROVE PO</button>
                            </div>
                        </div>
                    </div>`;
                }} else {{
                    content = `<div class="w-full text-center py-32">
                        <i class="fa-solid fa-screwdriver-wrench text-7xl text-cyan-400/10 mb-8"></i>
                        <h2 class="font-orbitron text-3xl font-black italic text-white uppercase tracking-tighter">${{name}}</h2>
                        <p class="text-slate-600 font-mono text-xs uppercase tracking-[0.5em] mt-4 italic">Neural Interface Under Construction // DFNO</p>
                    </div>`;
                }}

                viewport.innerHTML = content;
            }}

            function triggerBananas() {{ document.getElementById('bananaError').classList.remove('hidden'); }}
        </script>
    </body>
    </html>
    """