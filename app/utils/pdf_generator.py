from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from datetime import datetime


def create_pdf(review: dict, filename: str, output_path: str):
    """
    Creates a professional PDF report from the AI review.
    """

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(output_path)

    elements = []

    elements.append(Paragraph("<b>AI Software Review Report</b>", styles["Title"]))

    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(f"<b>Filename:</b> {filename}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"<b>Overall Score:</b> {review['score']}/10", styles["Heading2"])
    )

    elements.append(
        Paragraph("<b>Summary</b>", styles["Heading2"])
    )
    elements.append(
        Paragraph(review["summary"], styles["BodyText"])
    )

    sections = [
        ("Bugs", review["bugs"]),
        ("Security Issues", review["security"]),
        ("Performance", review["performance"]),
        ("Code Quality", review["quality"]),
        ("PEP8", review["pep8"]),
    ]

    for title, items in sections:

        elements.append(
            Paragraph(f"<b>{title}</b>", styles["Heading2"])
        )

        if len(items) == 0:

            elements.append(
                Paragraph("No issues found.", styles["BodyText"])
            )

        else:

            for item in items:

                elements.append(
                    Paragraph(f"• {item}", styles["BodyText"])
                )

    doc.build(elements)