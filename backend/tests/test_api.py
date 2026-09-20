import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.utils.bns_mapping import validate_citations


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["legal_enforcement_year"] == 2024
        assert data["repealed_ipc_blocked"] is True


@pytest.mark.asyncio
async def test_intake_tenant_issue():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "query": "My landlord in Pune is threatening to evict me within 2 days and cut my electricity because of security deposit dispute.",
            "language": "en"
        }
        response = await ac.post("/api/intake", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "Tenant" in data["domain"]
        assert len(data["clarifying_questions"]) == 3
        assert data["confidence"] > 0.85


@pytest.mark.asyncio
async def test_intake_cyber_fraud():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "query": "I received a fake SMS and ₹45,000 was debited from my bank via fraudulent UPI transaction today.",
            "language": "hi"
        }
        response = await ac.post("/api/intake", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "Cyber" in data["domain"] or "Fraud" in data["domain"]
        assert len(data["clarifying_questions"]) == 3


@pytest.mark.asyncio
async def test_rights_bns_compliance():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "domain": "Tenant & Housing Dispute",
            "user_query": "Landlord withholding deposit and giving oral eviction notice",
            "answered_context": {
                "agreement_status": "Yes, Registered Agreement",
                "notice_served": "No notice given",
                "deposit_amount": "50000"
            },
            "language": "en"
        }
        response = await ac.post("/api/rights", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["compliance_2024"] is True
        assert data["reading_level"] == "Grade 6"
        assert len(data["rights"]) >= 2
        # Verify BNS citations are included, not IPC
        for cite in data["bns_citations"]:
            assert "IPC" not in cite
            assert ("BNS" in cite or "Tenancy" in cite or "BNSS" in cite)


@pytest.mark.asyncio
async def test_rights_cyber_zero_fir():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "domain": "Cyber Crime & Financial Fraud",
            "user_query": "Online financial fraud via fake app",
            "answered_context": {},
            "language": "en"
        }
        response = await ac.post("/api/rights", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["zero_fir_eligible"] is True
        assert any("173(1) BNSS" in c for c in data["bns_citations"])


@pytest.mark.asyncio
async def test_document_generation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "doc_type": "legal_notice_tenant",
            "applicant_name": "Ramesh Kumar",
            "applicant_contact": "+91 9876543210",
            "applicant_address": "Flat 302, Green Valley Apartments, Pune, Maharashtra 411001",
            "opposite_party_name": "Suresh Sharma (Landlord)",
            "opposite_party_address": "Bungalow 12, Model Colony, Pune 411016",
            "incident_date": "2026-09-10",
            "disputed_amount": "60,000",
            "facts_description": "The tenant paid all rents promptly. The landlord is refusing to return the security deposit and threatens illegal eviction without 30 days notice.",
            "remedy_sought": "Immediate refund of Rs 60,000 security deposit with 18% interest and cessation of eviction threats.",
            "language": "en"
        }
        response = await ac.post("/api/documents/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "RAMESH KUMAR" in data["generated_text"].upper()
        assert "SURESH SHARMA" in data["generated_text"].upper()
        assert len(data["statutes_cited"]) > 0
        assert "IPC" not in data["generated_text"]


@pytest.mark.asyncio
async def test_pdf_download():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "doc_type": "legal_notice_tenant",
            "applicant_name": "Ramesh Kumar",
            "applicant_contact": "+91 9876543210",
            "applicant_address": "Pune, Maharashtra",
            "opposite_party_name": "Suresh Sharma",
            "opposite_party_address": "Pune, Maharashtra",
            "incident_date": "2026-09-10",
            "facts_description": "Illegal eviction notice without 30 days statutory notice.",
            "remedy_sought": "Refund deposit and cease harassment."
        }
        response = await ac.post("/api/documents/download-pdf", json=payload)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.content.startswith(b"%PDF")


@pytest.mark.asyncio
async def test_escalation_resources():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/escalation/resources")
        assert response.status_code == 200
        resources = response.json()
        assert len(resources) >= 4
        # Tele-law 1516 and NALSA 15100 must be present
        phones = [r["phone"] for r in resources]
        assert "1516" in phones
        assert "15100" in phones


@pytest.mark.asyncio
async def test_citation_verifier_rejects_ipc():
    """Validates 0-Hallucination requirement against repealed laws."""
    # Test text containing repealed IPC
    bad_text = "This offence is punishable under Section 420 IPC and Section 506 Indian Penal Code."
    result_bad = validate_citations(bad_text)
    assert result_bad["compliant_2024"] is False
    assert len(result_bad["repealed_laws_detected"]) > 0

    # Test text using 2024 BNS
    good_text = "This offence is punishable under Section 318 BNS 2023 and Section 351 BNS 2023."
    result_good = validate_citations(good_text)
    assert result_good["compliant_2024"] is True
    assert len(result_good["repealed_laws_detected"]) == 0
