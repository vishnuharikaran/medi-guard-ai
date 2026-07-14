"""Diagnostic PDF Report Compiler using ReportLab."""

from __future__ import annotations

import io
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas helper for adding 'Page X of Y' footer dynamically."""
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
        self.drawString(54, 750, "MediGuard AI - Digital Health Twin Assessment Report")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer (Bottom of page)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.drawString(54, 40, "Confidential - Medical Twin Diagnostic Screening Report")
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
    """Compiles assessment details into a clinical-grade PDF document."""
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
    
    # Custom clinical palette styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=15
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155")
    )
    
    label_style = ParagraphStyle(
        'GridLabel',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#475569")
    )
    
    bullet_style = ParagraphStyle(
        'BulletItem',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )

    story = []
    
    # Title
    story.append(Paragraph("MediGuard AI Assessment Report", title_style))
    story.append(Paragraph("Personalized Preventive Screening & Digital Health Twin Diagnostics", body_style))
    story.append(Spacer(1, 15))
    
    # Patient Demographics block
    demo_data = [
        [
            Paragraph("Patient Name:", label_style), Paragraph(profile.name, body_style),
            Paragraph("Report Date:", label_style), Paragraph("Current Assessment", body_style)
        ],
        [
            Paragraph("Age / Gender:", label_style), Paragraph(f"{profile.age} / {profile.gender}", body_style),
            Paragraph("Assessment Type:", label_style), Paragraph("Digital Health Twin", body_style)
        ]
    ]
    demo_table = Table(demo_data, colWidths=[110, 142, 110, 142])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#F1F5F9")),
    ]))
    story.append(demo_table)
    story.append(Spacer(1, 20))
    
    # Twin Diagnostics Metrics Summary
    story.append(Paragraph("Digital Twin Biological Metrics", section_title_style))
    
    age_delta_text = f"+{age_diff}" if age_diff > 0 else f"{age_diff}"
    twin_data = [
        [
            Paragraph("Biological Health Score", label_style),
            Paragraph("Chronological Age", label_style),
            Paragraph("Estimated Twin Health Age", label_style),
            Paragraph("Triage Priority Level", label_style)
        ],
        [
            Paragraph(f"<b>{health_score} / 100</b> ({category})", body_style),
            Paragraph(f"{profile.age} years", body_style),
            Paragraph(f"{health_age} years ({age_delta_text} diff)", body_style),
            Paragraph(f"{triage['color']} - {triage['level']}", body_style)
        ]
    ]
    twin_table = Table(twin_data, colWidths=[126, 126, 126, 126])
    twin_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#DBEAFE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EFF6FF")),
    ]))
    story.append(twin_table)
    story.append(Spacer(1, 15))
    
    # Vital Vitals Table
    story.append(Paragraph("Vitals & Lab Parameters", section_title_style))
    vitals_headers = [
        Paragraph("Parameter", label_style),
        Paragraph("Measured Value", label_style),
        Paragraph("Ideal Clinical Boundaries", label_style)
    ]
    
    vitals_rows = [
        vitals_headers,
        [Paragraph("Height", body_style), Paragraph(f"{profile.height:.1f} cm", body_style), Paragraph("160.0 - 190.0 cm", body_style)],
        [Paragraph("Weight", body_style), Paragraph(f"{profile.weight:.1f} kg", body_style), Paragraph("50.0 - 100.0 kg", body_style)],
        [Paragraph("Systolic Blood Pressure", body_style), Paragraph(f"{int(profile.systolic_bp)} mmHg", body_style), Paragraph("90.0 - 120.0 mmHg", body_style)],
        [Paragraph("Diastolic Blood Pressure", body_style), Paragraph(f"{int(profile.diastolic_bp)} mmHg", body_style), Paragraph("60.0 - 80.0 mmHg", body_style)],
        [Paragraph("Fasting Blood Sugar", body_style), Paragraph(f"{int(profile.blood_sugar)} mg/dL", body_style), Paragraph("70.0 - 100.0 mg/dL", body_style)],
        [Paragraph("Resting Heart Rate", body_style), Paragraph(f"{int(profile.heart_rate)} bpm", body_style), Paragraph("60.0 - 100.0 bpm", body_style)],
    ]
    vitals_table = Table(vitals_rows, colWidths=[180, 162, 162])
    vitals_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
    ]))
    story.append(vitals_table)
    story.append(Spacer(1, 15))
    
    # Disease Risks
    story.append(Paragraph("Predictive Disease Risk Stratification", section_title_style))
    risk_headers = [
        Paragraph("Target Condition", label_style),
        Paragraph("Forecasted Risk Probability", label_style),
        Paragraph("Clinical Severity", label_style)
    ]
    
    risk_rows = [risk_headers]
    for disease, details in risks.items():
        risk_rows.append([
            Paragraph(disease, body_style),
            Paragraph(f"{details['probability']:.1%}", body_style),
            Paragraph(details["label"], body_style)
        ])
        
    risk_table = Table(risk_rows, colWidths=[180, 162, 162])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#FFFBEB")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor("#FDE68A")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FDE68A")),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 15))
    
    # Triage Action Recommended
    story.append(Paragraph("Smart Clinical Triage & Actions", section_title_style))
    triage_text = f"<b>Recommended Action:</b> {triage['action']}"
    story.append(Paragraph(triage_text, body_style))
    story.append(Spacer(1, 15))
    
    # Recommendations
    story.append(Paragraph("Personalized Medical Recommendations", section_title_style))
    for rec in recommendations:
        story.append(Paragraph(f"• {rec}", bullet_style))
        
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer.getvalue()
