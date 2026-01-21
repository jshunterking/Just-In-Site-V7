import sys
from monkey_brain import MonkeyBrain
from monkey_heart import MonkeyHeart
from bananas import Bananas
from raptor_automation import RaptorAutomation
from owl_singularity import OwlSingularity


class OxideSingularity:
    """
    THE SINGULARITY: The terminal point of the Oxide Architecture.
    OXIDE DISSECTION: Bootstrapping the entire 50-block ecosystem.
    Target: 100% System Integration and Autonomous Business Operations.
    """

    @staticmethod
    def ignite_system():
        """
        THE FINAL STRIKE:
        1. Establishes the 'Brain' Connection.
        2. Validates the 'Heart' Pulse.
        3. Initializes all Rabbit Burrows & Owl Wisdom.
        4. Launches the Raptor Ghost Workers.
        """
        print("--- INITIATING OXIDE SINGULARITY ---")

        try:
            # 1. Start the Brain
            if not MonkeyBrain.get_connection():
                raise ConnectionError("CRITICAL_BRAIN_FAILURE: Single Source of Truth offline.")

            # 2. Synchronize Heart & Pulse
            MonkeyHeart.log_system_event("SINGULARITY_IGNITION", "Just-In-Site OS version 2026.1 Online.")

            # 3. Deploy the Raptors (Phase 4 Automation)
            # This ensures the 'Ghost Workers' start their nightly cycles
            RaptorAutomation.process_nightly_ghost_tasks()

            # 4. Generate the First 'God-View' Report
            intelligence = OwlSingularity.calculate_enterprise_pulse()

            print(f"SYSTEM_STATUS: [ONLINE]")
            print(f"ENTERPRISE_PULSE: [{intelligence['singularity_score']}/100]")
            print(f"OUTLOOK: [{intelligence['outlook']}]")
            print("--- JUST-IN-SITE IS NOW LIVE ---")

            Bananas.notify("SYSTEM_IGNITION", "All 50 Blocks of the Oxide Singularity are operational.")
            return True

        except Exception as e:
            Bananas.report_collision(e, "SINGULARITY_LAUNCH_FAILURE")
            sys.exit(1)


if __name__ == "__main__":
    # The final command that brings the entire project to life.
    OxideSingularity.ignite_system()