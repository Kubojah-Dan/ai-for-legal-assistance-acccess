from fastapi import APIRouter, HTTPException
from app.models.schemas import RightsRequest, RightsResponse, LegalRightItem
from app.services.legal_service import legal_service

router = APIRouter(prefix="/api/rights", tags=["Rights"])


@router.post("", response_model=RightsResponse)
async def get_rights(request: RightsRequest):
    """
    Step 2: Mere Adhikaar (Know My Rights)
    Grounded on 2024 Indian Law (BNS, BNSS, BSA, CPA 2019, Model Tenancy Act).
    Explains statutory rights at a Grade 6 reading level, delivers concrete deadlines,
    and checks Zero-FIR eligibility under Section 173(1) BNSS 2023.
    """
    if not request.domain:
        raise HTTPException(status_code=400, detail="Domain must be specified")

    result = await legal_service.get_rights_and_timeline(
        domain=request.domain,
        user_query=request.user_query,
        context=request.answered_context,
        language=request.language
    )

    items = [
        LegalRightItem(
            right_en=r["right_en"],
            right_hi=r["right_hi"],
            statute_2024=r["statute_2024"],
            description_en=r["description_en"],
            description_hi=r["description_hi"],
            urgency_level=r["urgency_level"]
        )
        for r in result.get("rights", [])
    ]

    return RightsResponse(
        domain=result.get("domain", request.domain),
        reading_level="Grade 6",
        rights=items,
        concrete_timeline=result.get("concrete_timeline", "15 to 30 days statutory period"),
        deadline_days=result.get("deadline_days", 15),
        zero_fir_eligible=result.get("zero_fir_eligible", False),
        free_aid_recommended=result.get("free_aid_recommended", True),
        aid_contact=result.get("aid_contact", "Tele-Law 1516 / NALSA 15100"),
        compliance_2024=True,
        bns_citations=result.get("bns_citations", [])
    )
