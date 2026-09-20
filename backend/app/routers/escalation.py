from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/api/escalation", tags=["Escalation"])


class AidResource(BaseModel):
    name: str
    phone: str
    website: str
    coverage: str
    fee: str
    eligibility: str


@router.get("/resources", response_model=List[AidResource])
async def get_legal_aid_resources():
    """
    Returns verified free human legal aid networks in India
    under the Legal Services Authorities Act, 1987.
    """
    return [
        AidResource(
            name="Tele-Law Scheme (Department of Justice)",
            phone="1516",
            website="https://www.tele-law.in",
            coverage="Pan-India across 100,000+ Common Service Centres (CSCs)",
            fee="Free of cost for women, SC/ST, victims of trafficking, and low-income citizens",
            eligibility="Section 12 Legal Services Authorities Act"
        ),
        AidResource(
            name="National Legal Services Authority (NALSA)",
            phone="15100",
            website="https://nalsa.gov.in",
            coverage="All High Courts, District Legal Services Authorities (DLSA), Taluk Committees",
            fee="100% Free legal aid and advocate assignment",
            eligibility="Annual income < ₹3 Lakhs, women, children, workers, undertrial prisoners"
        ),
        AidResource(
            name="National Cyber Crime Reporting Helpline",
            phone="1930",
            website="https://cybercrime.gov.in",
            coverage="Real-time financial fraud coordination across Indian banks",
            fee="Free Govt Helpline",
            eligibility="Any citizen reporting unauthorized transaction within golden window"
        ),
        AidResource(
            name="National Consumer Helpline (NCH)",
            phone="1915",
            website="https://consumerhelpline.gov.in",
            coverage="Pre-litigation conciliation with 10,000+ registered corporations",
            fee="Free Govt Service",
            eligibility="All Indian consumers"
        )
    ]
