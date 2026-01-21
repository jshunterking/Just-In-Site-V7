import qrcode
from io import BytesIO
from monkey_heart import MonkeyHeart
from monkey_brain import MonkeyBrain
from bananas import Bananas


class RabbitLabels:
    """
    RABBIT PROTOCOL: High-speed lateral expansion for Field Identification.
    OXIDE DISSECTION: Generating QR signatures for Assemblies, Tools, and Plans.
    Target: 0-second latency between Physical Object and Digital Data.
    """

    @staticmethod
    def generate_qr_signature(data_string):
        """
        OXIDE: Converts a data string (URL or ID) into a high-fidelity QR Code.
        Returns a PIL image object for UI rendering or printing.
        """
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data_string)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Save to buffer for Streamlit/Web display
            buf = BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()

        except Exception as e:
            Bananas.report_collision(e, "QR_GENERATION_FAILURE")
            return None

    @staticmethod
    def map_prefab_kit(assembly_id):
        """
        Generates a label for a Pre-Fab assembly.
        The QR points to the internal URL for that specific kit's BOM.
        """
        # In a 50k line app, 'domain' would be your Railway URL
        domain = "https://just-in-site-production.up.railway.app"
        target_url = f"{domain}/?view=prefab&id={assembly_id}"

        return RabbitLabels.generate_qr_signature(target_url)

    @staticmethod
    def map_asset_tag(asset_id):
        """
        Generates a permanent ID tag for tools and equipment.
        Allows instant 'Check-In/Out' from the field.
        """
        return RabbitLabels.generate_qr_signature(asset_id)

    @staticmethod
    def map_document_link(project_id, doc_type):
        """
        Generates a QR for job-site postings.
        Scan the QR on the electrical room door to see the latest As-Builts.
        """
        link = f"DOC_VAULT_{project_id}_{doc_type}"
        return RabbitLabels.generate_qr_signature(link)