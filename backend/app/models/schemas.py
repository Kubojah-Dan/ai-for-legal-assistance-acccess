from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class IntakeClarifyingQuestion(BaseModel):
    id: str = Field(..., description="Unique question ID")
    question_en: str = Field(..., description="English question")
    question_hi: str = Field(..., description="Hindi translation of question")
    options: List[str] = Field(default_factory=list, description="Preset choices for quick tap")
    input_type: str = Field(default="text", description="text | single_choice | date | number")


class IntakeRequest(BaseModel):
    query: str = Field(..., description="User's natural language problem statement")
    language: str = Field(default="en", description="'en' or 'hi'")
    answered_questions: Optional[Dict[str, str]] = Field(default=None, description="Previous question-answers")


class IntakeResponse(BaseModel):
    domain: str = Field(..., description="Detected legal domain: Tenant, Consumer, Criminal/Cyber, RTI, Labour, Other")
    confidence: float = Field(..., description="Classification confidence")
    summary_grade6_en: str = Field(..., description="Clear explanation in simple Grade 6 English")
    summary_grade6_hi: str = Field(..., description="Clear explanation in simple Grade 6 Hindi")
    clarifying_questions: List[IntakeClarifyingQuestion] = Field(
        ..., description="3 targeted clarifying questions"
    )
    is_complete: bool = Field(default=False, description="Whether all 3 questions have been answered")
    next_action: str = Field(default="answer_questions", description="Next UI step")


class RightsRequest(BaseModel):
    domain: str
    user_query: str
    answered_context: Dict[str, str] = Field(default_factory=dict)
    language: str = Field(default="en")


class LegalRightItem(BaseModel):
    right_en: str
    right_hi: str
    statute_2024: str
    description_en: str
    description_hi: str
    urgency_level: str  # high | medium | low


class RightsResponse(BaseModel):
    domain: str
    reading_level: str = "Grade 6"
    rights: List[LegalRightItem]
    concrete_timeline: str
    deadline_days: int
    zero_fir_eligible: bool
    free_aid_recommended: bool
    aid_contact: str = "Tele-Law 1516 / National Legal Services Authority (NALSA) Toll-Free 15100"
    compliance_2024: bool = True
    bns_citations: List[str]


class DocumentGenerateRequest(BaseModel):
    doc_type: str = Field(..., description="'legal_notice_tenant', 'consumer_complaint', 'rti_application', 'cyber_fraud_complaint'")
    applicant_name: str
    applicant_contact: str
    applicant_address: str
    opposite_party_name: str
    opposite_party_address: str
    incident_date: str
    disputed_amount: Optional[str] = None
    facts_description: str
    remedy_sought: str
    language: str = Field(default="en")


class DocumentGenerateResponse(BaseModel):
    doc_title: str
    doc_type: str
    generated_text: str
    statutes_cited: List[str]
    filing_instructions_en: List[str]
    filing_instructions_hi: List[str]
    tele_law_referral: str
    pdf_download_url: Optional[str] = None
    created_at: str


class CitationCheckRequest(BaseModel):
    text: str


class CitationCheckResponse(BaseModel):
    compliant_2024: bool
    repealed_laws_detected: List[str]
    statutes_applicable: List[str]
    verification_score: float
