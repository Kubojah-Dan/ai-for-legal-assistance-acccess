import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_legal_document_pdf(
    doc_title: str,
    applicant_name: str,
    applicant_contact: str,
    applicant_address: str,
    opposite_party_name: str,
    opposite_party_address: str,
    incident_date: str,
    facts_description: str,
    remedy_sought: str,
    statutes_cited: list,
    disputed_amount: str = None
) -> bytes:
    """
    Generates a clean, formal, ready-to-file Indian Legal Notice or Application PDF
    using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        alignment=1, # Center
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=15
    )
    
    sub_title_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        alignment=1,
        textColor=colors.HexColor("#475569"),
        spaceAfter=20
    )
    
    heading2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=8
    )

    legal_cite_style = ParagraphStyle(
        'LegalCite',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#047857"),
        spaceAfter=4
    )

    elements = []

    # Title & Legal Notice Header
    elements.append(Paragraph(doc_title.upper(), title_style))
    elements.append(Paragraph("DRAFTED COMPLIANT WITH 2024 INDIAN LEGAL STATUTES (BNS / BNSS / CPA)", sub_title_style))

    # Parties Metadata Table
    parties_data = [
        [
            Paragraph("<b>FROM (Applicant/Complainant):</b>", heading2_style),
            Paragraph("<b>TO (Opposite Party/Noticee):</b>", heading2_style)
        ],
        [
            Paragraph(f"<b>Name:</b> {applicant_name}<br/><b>Address:</b> {applicant_address}<br/><b>Contact:</b> {applicant_contact}", body_style),
            Paragraph(f"<b>Name:</b> {opposite_party_name}<br/><b>Address:</b> {opposite_party_address}", body_style)
        ]
    ]
    t = Table(parties_data, colWidths=[260, 260])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))

    # Date and Subject
    elements.append(Paragraph(f"<b>DATE OF DISPUTE/INCIDENT:</b> {incident_date}", body_style))
    if disputed_amount:
        elements.append(Paragraph(f"<b>DISPUTED AMOUNT / VALUATION:</b> INR ₹{disputed_amount}", body_style))
    elements.append(Spacer(1, 10))

    # Section 1: Statement of Facts
    elements.append(Paragraph("1. STATEMENT OF FACTS", heading2_style))
    for para in facts_description.split("\n\n"):
        if para.strip():
            elements.append(Paragraph(para.strip(), body_style))
    elements.append(Spacer(1, 10))

    # Section 2: Statutory Provisions & 2024 Legal Citations
    elements.append(Paragraph("2. STATUTORY BREACHES & LEGAL CITATIONS (2024)", heading2_style))
    for cite in statutes_cited:
        elements.append(Paragraph(f"• <b>{cite}</b>", legal_cite_style))
    elements.append(Spacer(1, 10))

    # Section 3: Remedy & Demand
    elements.append(Paragraph("3. REMEDY SOUGHT / FORMAL DEMAND", heading2_style))
    elements.append(Paragraph(remedy_sought, body_style))
    elements.append(Spacer(1, 15))

    # Section 4: Notice Period & Escalation Warning
    elements.append(Paragraph("4. NOTICE TIMELINE & LEGAL ESCALATION", heading2_style))
    elements.append(Paragraph(
        "TAKE NOTE that if the above demands are not satisfied within 15 (fifteen) days from the receipt of this legal document, the Complainant shall be constrained to initiate formal judicial proceedings under Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 or the Consumer Protection Act, 2019 before the competent court/tribunal entirely at your risk as to cost and consequences.",
        body_style
    ))
    elements.append(Spacer(1, 25))

    # Signature Block
    elements.append(Paragraph(f"<b>(Signature of Applicant/Complainant)</b><br/>{applicant_name}<br/>Date: {datetime.now().strftime('%d %B %Y')}", body_style))
    elements.append(Spacer(1, 20))

    # Free Legal Aid Disclaimer
    elements.append(Paragraph(
        "<font size=8 color='#64748b'><i>NyayaMitra Public Legal Tech Initiative: For citizens unable to afford representation, free legal aid is available under the Legal Services Authorities Act, 1987 via Tele-Law (Call 1516) or National Legal Services Authority (NALSA 15100).</i></font>",
        body_style
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
