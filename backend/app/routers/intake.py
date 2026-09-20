from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import IntakeRequest, IntakeResponse, IntakeClarifyingQuestion
from app.services.legal_service import legal_service

router = APIRouter(prefix="/api/intake", tags=["Intake"])


@router.post("", response_model=IntakeResponse)
async def process_intake(request: IntakeRequest):
    """
    Step 1: Samjho Mera Problem (Guided Intake)
    Takes citizen's natural language input in Hindi or English,
    classifies the legal dispute with sub-100ms small-to-large routing,
    and returns 3 focused clarifying questions.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    classification = await legal_service.classify_and_clarify(
        query=request.query,
        language=request.language
    )

    questions = [
        IntakeClarifyingQuestion(
            id=q.get("id", f"q_{idx}"),
            question_en=q.get("question_en", ""),
            question_hi=q.get("question_hi", ""),
            options=q.get("options", []),
            input_type=q.get("input_type", "single_choice")
        )
        for idx, q in enumerate(classification.get("questions", []))
    ]

    answered = request.answered_questions or {}
    is_complete = len(answered) >= 3

    return IntakeResponse(
        domain=classification.get("domain", "General Legal"),
        confidence=float(classification.get("confidence", 0.95)),
        summary_grade6_en=classification.get("summary_en", "Legal dispute identified."),
        summary_grade6_hi=classification.get("summary_hi", "कानूनी विवाद की पहचान की गई।"),
        clarifying_questions=questions,
        is_complete=is_complete,
        next_action="proceed_to_rights" if is_complete else "answer_questions"
    )
