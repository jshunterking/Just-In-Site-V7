"""
JUST-IN-SITE V10.01.4 | THE ENGINE IGNITION
Functional Modules: AI Take-Off, Prefab Orbit, Manpower, and Bid Trajectory.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3

# --- 1. THE BRAIN ---
def get_db_data():
    # Simulation of database retrieval for the Truth
    return {
        "assemblies": [
            {"id": "MKY-001", "name": "Mercy Hospital Rack", "stage": "Launchpad"},
            {"id": "MKY-002", "name": "Steel Mill Spider", "stage": "Assembly"},
        ],
        "crew": [
            {"name": "Justin", "job": "Admin-01", "burn": "Nominal"},
            {"name": "Apprentice-A", "job": "Mercy-734", "burn": "Elevated"},
        ]
    }

# --- 2. THE ENGINE ---
print("------------------------------------------")
print("!!! JUST-IN-SITE V10.01.4: IGNITION    !!!")
print("!!!    DFNO! ENGINES ARE HOT           !!!")
print("------------------------------------------")

app = FastAPI()

# MASTER HAT MATRIX
HATS = {
    "ADMIN": ["Neural Hat Manager", "Global Kill-Switch", "Truth Audit Log", "Database Pulse", "Bananas Override", "Financial Pulse", "Ghost Mode", "API Command", "Activity Heatmap", "Nitrous Broadcast"],
    "PURCHASING": ["The Buy-Board", "Vendor Radar", "UOM Engine", "Restock Alert", "Copper Index", "Packing Slip OCR", "Scrap Ledger", "Bulk Strategy", "Backorder Watchdog", "Bin Locators"],
    "PROJECT_MANAGER": ["Master Vault", "Submittal Radar", "Change Order Pulse", "Job-Cost Heatmap", "RFI Live-Link", "Labor Velocity", "Manpower Capsule", "Punch-List", "Site Quick-Card", "Utility Ledger"],
    "PREFAB_MANAGER": ["Prefab Orbit", "QR Neural Linker", "BOM Pop-up", "Load Balancer", "Shortage Panic", "3D Viewport", "Label Printer", "QC Flight Check", "Logistics", "History Audit"],
    "ESTIMATOR": ["AI Take-Off", "Pricing Library", "Quote Matrix", "Labor Multiplier", "Scope Generator", "Risk Matrix", "Margin Pulse", "Addenda Log", "Bid Ticker", "Post-Mortem Sync"],
    "FOREMAN": ["Raptor Voice", "Time Approvals", "The Teaching Loop", "Safety Journal", "Markup Sync", "Surplus Scanner", "Travel Tracker", "Tool Tethering"]
}

@app.get("/", response_class=HTMLResponse)
async def bridge():
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
        <title>Just-In-Site | V10.01.4</title>
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
            .kanban-col {{ background: rgba(0,0,0,0.3); border-radius: 20px; padding: 15px; min-height: 400px; border: 1px solid rgba(255,255,255,0.05); }}
            .upload-zone {{ border: 2px dashed rgba(34, 211, 238, 0.3); }}
            .upload-zone:hover {{ border-color: #22d3ee; background: rgba(34, 211, 238, 0.05); }}
        </style>
    </head>
    <body class="flex h-screen">
        <aside class="sidebar w-72 flex flex-col z-20">{sidebar_html}</aside>

        <main class="flex-1 p-12 overflow-y-auto">
            <div class="max-w-7xl mx-auto">
                <div class="text-center mb-16">
                    <h1 class="font-orbitron text-8xl font-black text-white italic neon-text uppercase tracking-tighter">Just-In-Site</h1>
                    <p class="text-cyan-400 font-mono text-sm tracking-[0.7em] uppercase mt-4 italic">"The Single Source of Truth"</p>
                </div>

                <div id="module-viewport" class="glass rounded-[40px] p-12 min-h-[600px]">
                    <div id="viewport-content" class="flex items-center justify-center h-full">
                        <div class="text-center">
                            <i class="fa-solid fa-rocket text-6xl text-slate-700 mb-6"></i>
                            <h2 class="font-orbitron text-3xl font-bold italic text-slate-500 uppercase">Awaiting Command</h2>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <script>
            function loadModule(name) {{
                const viewport = document.getElementById('viewport-content');
                let content = '';

                switch(name) {{
                    case 'AI Take-Off':
                        content = `
                            <div class="w-full">
                                <h2 class="font-orbitron text-4xl font-black italic uppercase mb-8">Scanner Monkey: AI Take-Off</h2>
                                <div class="upload-zone rounded-[30px] p-20 text-center cursor-pointer transition">
                                    <i class="fa-solid fa-cloud-arrow-up text-5xl text-cyan-400 mb-4"></i>
                                    <p class="text-lg font-bold">Drop Drawing PDF here or Click to Browse</p>
                                    <p class="text-xs text-slate-500 mt-2 font-mono uppercase tracking-widest">Supports: .pdf, .dwg, .rvt</p>
                                </div>
                                <div class="mt-10 grid grid-cols-3 gap-6">
                                    <div class="glass p-6 rounded-2xl text-center"><div class="text-xs text-slate-500 mb-1">Status</div><div class="font-bold text-cyan-400">IDLE</div></div>
                                    <div class="glass p-6 rounded-2xl text-center"><div class="text-xs text-slate-500 mb-1">Last Scan</div><div class="font-bold">None</div></div>
                                    <div class="glass p-6 rounded-2xl text-center"><div class="text-xs text-slate-500 mb-1">Confidence</div><div class="font-bold">0%</div></div>
                                </div>
                            </div>`;
                        break;
                    case 'Prefab Orbit':
                        content = `
                            <div class="w-full">
                                <h2 class="font-orbitron text-4xl font-black italic uppercase mb-8">Prefab Production Orbit</h2>
                                <div class="grid grid-cols-4 gap-6">
                                    <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-slate-500 mb-4 tracking-widest uppercase">Launchpad</h3><div class="glass p-4 rounded-xl text-xs border-l-2 border-slate-500">MKY-RACK-01</div></div>
                                    <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-blue-500 mb-4 tracking-widest uppercase">Assembly</h3><div class="glass p-4 rounded-xl text-xs border-l-2 border-blue-500">STEEL-SPIDER-A</div></div>
                                    <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-purple-500 mb-4 tracking-widest uppercase">Flight Check</h3></div>
                                    <div class="kanban-col"><h3 class="text-[0.6rem] font-bold text-green-500 mb-4 tracking-widest uppercase">In Orbit</h3></div>
                                </div>
                            </div>`;
                        break;
                    case 'Manpower Capsule':
                        content = `
                            <div class="w-full">
                                <h2 class="font-orbitron text-4xl font-black italic uppercase mb-8">Manpower Capsule</h2>
                                <table class="w-full text-left font-mono text-sm">
                                    <thead class="text-cyan-400 border-b border-white/10 uppercase tracking-widest">
                                        <tr><th class="pb-4">Operator</th><th class="pb-4">Active Job</th><th class="pb-4">Burn Rate</th><th class="pb-4">Status</th></tr>
                                    </thead>
                                    <tbody class="text-slate-300">
                                        <tr class="border-b border-white/5"><td class="py-4">Justin</td><td class="py-4">ADMIN-CORE</td><td class="py-4">0.00h</td><td class="py-4 text-green-500">ACTIVE</td></tr>
                                        <tr class="border-b border-white/5"><td class="py-4">Foreman-Smith</td><td class="py-4">MERCY-734</td><td class="py-4">7.50h</td><td class="py-4 text-green-500">ACTIVE</td></tr>
                                    </tbody>
                                </table>
                            </div>`;
                        break;
                    default:
                        content = `
                            <div class="text-center py-20">
                                <i class="fa-solid fa-screwdriver-wrench text-6xl text-cyan-400/20 mb-6"></i>
                                <h2 class="font-orbitron text-2xl font-black italic text-white mb-2 uppercase tracking-tighter">${{name}}</h2>
                                <p class="text-slate-500 font-mono text-xs uppercase tracking-widest">Awaiting Functional Wiring // DFNO</p>
                            </div>`;
                }}
                viewport.innerHTML = content;
            }}
        </script>
    </body>
    </html>
    """