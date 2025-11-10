import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from models import Property, Task, User  # or whatever models you use

REPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(REPORT_DIR, exist_ok=True)


def generate_property_report(property_id: int, db: Session) -> str:
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise ValueError("Property not found")

    tasks = db.query(models.Task).filter(models.Task.property_id == property_id).all()

    filename = f"property_{property_id}_report.pdf"
    path = os.path.join(REPORT_DIR, filename)

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"FixHub Report - {prop.name}")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Address: {prop.address}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Tasks:")
    y -= 20
    c.setFont("Helvetica", 10)

    for t in tasks:
        if y < 80:
            c.showPage()
            y = height - 50
        line = f"- {t.title} | {t.status} | Assigned: {t.assigned_to or 'N/A'}"
        c.drawString(60, y, line)
        y -= 15

    c.showPage()
    c.save()
    return path
