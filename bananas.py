import streamlit as st
import traceback
from datetime import datetime
from monkey_heart import MonkeyHeart


class Bananas:
    """
    SURVEILLANCE: High-fidelity error dissection and collision reporting.
    This module captures system-wide exceptions and translates them into
    actionable industrial data for the operator.
    """

    @staticmethod
    def report_collision(error, context="KERNEL_CORE"):
        """
        Dissects a Python exception and renders it within the Oxide UI.
        Logs the event to persistent storage on the Railway Volume.
        """
        # 1. Capture the Traceback for internal logging
        error_trace = traceback.format_exc()
        timestamp = datetime.now().strftime("%H:%M:%S")

        # 2. Log to Persistent Volume (Heart Path)
        MonkeyHeart.log_system_event("COLLISION", f"Node: {context} | Error: {str(error)}")

        # 3. Industrial UI Feedback
        st.markdown(f"""
            <div style="
                border-left: 4px solid {MonkeyHeart.THEME['CRITICAL']};
                background-color: rgba(255, 0, 85, 0.05);
                padding: 20px;
                margin: 15px 0;
            ">
                <h3 style="color: {MonkeyHeart.THEME['CRITICAL']}; margin: 0; padding: 0; border: none;">
                    SYSTEM COLLISION // {context}
                </h3>
                <p style="color: #aaaaaa; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; margin-top: 10px;">
                    TIMESTAMP: {timestamp} | STATUS: NON-FATAL_HALT
                </p>
                <div style="
                    background-color: rgba(0,0,0,0.3);
                    padding: 10px;
                    border: 1px solid #333;
                    margin-top: 10px;
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.8rem;
                    color: #ff4b4b;
                ">
                    {str(error)}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 4. Developer Mode Toggle (Optional detail for debugging)
        with st.expander("VIEW STACK DISSECTION"):
            st.code(error_trace, language="python")

    @staticmethod
    def notify(status_type, message):
        """
        Non-error notifications designed for the industrial interface.
        """
        color = MonkeyHeart.THEME['NEON_CYAN'] if status_type == "INFO" else MonkeyHeart.THEME['OXIDE_PURPLE']

        st.markdown(f"""
            <div style="
                border-bottom: 1px solid {color};
                padding: 10px 0;
                margin-bottom: 10px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.9rem;
            ">
                <span style="color: {color}; font-weight: bold;">[{status_type}]</span> {message}
            </div>
        """, unsafe_allow_html=True)