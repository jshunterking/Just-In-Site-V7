import math
from monkey_heart import MonkeyHeart
from bananas import Bananas


class RabbitHVAC:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for HVAC & Sheet Metal.
    OXIDE DISSECTION: Airflow dynamics, duct sizing, and thermal load calcs.
    Target: Zero-error ventilation and heating design for Ohio Contractors.
    """

    @staticmethod
    def calculate_duct_velocity(cfm, area_sq_in):
        """
        OXIDE: Standard Air Velocity Calculation.
        Formula: Velocity (FPM) = CFM / Area (sq ft)
        Target: Maintaining quiet and efficient airflow (typically < 1000 FPM for residential).
        """
        try:
            area_sq_ft = area_sq_in / 144
            velocity = cfm / area_sq_ft

            status = "OPTIMAL" if velocity <= 1200 else "TURBULENT"

            return {
                "velocity_fpm": round(velocity, 2),
                "airflow_status": status,
                "physics_engine": "OXIDE_RABBIT_V3"
            }
        except ZeroDivisionError:
            return {"status": "ERROR", "message": "Duct area cannot be zero."}
        except Exception as e:
            Bananas.report_collision(e, "HVAC_VELOCITY_CRASH")

    @staticmethod
    def btu_load_dissection(sq_ft, ceiling_height=8, insulation_factor=1.2):
        """
        OXIDE: Rough-in BTU/h estimation for heating/cooling requirements.
        Dissects volume and thermal efficiency.
        """
        try:
            volume = sq_ft * ceiling_height
            # Simplified base calc: Volume * factor
            estimated_btu = volume * 20 * insulation_factor
            tonnage = estimated_btu / 12000

            return {
                "estimated_btu_h": round(estimated_btu, 2),
                "required_tonnage": round(tonnage, 1),
                "insulation_multiplier": insulation_factor
            }
        except Exception as e:
            Bananas.report_collision(e, "THERMAL_LOAD_FAILURE")

    @staticmethod
    def get_sheet_metal_labor_units(item_category):
        """
        Provides regional labor units for Ohio HVAC/Sheet Metal markets.
        Ensures the 'Immediate Buy-In' for mechanical estimators.
        """
        units = {
            "RECT_DUCT_GALVANIZED": 0.15,  # Hours per lb
            "FLEX_DUCT_10_INCH": 0.05,  # Hours per foot
            "RTU_5_TON_INSTALL": 16.0,  # Hours per unit
            "VAV_BOX_SETTING": 4.0  # Hours per unit
        }
        return units.get(item_category, 0.0)