from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(data):
    c = canvas.Canvas("ATS_Report.pdf", pagesize=A4)
    w, h = A4

    y = h - 50
    for key, value in data.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

    c.save()
