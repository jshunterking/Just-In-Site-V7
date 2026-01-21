import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CORE SYSTEMS ---
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from owl_singularity import OwlSingularity
from oxide_roles import OxideRoles

# --- THE RABBITS (WORKERS) ---
from rabbit_billing import RabbitBilling
from rabbit_manpower import RabbitManpower
from rabbit_daily_reports import RabbitDailyReports
from rabbit_prefab import RabbitPrefab
from rabbit_plans import RabbitPlans  # <--- CORRECTED TAXONOMY

# --- THE RAPTORS (HUNTERS) ---
from raptor_leads import RaptorLeads
from raptor_voice import RaptorVoice
from raptor_admin import RaptorAdmin
from raptor_outlook import RaptorOutlook

# --- THE OWLS (ADVISORS) ---
from owl_safety import OwlSafety

# ==============================================================================
# 1. ATMOSPHERIC INITIALIZATION & BOOT SEQUENCE
# ==============================================================================
st.set_page_config(
    page_title="JUST-IN-SITE | AIR",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FORCE SYSTEM BOOT (Safe Mode Protection)
# This ensures tables exist before the UI tries to query them.
try:
    MonkeyBrain.initialize_database()
    OxideRoles.initialize_auth_table()
    RabbitDailyReports.initialize_daily_tables()
    RabbitPrefab.initialize_prefab_tables()
    RaptorLeads.initialize_lead_tables()
except Exception as e:
    st.error(f"SYSTEM BOOT SEQUENCE INTERRUPTED: {e}")

# ==============================================================================
# 2. THE NEON SINGULARITY CSS ENGINE
# ==============================================================================
st.markdown("""
    <style>
    /* IMPORT FUTURISTIC FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

    /* GLOBAL RESET - DEEP VOID */
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* HEADERS - ORBITRON GLOW */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #fff;
        text-shadow: 0 0 10px #bf00ff, 0 0 20px #bf00ff; /* NEON PURPLE */
    }

    /* SIDEBAR - COCKPIT PANEL */
    [data-testid="stSidebar"] {
        background-color: #0b0c10;
        border-right: 2px solid #bf00ff;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.1rem;
    }

    /* METRIC CARDS - HUD STYLE */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #111, #1a1a2e);
        border: 1px solid #333;
        border-left: 5px solid #bf00ff;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(191, 0, 255, 0.2);
        border-radius: 0px;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #00ff9d; /* HUD GREEN */
        text-shadow: 0 0 5px #00ff9d;
    }
    div[data-testid="stMetricLabel"] {
        color: #a0a0a0;
        font-weight: bold;
        text-transform: uppercase;
    }

    /* BUTTONS - THE STRIKE */
    .stButton>button {
        background: transparent;
        border: 2px solid #bf00ff;
        color: #bf00ff;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        border-radius: 0px;
        transition: 0.3s;
        text-transform: uppercase;
        width: 100%;
    }
    .stButton>button:hover {
        background: #bf00ff;
        color: #fff;
        box-shadow: 0 0 20px #bf00ff;
    }

    /* INPUTS & SELECTS */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #111;
        color: #fff;
        border: 1px solid #333;
        font-family: 'Rajdhani', sans-serif;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #111;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #fff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #bf00ff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. THE SECURITY GATE (LOGIN)
# ==============================================================================

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
    st.session_state['user_name'] = ""

if st.session_state['user_role'] is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>JUST-IN-SITE</h1>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align: center; color: #bf00ff; font-family: Orbitron;'>OXIDE SINGULARITY OS // V.2026.1</div>",
            unsafe_allow_html=True)
        st.divider()

        user_input = st.text_input("OPERATOR ID")
        pass_input = st.text_input("ACCESS KEY", type="password")

        if st.button("INITIALIZE LINK"):
            auth = OxideRoles.login(user_input, pass_input)
            if auth["authenticated"]:
                st.session_state['user_role'] = auth['role_code']
                st.session_state['user_name'] = auth['name']
                st.rerun()
            else:
                st.error("ACCESS DENIED: BIOMETRIC MISMATCH.")

    st.stop()  # HALT UNTIL LOGIN

# ==============================================================================
# 4. AIR COMMAND (SIDEBAR)
# ==============================================================================
user_role = st.session_state['user_role']
user_name = st.session_state['user_name']
allowed_theaters = OxideRoles.get_accessible_theaters(user_role)

with st.sidebar:
    st.markdown("## 🦅 AIR COMMAND")
    st.markdown(f"**OP:** <span style='color:#00ff9d'>{user_name}</span>", unsafe_allow_html=True)
    st.markdown(f"**RANK:** `{user_role}`")
    st.write("---")

    # DYNAMIC NAVIGATION
    theater = st.radio("ACTIVE THEATERS", allowed_theaters)

    st.write("---")
    if st.button("TERMINATE UPLINK"):
        st.session_state['user_role'] = None
        st.rerun()

    st.markdown(
        f"<div style='text-align: center; color: #555; font-size: 0.8em; margin-top: 20px;'>SYSTEM CLOCK<br>{datetime.now().strftime('%H:%M:%S')}</div>",
        unsafe_allow_html=True)

# ==============================================================================
# 5. THEATER 1: ORACLE (EXECUTIVE)
# ==============================================================================
if theater == "Oracle (Executive)":
    st.title("STRATEGIC PULSE")

    pulse = OwlSingularity.calculate_enterprise_pulse()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SINGULARITY SCORE", f"{pulse['singularity_score']}/100", delta="STABLE")
    c2.metric("MARKET VECTOR", pulse['outlook'])
    c3.metric("CRITICAL ACTION", pulse['critical_action'])
    c4.metric("SYSTEM UPTIME", "99.9%", delta="OPTIMAL")

    st.divider()

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.subheader("REVENUE TRAJECTORY (OHIO SECTOR)")
        # In Production, pull this from MonkeyBrain.query_oxide("SELECT...")
        chart_data = pd.DataFrame({
            'Timeline': ['Wk1', 'Wk2', 'Wk3', 'Wk4', 'Wk5'],
            'Actuals': [45000, 52000, 49000, 61000, 65000],
            'Projected': [46000, 48000, 50000, 52000, 54000]
        })
        st.line_chart(chart_data, x="Timeline", color=["#bf00ff", "#00ff9d"])

    with col_side:
        st.subheader("LIVE ALERTS")
        st.info("⚠️ Material Delay: 200A Panels (Vendor X)")
        st.success("✅ Bid Won: Cleveland Clinic Exp.")
        st.warning("⚡ Weather Alert: High Winds - Secure Cranes")

# ==============================================================================
# 6. THEATER 2: VAULT (FINANCIAL)
# ==============================================================================
elif theater == "Vault (Financial)":
    st.title("THE VAULT")

    if not OxideRoles.can_view_money(user_role):
        st.error("SECURITY ALERT: CLEARANCE INSUFFICIENT.")
        st.stop()

    tab1, tab2 = st.tabs(["BILLING ENGINE", "CASH FLOW"])

    with tab1:
        st.subheader("GENERATE PAY APP (G702)")
        c1, c2 = st.columns(2)
        with c1:
            pid = st.text_input("PROJECT ID")
            val = st.number_input("PERIOD VALUE ($)", min_value=0.0)
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("EXECUTE BILLING"):
                net = RabbitBilling.create_pay_app(pid, val, 0)
                st.success(f"PAY APP GENERATED. NET: ${net:,.2f}")

# ==============================================================================
# 7. THEATER 3: FIELD (PRODUCTION)
# ==============================================================================
elif theater == "Field (Production)":
    st.title("FIELD COMMAND")

    tab_voice, tab_prefab, tab_plans, tab_daily = st.tabs(
        ["🎙️ VOICE LOG", "🏭 PREFAB ORDER", "📜 BLUEPRINTS", "📋 DAILY REPORT"])

    # --- TAB: VOICE ---
    with tab_voice:
        st.subheader("VOICE-TO-DATA UPLINK")
        audio = st.file_uploader("UPLOAD FIELD LOG (.wav)", type=["wav"])
        if audio:
            with st.spinner("RAPTOR DECRYPTING AUDIO..."):
                txt = RaptorVoice.process_field_memo(audio, "PROJ-FIELD", user_name)
                st.success("DATA INJECTED.")
                st.code(txt, language="text")

    # --- TAB: PREFAB ---
    with tab_prefab:
        st.subheader("DIGITAL FACTORY ORDER")
        with st.form("prefab_field_form"):
            c1, c2 = st.columns(2)
            p_id = c1.text_input("Project ID (e.g. PROJ-2026-01)")
            k_type = c2.selectbox("Kit Type", ["Room-in-a-Box", "Panel Build", "Lighting Whip", "Conduit Rack"])
            desc = c1.text_input("Details (Room #s)")
            qty = c2.number_input("Quantity", min_value=1)
            prio = st.select_slider("Priority", ["STANDARD", "RUSH", "CRITICAL"])
            due = st.date_input("Need By Date")

            if st.form_submit_button("TRANSMIT ORDER"):
                RabbitPrefab.submit_order(p_id, k_type, desc, qty, prio, user_name, due)
                st.success("ORDER TRANSMITTED TO SHOP QUEUE.")

    # --- TAB: PLANS ---
    with tab_plans:
        st.subheader("PLAN TABLE")
        # Ensure directory exists
        if not os.path.exists("project_plans"):
            os.makedirs("project_plans")

        proj_list = RaptorAdmin.get_all_projects()['project_id'].tolist()
        sel_proj = st.selectbox("Select Project Plans",
                                proj_list) if not RaptorAdmin.get_all_projects().empty else "No Projects"

        # --- FIXED: USING RABBIT PLANS ---
        drawings = RabbitPlans.list_project_drawings(sel_proj)

        if drawings:
            sel_dwg = st.selectbox("Select Drawing", drawings)
            st.info(f"Accessing {sel_dwg}... (PDF Viewer Active)")
            # Future: st.iframe or embedded PDF viewer logic here
        else:
            st.warning(f"No digital plans found for {sel_proj}.")

    # --- TAB: DAILY ---
    with tab_daily:
        st.subheader("END OF DAY REPORT")
        with st.form("daily_rep_form"):
            dp_id = st.text_input("Project ID")
            weath = st.text_input("Weather Conditions")
            notes = st.text_area("Site Notes / Delays")

            if st.form_submit_button("FILE REPORT"):
                RabbitDailyReports.log_report(dp_id, weath, notes)
                st.success("REPORT FILED IN SINGLE SOURCE OF TRUTH.")

# ==============================================================================
# 8. THEATER 4: RADAR (SCOUTING)
# ==============================================================================
elif theater == "Radar (Scouting)":
    st.title("MARKET RADAR")

    if st.button("INITIATE RAPTOR SWEEP"):
        with st.status("SCANNING OHIO BID NETWORKS...", expanded=True):
            st.write("Targeting Commercial Electrical...")
            RaptorLeads.harvest_public_rfps("Electrical")
            st.write("Filtering Junk...")
        st.success("TARGETS ACQUIRED.")

    leads = MonkeyBrain.query_oxide("SELECT * FROM bid_leads ORDER BY timestamp_found DESC")
    st.dataframe(leads, use_container_width=True)

# ==============================================================================
# 9. THEATER 5: COMM CENTER (OUTLOOK)
# ==============================================================================
elif theater == "Comm Center":
    st.title("COMMUNICATIONS LINK")
    st.subheader("OUTLOOK INTEGRATION")

    target_proj = st.text_input("Filter by Project ID", value="PROJ-2026-01")

    if st.button("SYNC INBOX"):
        with st.spinner("Connect to Exchange Server..."):
            emails = RaptorOutlook.get_project_emails(target_proj)
            if not emails.empty and "Error" not in emails.columns:
                st.dataframe(emails, use_container_width=True)
            elif "Error" in emails.columns:
                st.error(emails['Error'].iloc[0])
            else:
                st.info("No relevant communications found.")

# ==============================================================================
# 10. THEATER 6: SETTINGS (ADMIN)
# ==============================================================================
elif theater == "Settings (System)":
    st.title("SYSTEM CORE")

    if user_role != "OVERLORD":
        st.error("ACCESS DENIED. BIOMETRICS REJECTED.")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["RECRUITMENT (USERS)", "OPERATIONS (PROJECTS)", "SYSTEM LOGS"])

    # --- TAB 1: ADD USERS ---
    with tab1:
        st.subheader("RECRUIT NEW OPERATOR")
        with st.form("new_user_form"):
            c1, c2 = st.columns(2)
            new_user = c1.text_input("Username (Login ID)")
            new_pass = c2.text_input("Password", type="password")
            new_name = c1.text_input("Full Name")
            new_email = c2.text_input("Email")
            new_role = st.selectbox("Rank / Clearance",
                                    ["INFANTRY", "LOGISTICS", "FIELD_CMDR", "SEER", "COMMAND", "EXECUTIVE", "OVERLORD"])

            if st.form_submit_button("AUTHORIZE RECRUITMENT"):
                if RaptorAdmin.create_new_user(new_user, new_pass, new_role, new_name, new_email):
                    st.success(f"OPERATOR {new_user} ACTIVE.")
                else:
                    st.error("RECRUITMENT FAILED.")

        st.divider()
        st.subheader("ACTIVE ROSTER")
        st.dataframe(RaptorAdmin.get_all_users(), use_container_width=True)

    # --- TAB 2: ADD PROJECTS ---
    with tab2:
        st.subheader("LAUNCH NEW OPERATION")
        with st.form("new_proj_form"):
            c1, c2 = st.columns(2)
            p_id = c1.text_input("Project ID (e.g. PROJ-2026-XX)")
            p_name = c2.text_input("Project Name")
            p_client = c1.text_input("Client")
            p_margin = c2.number_input("Target Margin (0.00 - 1.00)", min_value=0.0, max_value=1.0, value=0.25)

            if st.form_submit_button("INITIATE PROJECT"):
                if RaptorAdmin.create_new_project(p_id, p_name, p_client, p_margin):
                    st.success(f"OPERATION {p_name} LAUNCHED.")
                else:
                    st.error("LAUNCH FAILED.")

        st.divider()
        st.subheader("ACTIVE THEATERS")
        st.dataframe(RaptorAdmin.get_all_projects(), use_container_width=True)

    # --- TAB 3: LOGS ---
    with tab3:
        st.subheader("HEARTBEAT LOGS")
        try:
            with open("system_logs/oxide_kernel.log", "r") as f:
                logs = f.readlines()
                for line in logs[-20:]:
                    st.text(line.strip())
        except:
            st.warning("NO LOGS FOUND.")