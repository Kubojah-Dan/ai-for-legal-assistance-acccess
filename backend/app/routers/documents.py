from fastapi import APIRouter, HTTPException, Response
from app.models.schemas import DocumentGenerateRequest, DocumentGenerateResponse
from app.services.legal_service import legal_service
from app.utils.pdf_generator import generate_legal_document_pdf

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.post("/generate", response_model=DocumentGenerateResponse)
async def generate_document(request: DocumentGenerateRequest):
    """
    Step 3: Mera Document (Document Generation)
    Generates a ready-to-file Indian Legal Notice, RTI application,
    or Consumer Complaint formatted strictly with 2024 BNS/BNSS/CPA citations.
    """
    if not request.applicant_name or not request.opposite_party_name:
        raise HTTPException(status_code=400, detail="Applicant and Opposite Party names are mandatory")

    result = await legal_service.generate_document(request.model_dump())
    return DocumentGenerateResponse(
        doc_title=result["doc_title"],
        doc_type=result["doc_type"],
        generated_text=result["generated_text"],
        statutes_cited=result["statutes_cited"],
        filing_instructions_en=result["filing_instructions_en"],
        filing_instructions_hi=result["filing_instructions_hi"],
        tele_law_referral=result["tele_law_referral"],
        pdf_download_url=f"/api/documents/download-pdf?doc_type={request.doc_type}&applicant_name={request.applicant_name}",
        created_at=result["created_at"]
    )


@router.post("/download-pdf")
async def download_pdf_direct(request: DocumentGenerateRequest):
    """
    Generates and downloads a clean, printable PDF legal document
    using ReportLab.
    """
    statutes_map = {
        "legal_notice_tenant": ["Section 329 BNS 2023 (Criminal Trespass)", "Section 318 BNS 2023 (Cheating)", "Model Tenancy Act 2021"],
        "consumer_complaint": ["Section 35 Consumer Protection Act 2019", "Section 38 & 39 CPA 2019", "Section 318 BNS 2023"],
        "rti_application": ["Section 6(1) & 7(1) Right to Information Act, 2005"],
        "cyber_fraud_complaint": ["Section 173(1) BNSS 2023 (Zero FIR)", "Section 318(4) BNS 2023", "Section 66D IT Act 2000"]
    }
    statutes = statutes_map.get(request.doc_type, ["Bharatiya Nyaya Sanhita (BNS) 2023"])

    pdf_bytes = generate_legal_document_pdf(
        doc_title=f"LEGAL NOTICE / FORMAL COMPLAINT ({request.doc_type.upper().replace('_', ' ')})",
        applicant_name=request.applicant_name,
        applicant_contact=request.applicant_contact,
        applicant_address=request.applicant_address,
        opposite_party_name=request.opposite_party_name,
        opposite_party_address=request.opposite_party_address,
        incident_date=request.incident_date,
        facts_description=request.facts_description,
        remedy_sought=request.remedy_sought,
        statutes_cited=statutes,
        disputed_amount=request.disputed_amount
    )

    filename = f"NyayaMitra_{request.doc_type}_{request.applicant_name.replace(' ', '_')}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=\"{filename}\"",
            "X-Generated-By": "NyayaMitra-LegalTech-2024"
        }
    )
