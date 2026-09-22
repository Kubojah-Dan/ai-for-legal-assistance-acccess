from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/tracker", tags=["Nyaya Case Tracker"])

class CaseTrackerRequest(BaseModel):
    cnr_or_fir: str

@router.post("/status")
async def get_case_status(req: CaseTrackerRequest):
    return {
        "cnr": (req.cnr_or_fir or "MHPU010045212024").upper(),
        "status": "Hearing Pending",
        "current_stage": "Notice / Hearing",
        "court_name": "District & Sessions Court, Pune",
        "next_hearing_date": "October 14, 2026",
        "petitioner": "Ramesh Kumar",
        "act_applicable": "Model Tenancy Act / Sec 329 BNS 2023",
        "ecourts_url": "https://ecourts.gov.in"
    }
