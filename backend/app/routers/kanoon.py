from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/kanoon", tags=["Kanoon Explainer"])

class KanoonQueryRequest(BaseModel):
    query: str

@router.post("/explain")
async def explain_law(req: KanoonQueryRequest):
    q = req.query.lower()
    if any(k in q for k in ["evict", "tenant", "landlord", "rent"]):
        return {
            "answer": "Under the Model Tenancy Act 2021 & BNS Section 329, no landlord can evict a tenant without giving a statutory 30-day written notice. Landlords cannot cut off electricity or water supply or lock out tenants forcibly.",
            "statutes": ["BNS 2023 Section 329 (Criminal Trespass)", "Model Tenancy Act 2021 Section 20", "BNSS Section 173 (Zero FIR)"]
        }
    elif any(k in q for k in ["cyber", "upi", "fraud", "scam"]):
        return {
            "answer": "Digital financial fraud and UPI cheating are punishable under BNS Section 318(4) and IT Act Section 66D. If reported within 24 hours via Cyber Helpline 1930, stolen funds can be frozen immediately in the scammer bank account.",
            "statutes": ["BNS Section 318(4) (Financial Cheating)", "IT Act Section 66D", "MHA Cyber Fraud Protocol"]
        }
    else:
        return {
            "answer": "Under Indian Consumer Protection Act 2019, buyers delivered defective goods or deficient services are entitled to full refund, replacement, or compensation via District Consumer Commission.",
            "statutes": ["Consumer Protection Act 2019 Section 35", "BNS 2023 Section 318"]
        }
