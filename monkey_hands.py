import streamlit as st
from monkey_heart import MonkeyHeart
from monkey_brain import MonkeyBrain
from bananas import Bananas


class MonkeyHands:
    """
    DEXTERITY: The manual override and fine-tuning layer.
    OXIDE PROTOCOL: High-fidelity input components for precision adjustments.
    Target: Eliminating friction between the Contractor and the Data.
    """

    @staticmethod
    def adjust_project_vitals(project_id):
        """
        OXIDE: Provides the tactile controls to "manually" tune project margins
         and status without entering the database directly.
        """
        try:
            st.markdown("### MANUAL VITALS ADJUSTMENT")

            # 1. Reach into the Belly for current data
            query = "SELECT project_name, gross_margin_target, status FROM core_projects WHERE project_id = ?"
            df = MonkeyBrain.query_oxide(query, (project_id,))

            if not df.empty:
                current_data = df.iloc[0]

                # 2. Precision Sliders (The Hands)
                new_margin = st.slider(
                    "ADJUST TARGET MARGIN (%)",
                    0.0, 100.0,
                    float(current_data['gross_margin_target']),
                    help="Manual override for project profitability thresholds."
                )

                new_status = st.selectbox(
                    "TRANSITION PROJECT STATUS",
                    ["ACTIVE", "PENDING", "COMPLETED", "ARCHIVED"],
                    index=["ACTIVE", "PENDING", "COMPLETED", "ARCHIVED"].index(current_data['status'])
                )

                # 3. Commit the change
                if st.button("EXECUTE ADJUSTMENT"):
                    cmd = "UPDATE core_projects SET gross_margin_target = ?, status = ? WHERE project_id = ?"
                    MonkeyBrain.execute_oxide(cmd, (new_margin, new_status, project_id))
                    st.success(f"Vitals for {project_id} updated successfully.")

        except Exception as e:
            Bananas.report_collision(e, "HANDS_MANIPULATION_FAILURE")

    @staticmethod
    def material_fine_tune(item_id):
        """
        Allows the contractor to 'manually' grip and change material pricing
        on the fly during an estimate.
        """
        st.markdown(f"#### MANUAL OVERRIDE // ITEM: {item_id}")
        # Logic for individual material cost manipulation
        pass

    @staticmethod
    def capture_signature():
        """
        Oxide expansion for field sign-offs and delivery confirmations.
        """
        # Placeholder for future 22nd-century touchscreen signature capture
        pass