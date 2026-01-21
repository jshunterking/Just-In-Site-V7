import streamlit as st
import time
from monkey_heart import MonkeyHeart
from monkey_brain import MonkeyBrain
from monkey_eyes import MonkeyEyes
from bananas import Bananas
# monkeys.py (Top of file)

# These tell the Dashboard where to find the "Monkeys"
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart

# These tell the Dashboard where to find the "Rabbits"
from rabbit_billing import RabbitBilling
from rabbit_manpower import RabbitManpower

# These tell the Dashboard where to find the "Owls"
from owl_analytics import OwlAnalytics
from owl_safety import OwlSafety

def initialize_system():
    """
    OXIDE: Synchronization of all core modules before UI deployment.
    """
    try:
        MonkeyHeart.initialize_oxide_environment()
        MonkeyBrain.initialize_singularity()
    except Exception as e:
        Bananas.report_collision(e, "SYSTEM_BOOT_FAILURE")


def boot_system():
    # Start the Brain first!
    MonkeyBrain.initialize_database()

    # Now tell the Brain to build the Billing table
    RabbitBilling.initialize_billing_tables()

    # Now tell the Brain to build the Manpower table
    RabbitManpower.initialize_labor_tables()

    print("Just-In-Site: All systems wired and talking.")

def main():
    # 1. APPLY 22ND CENTURY PHYSICS
    MonkeyHeart.apply_industrial_css()
    initialize_system()

    # 2. AUTHENTICATION GATEWAY (OXIDE DISSECTION)
    if not st.session_state.get('oxide_auth', False):
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div style='text-align: center; padding-top: 50px;'>
                    <h1 style='letter-spacing: 10px;'>JUST-IN-SITE</h1>
                    <p style='color: #6E00FF; letter-spacing: 5px; font-weight: bold;'>MONKEYS V2.0 // OXIDE</p>
                </div>
            """, unsafe_allow_html=True)

            with st.form("oxide_gate"):
                st.markdown("### OPERATOR IDENTITY")
                u_input = st.text_input("HANDLE")
                p_input = st.text_input("SECURITY KEY", type="password")

                if st.form_submit_button("ENGAGE KERNEL"):
                    if u_input == "Admin" and p_input == "Nitrous2026":
                        st.session_state.oxide_auth = True
                        st.session_state.operator = u_input
                        Bananas.notify("SUCCESS", "Neural Link Established.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED: Credentials Rejected by Kernel.")
        return

    # 3. INDUSTRIAL COMMAND CENTER (THE COCKPIT)
    st.sidebar.markdown(f"## COMMAND // {st.session_state.operator}")

    trade_focus = st.sidebar.selectbox("CORE INDUSTRY SECTOR", [
        "ELECTRICAL CONTRACTOR",
        "PLUMBING & MECHANICAL",
        "HVAC / SHEET METAL",
        "GENERAL CONTRACTING",
        "INDUSTRIAL PRE-FAB"
    ])

    # Persistent Storage Status
    st.sidebar.divider()
    st.sidebar.caption(f"DB PATH: {MonkeyHeart.DB_PATH}")
    st.sidebar.caption(f"VAULT: {MonkeyHeart.VAULT_PATH}")

    # 4. OPERATIONAL DASHBOARD (THE SELL)
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(f"## {trade_focus} // PULSE")
        st.info(f"System Operational. Monitoring {trade_focus} logic.")

        # Action Center
        tab1, tab2, tab3 = st.tabs(["PROJECTS", "BLUEPRINT SCAN", "LOGISTICS"])

        with tab1:
            st.markdown("### ACTIVE PROJECTS")
            projects = MonkeyBrain.query_oxide("SELECT * FROM core_projects")
            if projects.empty:
                st.write("NO ACTIVE PROJECTS FOUND IN SINGULARITY.")
                if st.button("+ INITIALIZE NEW PROJECT"):
                    # This will be expanded in Block 06
                    pass
            else:
                st.dataframe(projects, use_container_width=True)

        with tab2:
            st.markdown("### VISION UPLOAD")
            uploaded_file = st.file_uploader("DROP BLUEPRINT PDF FOR DISSECTION", type=["pdf"])
            if uploaded_file:
                path = MonkeyEyes.archive_blueprint(uploaded_file, "TEMP_ID")
                st.success(f"Archived to Vault: {path}")
                if st.button("RUN OXIDE SCAN"):
                    with st.spinner("DISSECTING PIXELS..."):
                        img = MonkeyEyes.rasterize_blueprint(path)
                        st.image(img, caption="Rasterized Surface", use_container_width=True)
                        results = MonkeyEyes.generate_oxide_takeoff(img, trade_focus)
                        st.json(results)

    with col2:
        st.markdown("### KPI MATRIX")
        st.metric("TAKEOFF ACCURACY", "99.8%", "+0.2%")
        st.metric("DB LATENCY", "12ms", "-2ms")
        st.metric("MARGIN DELTA", "4.2%", "+1.1%")

    with col3:
        st.markdown("### SYSTEM LOGS")
        if os.path.exists(os.path.join(MonkeyHeart.LOG_PATH, "oxide_kernel.log")):
            with open(os.path.join(MonkeyHeart.LOG_PATH, "oxide_kernel.log"), "r") as f:
                logs = f.readlines()
                st.code("".join(logs[-10:]), language="text")


if __name__ == "__main__":
    main()