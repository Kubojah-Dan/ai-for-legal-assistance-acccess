from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/bns", tags=["BNS Law Converter"])

class BnsConvertRequest(BaseModel):
    query: str

@router.post("/convert")
async def convert_bns(req: BnsConvertRequest):
    q = req.query.lower()
    if "420" in q:
        return {
            "old_statute": "IPC Section 420",
            "new_statute": "BNS Section 318(4)",
            "title": "Cheating & Dishonestly Inducing Delivery of Property",
            "changes": "Updated penalties and specific provisions for cyber financial fraud."
        }
    elif "302" in q:
        return {
            "old_statute": "IPC Section 302",
            "new_statute": "BNS Section 103",
            "title": "Punishment for Murder",
            "changes": "Includes mob lynching by 5+ persons under BNS 103(2)."
        }
    else:
        return {
            "old_statute": "CrPC Section 154",
            "new_statute": "BNSS Section 173(1)",
            "title": "Zero FIR Registration Anywhere",
            "changes": "Mandatory Zero FIR registration nationwide regardless of territorial jurisdiction."
        }
