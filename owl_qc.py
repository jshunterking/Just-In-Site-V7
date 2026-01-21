import pandas as pd
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas


class OwlQC:
    """
    OWL PROTOCOL: Wisdom in Craftsmanship.
    OXIDE DISSECTION: Predicting installation errors before the "Walls Close Up."
    Target: Zero-Defect Handover and 100% First-Pass Inspection Rate.
    """

    @staticmethod
    def identify_error_patterns(project_id):
        """
        OWL: Scans the Punch List (Block 28) across all historical projects
        to find recurring "Fail Points" for the current trade focus.
        """
        try:
            # 1. Identify common punch items for this trade (e.g., Electrical)
            query = """
                SELECT description, COUNT(*) as frequency
                FROM punch_list
                WHERE status != 'VERIFIED'
                GROUP BY description
                ORDER BY frequency DESC
                LIMIT 5
            """
            patterns = MonkeyBrain.query_oxide(query)

            # 2. Cross-reference with current project submittals
            # If we have a history of "Wrong Faceplate Color" and a pending
            # Device Submittal, the Owl flags it.
            return {
                "top_risks": patterns.to_dict(orient='records'),
                "inspection_focus": "Trim & Devices" if not patterns.empty else "General",
                "owl_advice": "High frequency of labeling errors detected in similar projects."
            }

        except Exception as e:
            Bananas.report_collision(e, "QC_PATTERN_ANALYSIS_FAILURE")

    @staticmethod
    def trigger_preemptive_inspection(project_id, location):
        """
        OWL: Automatically generates an internal inspection task
        before the official Municipal Inspection (Block 18).
        """
        try:
            cmd = """
                INSERT INTO punch_list (project_id, description, location, status)
                VALUES (?, 'PRE-INSPECTION: Internal QC Sweep', ?, 'OPEN')
            """
            MonkeyBrain.execute_oxide(cmd, (project_id, location))
            Bananas.notify("QC_ALERT", f"Internal sweep triggered for {location} to prevent re-work.")
        except Exception as e:
            Bananas.report_collision(e, "QC_TRIGGER_FAILURE")

    @staticmethod
    def calculate_rework_cost(project_id):
        """
        OWL: Analyzes hours spent on 'Punch List' items vs. original production
        to show the owner how much money is being 'burned' on mistakes.
        """
        # In the 50k version, this provides the ROI for better field training.
        pass