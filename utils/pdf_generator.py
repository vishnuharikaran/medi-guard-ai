"""Educational PDF Report Compiler using ReportLab with HTML/XML Escaping and Medical Disclaimers."""

from __future__ import annotations

import io
import html
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Canvas helper for adding header and 'Page X of Y' footer dynamically."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Top of page)
        self.drawString(54, 750, "Medi-Guard AI — Educational Health Profile Report")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer (Bottom of page)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.drawString(54, 40, "Educational Prototype — Non-Clinical Demonstration Report")
        self.line(54, 52, 558, 52)
        
        self.restoreState()


def generate_health_report_pdf(
    profile,
    health_score: int,
    category: str,
    health_age: int,
    age_diff: int,
    triage: dict,
    risks: dict,
    recommendations: list[str]
) -> bytes:
    """Compiles assessment details into an Educational PDF document with safe text escaping."""
    buffer = io.BytesIO()
    
    # Setup document geometry (0.75 in / 54pt margins)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom palette styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0284C7"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155")
    )
    
    label_style = ParagraphStyle(
        'GridLabel',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#475569")
    )

    disclaimer_style = ParagraphStyle(
        'DisclaimerText',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#991B1B")
    )

    bullet_style = ParagraphStyle(
        'BulletItem',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4
    )

    story = []
    
    # Title & Subtitle with Escaping
    safe_name = html.escape(profile.name)
    safe_gender = html.escape(profile.gender)

    story.append(Paragraph("Medi-Guard — Educational Health Profile & Model Output Report", title_style))
    story.append(Paragraph("Non-Clinical Software Demonstration & Experimental Machine Learning Analytics", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Demographics Block
    demo_data = [
        [
            Paragraph("Patient Name:", label_style), Paragraph(safe_name, body_style),
            Paragraph("Report Purpose:", label_style), Paragraph("Educational Demonstration", body_style)
        ],
        [
            Paragraph("Age / Gender:", label_style), Paragraph(f"{profile.age} yrs / {safe_gender}", body_style),
            Paragraph("Software Model:", label_style), Paragraph("Experimental Classifier Pipeline", body_style)
        ]
    ]
    demo_table = Table(demo_data, colWidths=[105, 147, 105, 147])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#F1F5F9")),
    ]))
    story.append(demo_table)
    story.append(Spacer(1, 14))
    
    # Metrics Summary Table
    story.append(Paragraph("Educational Metric Summaries", section_title_style))
    
    age_delta_text = f"+{age_diff}" if age_diff > 0 else f"{age_diff}"
    twin_data = [
        [
            Paragraph("Health Score", label_style),
            Paragraph("Chronological Age", label_style),
            Paragraph("Lifestyle Age Estimate", label_style),
            Paragraph("Triage Priority", label_style)
        ],
        [
            Paragraph(f"<b>{health_score} / 100</b> ({html.escape(category)})", body_style),
            Paragraph(f"{profile.age} years", body_style),
            Paragraph(f"{health_age} years ({age_delta_text} yrs)", body_style),
            Paragraph(f"{html.escape(triage['color'])} - {html.escape(triage['level'])}", body_style)
        ]
    ]
    twin_table = Table(twin_data, colWidths=[126, 126, 126, 126])
    twin_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F0F9FF")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E0F2FE")),
    ]))
    story.append(twin_table)
    story.append(Spacer(1, 14))
    
    # Measured Vitals Table
    story.append(Paragraph("Measured Physiological Metrics", section_title_style))
    vitals_headers = [
        Paragraph("Parameter", label_style),
        Paragraph("Value", label_style),
        Paragraph("Reference Range", label_style)
    ]
    
    vitals_rows = [
        vitals_headers,
        [Paragraph("Height", body_style), Paragraph(f"{profile.height:.1f} cm", body_style), Paragraph("80.0 - 230.0 cm", body_style)],
        [Paragraph("Weight", body_style), Paragraph(f"{profile.weight:.1f} kg", body_style), Paragraph("20.0 - 220.0 kg", body_style)],
        [Paragraph("BMI", body_style), Paragraph(f"{profile.bmi:.2f} kg/m²", body_style), Paragraph("18.5 - 24.9 kg/m²", body_style)],
        [Paragraph("Systolic Blood Pressure", body_style), Paragraph(f"{int(profile.systolic_bp)} mmHg", body_style), Paragraph("90 - 120 mmHg", body_style)],
        [Paragraph("Diastolic Blood Pressure", body_style), Paragraph(f"{int(profile.diastolic_bp)} mmHg", body_style), Paragraph("60 - 80 mmHg", body_style)],
        [Paragraph("Fasting Blood Sugar", body_style), Paragraph(f"{int(profile.blood_sugar)} mg/dL", body_style), Paragraph("70 - 100 mg/dL", body_style)],
        [Paragraph("Resting Heart Rate", body_style), Paragraph(f"{int(profile.heart_rate)} bpm", body_style), Paragraph("60 - 100 bpm", body_style)],
    ]
    vitals_table = Table(vitals_rows, colWidths=[180, 162, 162])
    vitals_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
    ]))
    story.append(vitals_table)
    story.append(Spacer(1, 14))
    
    # Experimental Disease Risks Table
    story.append(Paragraph("Experimental Model Disease Classifications", section_title_style))
    risk_headers = [
        Paragraph("Target Disease", label_style),
        Paragraph("Experimental Probability", label_style),
        Paragraph("Risk Classification", label_style)
    ]
    
    risk_rows = [risk_headers]
    for disease, details in risks.items():
        risk_rows.append([
            Paragraph(html.escape(disease), body_style),
            Paragraph(f"{details['probability']:.1%}", body_style),
            Paragraph(html.escape(details["label"]), body_style)
        ])
        
    risk_table = Table(risk_rows, colWidths=[180, 162, 162])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#FEF3C7")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor("#FDE68A")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FDE68A")),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 14))
    
    # Educational Recommendations
    story.append(Paragraph("Educational Lifestyle Suggestions", section_title_style))
    for rec in recommendations:
        story.append(Paragraph(f"• {html.escape(rec)}", bullet_style))
        
    story.append(Spacer(1, 14))

    # Mandatory Legal/Medical Disclaimer Box
    disclaimer_box = [
        [Paragraph("<b>IMPORTANT NOTICE:</b> This report is generated by an educational software prototype. It has not been validated for clinical diagnosis, treatment decisions, or emergency triage. Consult a qualified healthcare professional for medical interpretation.", disclaimer_style)]
    ]
    disclaimer_table = Table(disclaimer_box, colWidths=[504])
    disclaimer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCA5A5")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(disclaimer_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer.getvalue()
