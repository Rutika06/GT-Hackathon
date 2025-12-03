from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd

def generate_pdf_report(dataset_name: str, df: pd.DataFrame, insights_text: str, output_path: str) -> str:
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Automated Data Insight Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Dataset: {dataset_name}")

    y = height - 120
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "Executive Insights:")

    y -= 20
    for line in insights_text.split("\n"):
        if not line.strip():
            continue
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)
        c.drawString(60, y, f"- {line}")
        y -= 15

    c.save()
    return output_path
