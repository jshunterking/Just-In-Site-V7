import streamlit as st
from datetime import datetime
from monkey_heart import MonkeyHeart
from monkey_brain import MonkeyBrain
from bananas import Bananas


class MonkeyEars:
    """
    AWARENESS: The auditory and alert layer of the system.
    OXIDE PROTOCOL: Monitoring threshold breaches and triggering notifications.
    Target: Real-time contractor alert systems for 50,000-line stability.
    """

    @staticmethod
    def listen_for_thresholds(project_id):
        """
        OXIDE: Scans the project data for "Danger Zones" (Over-budget, late deliveries).
        """
        try:
            # Query the Belly/Brain for margin health
            query = "SELECT gross_margin_target, status FROM core_projects WHERE project_id = ?"
            df = MonkeyBrain.query_oxide(query, (project_id,))

            if not df.empty:
                margin = df['gross_margin_target'].iloc[0]
                # Trigger "Auditory" alert if margin is critically low
                if margin < 10.0:
                    MonkeyEars.trigger_alert("CRITICAL_MARGIN", f"Project {project_id} below 10% threshold.")
        except Exception as e:
            Bananas.report_collision(e, "EARS_THRESHOLD_FAILURE")

    @staticmethod
    def trigger_alert(alert_level, message):
        """
        Visual and Auditory notification injection into the 22nd Century UI.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = MonkeyHeart.THEME['CRITICAL'] if "CRITICAL" in alert_level else MonkeyHeart.THEME['SIGNAL_CYAN']

        # In a 50k line app, this would also trigger SMS via Twilio or Email via SendGrid.
        st.toast(f"[{alert_level}] {message}")

        st.markdown(f"""
            <div style="
                border-left: 2px solid {color};
                background: rgba(0, 0, 0, 0.4);
                padding: 10px;
                margin-top: 5px;
                border-radius: 0 5px 5px 0;
            ">
                <span style="color: {color}; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: bold;">
                    {timestamp} // {alert_level}
                </span><br>
                <span style="color: #ffffff; font-size: 0.9rem;">{message}</span>
            </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def pulse_check():
        """
        Listens for the 'Heartbeat' of the Railway Volume.
        """
        if not os.path.exists(MonkeyHeart.VOLUME_ROOT):
            MonkeyEars.trigger_alert("STORAGE_DISCONNECT", "Persistent Volume Not Found. Data is Ephemeral!")