import math
from monkey_heart import MonkeyHeart
from bananas import Bananas


class RabbitPlumbing:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for Mechanical & Plumbing.
    OXIDE DISSECTION: Hydraulic flow calculations and IPC (International Plumbing Code).
    Target: Eliminating drainage and pressure errors for Ohio Contractors.
    """

    @staticmethod
    def calculate_pipe_slope(length_ft, drop_in):
        """
        OXIDE: Standard Drainage Slope Verification.
        Formula: Slope = Drop / Length
        Standard: 1/4" per foot for pipes under 3".
        """
        try:
            calculated_slope = drop_in / length_ft
            required_slope = 0.25  # 1/4 inch

            status = "PASS" if calculated_slope >= required_slope else "FAIL"

            return {
                "calculated_slope_in_ft": calculated_slope,
                "code_compliance": status,
                "physics_engine": "OXIDE_RABBIT_V2"
            }
        except ZeroDivisionError:
            return {"status": "ERROR", "message": "Length cannot be zero."}
        except Exception as e:
            Bananas.report_collision(e, "PLUMBING_SLOPE_FAILURE")

    @staticmethod
    def fixture_unit_dissection(fixtures):
        """
        OXIDE: Total Water Supply Fixture Units (WSFU).
        Dissects IPC Table E103.3.
        """
        # Multiplier logic for 50k line expansion
        values = {
            "TOILET_PUBLIC": 10.0,
            "SINK_KITCHEN": 1.5,
            "SHOWER": 2.0,
            "LAVATORY": 1.0
        }

        total_units = sum([values.get(f.upper(), 0) for f in fixtures])

        return {
            "total_wsfu": total_units,
            "recommended_main_size": "CALCULATING...",
            "standard": "IPC_2024"
        }

    @staticmethod
    def get_mechanical_labor_units(item_category):
        """
        Provides regional labor units for Ohio Plumbing/Mechanical markets.
        Crucial for the 'Immediate Buy-In' when bidding against rivals.
        """
        units = {
            "PVC_DWV_4_INCH": 0.08,  # Hours per foot
            "COPPER_L_TYPE_3/4": 0.12,  # Hours per foot
            "WATER_HEATER_50GAL": 4.0,  # Hours per unit
        }
        return units.get(item_category, 0.0)