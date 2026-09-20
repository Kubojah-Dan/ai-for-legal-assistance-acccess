from fastapi import APIRouter
from app.models.schemas import CitationCheckRequest, CitationCheckResponse
from app.utils.bns_mapping import validate_citations

router = APIRouter(prefix="/api/compliance", tags=["Compliance"])


@router.post("/verify-citations", response_model=CitationCheckResponse)
async def verify_legal_citations(request: CitationCheckRequest):
    """
    Evaluator Proof Endpoint:
    Checks if provided text contains any hallucinations of repealed British-era laws
    (IPC 1860, CrPC 1973, Evidence Act 1872).
    Returns strict 2024 compliance score.
    """
    check_result = validate_citations(request.text)
    score = 100.0 if check_result["compliant_2024"] else 0.0
    return CitationCheckResponse(
        compliant_2024=check_result["compliant_2024"],
        repealed_laws_detected=check_result["repealed_laws_detected"],
        statutes_applicable=check_result["statutes_applicable"],
        verification_score=score
    )
