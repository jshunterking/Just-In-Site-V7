import pandas as pd
import io
from datetime import datetime
from monkey_heart import MonkeyHeart
from monkey_brain import MonkeyBrain
from bananas import Bananas


class RabbitFoundation:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for Financial Integration.
    OXIDE DISSECTION: Mapping project data to Foundation Software import formats.
    Target: Eliminating double-entry for Ohio Accounting Departments.
    """

    @staticmethod
    def dissect_for_accounting(project_id):
        """
        OXIDE: Re-maps internal project data into the 'Job Cost' structure
        required by enterprise accounting software.
        """
        try:
            query = """
                SELECT project_id as [Job Number], 
                       project_name as [Description], 
                       trade_focus as [Department],
                       gross_margin_target as [Estimated Profit]
                FROM core_projects WHERE project_id = ?
            """
            df = MonkeyBrain.query_oxide(query, (project_id,))

            # Foundation Software requires specific CSV headers (A-E format)
            # We transform our 'Monkey' data into 'Accounting' data here.
            if not df.empty:
                df['Customer ID'] = "OH-CONTRACTOR-01"  # Placeholder for Client Mapping
                df['Status Code'] = "A"  # Active
                return df
            return None

        except Exception as e:
            Bananas.report_collision(e, "FOUNDATION_MAPPING_FAILURE")
            return None

    @staticmethod
    def generate_csv_export(df):
        """
        OXIDE: Converts the mapped dataframe into a downloadable buffer
        for the user to upload into Foundation Software.
        """
        output = io.BytesIO()
        df.to_csv(output, index=False)
        processed_data = output.getvalue()
        return processed_data

    @staticmethod
    def get_phase_codes(trade_focus):
        """
        Dissects trade-specific phase codes (CSI Codes) for accounting.
        """
        codes = {
            "ELECTRICAL CONTRACTOR": "26-00-00",
            "PLUMBING & MECHANICAL": "22-00-00",
            "HVAC / SHEET METAL": "23-00-00"
        }
        return codes.get(trade_focus, "00-00-00")