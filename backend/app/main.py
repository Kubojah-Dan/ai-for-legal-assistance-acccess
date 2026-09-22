from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.security import SecurityHeadersMiddleware, SlidingWindowRateLimitMiddleware
from app.routers import intake, rights, documents, escalation, compliance, kanoon, bns_matrix, tracker

app = FastAPI(
    title="NyayaMitra (न्यायमित्र) Legal Tech API",
    description="Accessible, Vernacular AI Legal Companion strictly grounded on 2024 Indian Law (BNS, BNSS, CPA 2019, RTI 2005)",
    version="2.0.0"
)

# 1. Custom Security Headers (CSP, X-Frame-Options, X-Content-Type-Options)
app.add_middleware(SecurityHeadersMiddleware)

# 2. Redis-backed Sliding Window Rate Limiter (30 requests/minute per client IP)
app.add_middleware(SlidingWindowRateLimitMiddleware, max_requests=settings.MAX_REQUESTS_PER_MINUTE, window_seconds=60)

# 3. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Include Routers
app.include_router(intake.router)
app.include_router(rights.router)
app.include_router(documents.router)
app.include_router(escalation.router)
app.include_router(compliance.router)
app.include_router(kanoon.router)
app.include_router(bns_matrix.router)
app.include_router(tracker.router)



@app.get("/api/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "NyayaMitra API",
        "version": "2.0.0",
        "legal_enforcement_year": settings.LEGAL_YEAR_ENFORCED,
        "repealed_ipc_blocked": settings.REJECT_REPEALED_IPC,
        "groq_models": {
            "small": settings.GROQ_MODEL_SMALL,
            "large": settings.GROQ_MODEL_LARGE
        },
        "accessibility_standard": "WCAG 2.1 AA Compliant"
    }
