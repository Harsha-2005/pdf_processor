# # generate_test_pdfs.py
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.enums import TA_CENTER
# import os

# # Create directories
# os.makedirs("input", exist_ok=True)

# # Simple PDF
# def create_simple_pdf():
#     doc = SimpleDocTemplate("input/simple.pdf", pagesize=letter)
#     styles = getSampleStyleSheet()
#     story = []
    
#     title_style = ParagraphStyle(
#         "Title",
#         parent=styles["Heading1"],
#         fontSize=24,
#         alignment=TA_CENTER
#     )
#     story.append(Paragraph("Understanding AI", title_style))
#     story.append(Paragraph("1. Introduction", styles["Heading1"]))
#     story.append(Paragraph("What is Artificial Intelligence?", styles["BodyText"]))
#     story.append(Paragraph("1.1 History", styles["Heading2"]))
#     story.append(Paragraph("AI development timeline", styles["BodyText"]))
    
#     doc.build(story)

# create_simple_pdf()
# print("Generated sample PDFs in input/ directory")
# Create new file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Create input directory
os.makedirs("input", exist_ok=True)

def create_simple_pdf():
    c = canvas.Canvas("input/simple.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "1. Introduction")
    c.setFont("Helvetica", 18)
    c.drawString(100, 700, "1.1 What is AI?")
    c.save()

def create_complex_pdf():
    c = canvas.Canvas("input/complex.pdf", pagesize=letter)
    # Multi-page with different styles
    for page_num in range(3):
        c.setFont("Times-Bold", 20)
        c.drawString(100, 750, f"Chapter {page_num+1}")
        c.setFont("Times-Roman", 16)
        c.drawString(100, 700, f"Section {page_num+1}.1")
        c.setFont("Courier", 14)
        c.drawString(100, 650, f"Subsection {page_num+1}.1.1")
        c.showPage()  # End page
    c.save()

def create_japanese_pdf():
    c = canvas.Canvas("input/japanese.pdf", pagesize=letter)
    # Japanese text (UTF-8 encoded)
    jp_text = [
        "第1章: 導入",
        "人工知能の基本概念",
        "1.1 機械学習とは"
    ]
    y_pos = 750
    for text in jp_text:
        c.setFont("Helvetica", 18)  # Fallback font
        c.drawString(100, y_pos, text)
        y_pos -= 50
    c.save()

if __name__ == "__main__":
    create_simple_pdf()
    create_complex_pdf()
    create_japanese_pdf()
    print("Generated test PDFs: simple.pdf, complex.pdf, japanese.pdf")