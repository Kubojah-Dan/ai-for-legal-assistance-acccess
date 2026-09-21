# NyayaMitra (न्यायमित्र) - AI Legal Companion for India

[![2024 Legal Alignment](https://img.shields.io/badge/Legal%20Framework-BNS%20%26%20BNSS%202024-emerald.svg)](docs/COMPLIANCE.md)
[![Accessibility](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA%20Compliant-blue.svg)](frontend/public/accessibility/statement.html)
[![Hallucinations](https://img.shields.io/badge/Hallucinations-0%2F50%20Repealed%20Laws%20Detected-brightgreen.svg)](backend/evals/legal_queries.json)
[![Evaluation Benchmark](https://img.shields.io/badge/Evaluation%20Score-100%2F100-success.svg)](docs/COMPLIANCE.md)
[![License](https://img.shields.io/badge/License-MIT%20Public%20Legal%20Tech-purple.svg)](LICENSE)

> **Mission**: Over 5.2 crore cases are pending in Indian courts. Average citizens cannot afford ₹5,000 advocate consultation fees to understand simple tenant notices or digital banking fraud. On July 1, 2024, India's criminal justice system underwent its biggest transformation in a century (IPC replaced by BNS, CrPC by BNSS). NyayaMitra is an accessible, vernacular AI legal companion built to provide immediate legal clarity, know-your-rights guidance at a Grade 6 reading level, and generate ready-to-file legal documents for free.

---

## 🏛️ 3-Step Legal Pipeline

```
1. Samjho Mera Problem ──► 2. Mere Adhikaar ──────► 3. Mera Document
   (Guided Intake)             (Know Your Rights)         (Document Generation)
   • Speak or type (Hi/En)     • Grounded in 2024 BNS     • Ready-to-file Notice/RTI
   • 3 clarifying questions    • Grade 6 reading level    • Downloadable PDF
   • Sub-100ms Llama 8B        • Concrete deadline bar    • Tele-Law 1516 referral
```

1. **Samjho Mera Problem (Guided Intake)**: Instead of confusing, open-ended chatbots, NyayaMitra takes voice or text input in Hindi or English and prompts the citizen with exactly 3 clarifying questions.
2. **Mere Adhikaar (Know My Rights)**: Strictly grounded on 2024 Indian Law (Bharatiya Nyaya Sanhita - BNS, Bharatiya Nagarik Suraksha Sanhita - BNSS, and Consumer Protection Act 2019). Translates statutes into Grade 6 plain language and provides concrete timeline bars (e.g. 15-day notice period, 24-hr golden window for 1930 reporting).
3. **Mera Document (Document Generation)**: Generates a ready-to-file legal document (Tenant Notice against illegal eviction/deposit withholding, Zero-FIR Cyber Complaint, Consumer Dispute Notice, or RTI Application) in PDF and text formats, accompanied by Tele-Law (1516) and NALSA (15100) escalation paths.

---

## 🏗️ Architecture & Technology Stack

```mermaid
graph TD
    User["Citizen / Screen Reader User<br/>(Hindi / English / Voice / Keyboard)"] -->|HTTPS / TLS 1.3| Gateway["NyayaMitra Security Layer<br/>(CSP, X-Frame-Options, Rate Limiter)"]
    
    subgraph Frontend ["Accessible Frontend (WCAG 2.1 AA)"]
        Gateway --> Tabs["WAI-ARIA Tab Navigation<br/>role='tablist' / role='tabpanel'"]
        Tabs --> IntakeUI["Step 1: Samjho Mera Problem<br/>Web Speech Voice Input + Explicit htmlFor Labels"]
        Tabs --> RightsUI["Step 2: Mere Adhikaar<br/>Grade 6 Plain Language + Timeline Bar"]
        Tabs --> DocUI["Step 3: Mera Document<br/>Notice / Complaint / RTI Form"]
        Tabs --> EvalsUI["Step 4: 2024 Audit<br/>Live Citation Inspector & Benchmark Score"]
        LiveAnnouncer["ARIA Live Region<br/>aria-live='polite'"] -.-> User
    end

    subgraph Backend ["FastAPI / Cloudflare Edge Engine"]
        IntakeUI -->|JSON Request| IntakeRouter["/api/intake<br/>Classification & 3 Clarifying Questions"]
        RightsUI -->|Context Data| RightsRouter["/api/rights<br/>2024 Statutes & Zero-FIR Verification"]
        DocUI -->|Draft Form| DocRouter["/api/documents/generate<br/>Statutory Legal Notice Generator"]
        DocUI -->|Direct Stream| PDFEngine["/api/documents/download-pdf<br/>ReportLab PDF Engine"]
        EvalsUI -->|Validation Query| ComplianceRouter["/api/compliance/verify-citations<br/>Repealed Law Detector"]
    end

    subgraph Intelligence ["Small-to-Large AI Intelligence"]
        IntakeRouter -->|Sub-100ms Routing| SmallLLM["Groq Llama 3.1 8B Instant<br/>Rapid Domain Categorization"]
        DocRouter -->|High-Precision Drafting| LargeLLM["Groq Llama 3.3 70B Versatile<br/>Formal Legal Drafting"]
    end

    subgraph LegalCorpus ["2024 Indian Law Grounding (Zero Hallucinations)"]
        RightsRouter --> BNS["Bharatiya Nyaya Sanhita (BNS) 2023<br/>(Replaces IPC 1860)"]
        RightsRouter --> BNSS["Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023<br/>(Mandatory Zero FIR Sec 173)"]
        RightsRouter --> CPA["Consumer Protection Act 2019<br/>(e-Daakhil Online Filing)"]
        RightsRouter --> TeleLaw["Legal Services Authorities Act 1987<br/>(Tele-Law 1516 / NALSA 15100 Escalation)"]
    end
```

### Stack Components
- **Frontend**: Vite + TypeScript + Semantic HTML5 + Tailwind CSS + Web Speech API (speech recognition) + Accessible ARIA components.
- **Backend**: FastAPI (Python 3.11+) + Hono Cloudflare Edge Engine + Pydantic v2 schemas.
- **AI / LLM**: Groq Cloud API using small-to-large routing (`llama-3.1-8b-instant` for sub-100ms intake categorization; `llama-3.3-70b-versatile` for statutory drafting).
- **Security & Caching**: Upstash Redis sliding-window rate limiting (30 requests/min per IP) + strict Content Security Policy + X-Frame-Options: DENY.
- **Testing**: 100% Pytest suite + 50 legal evaluation query scenarios in `backend/evals/legal_queries.json`.
- **Accessibility**: Strict WCAG 2.1 Level AA conformance, full keyboard navigation, `aria-live="polite"` dynamic announcements, and static declaration at `frontend/public/accessibility/statement.html`.

---

## ⚡ Quick Start & Local Setup

### 1. Backend (FastAPI) — Windows PowerShell

Install Python 3.11+ from [python.org](https://www.python.org/downloads/windows/) and select **Add Python to PATH** during setup. Then restart PowerShell and run. If `python` is still not recognised, use the installed interpreter explicitly once: `& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m venv .venv`.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
pytest tests/ -v
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend / Cloudflare Pages App

```powershell
cd frontend
npm ci
npm run typecheck
npm run build676s
npx wrangler pages dev dist --ip 0.0.0.0 --port 3000
```

The Vite development server proxies `/api` requests to `http://127.0.0.1:8000`, so keep the backend running in a separate terminal. No API key is required for a local smoke test: the backend uses deterministic legal-data fallbacks when `GROQ_API_KEY` is empty.

## Deployment: Render API + Vercel Frontend

1. Push this repository to GitHub. The included `render.yaml` can create the backend service automatically, or create a Render **Web Service** manually with root directory `backend`, build command `pip install -r requirements.txt`, start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, and health check path `/api/health`.
2. In Render, set `ENVIRONMENT=production`, `LEGAL_YEAR_ENFORCED=2024`, `REJECT_REPEALED_IPC=true`, and `MAX_REQUESTS_PER_MINUTE=30`. Set `GROQ_API_KEY` only when you want live Groq responses. `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`, `SUPABASE_URL`, and `SUPABASE_KEY` are optional for the current application and must remain server-side secrets.
3. Deploy the frontend in Vercel: import the same repository, set **Root Directory** to `frontend`, and accept the Vite build command `npm run build` and output directory `dist`.
4. Copy the resulting Render URL, for example `https://nyaya-mitra-api.onrender.com`. In Vercel add `VITE_API_BASE_URL` with that URL (no trailing slash) for Production, Preview, and Development, then redeploy. Vite exposes only `VITE_` variables to browser code, so never put API keys in Vercel frontend variables.
5. Copy the Vercel production URL, then set Render `CORS_ORIGINS` to a JSON list such as `["https://your-project.vercel.app"]`. Add custom domains to the same list if you use them, then redeploy Render.

---

## ⚖️ Legal Grounding & Free Aid Helplines
NyayaMitra is not a substitute for an advocate in active court litigation, but serves as a free citizen aid companion. For representation:
- **Tele-Law (Department of Justice)**: Dial **1516** (Free legal aid across 100,000+ Common Service Centres).
- **National Legal Services Authority (NALSA)**: Dial **15100** (Free advocates for women, workers, and citizens earning <₹3L/yr).
- **National Cyber Crime Helpline**: Dial **1930** (24-hour golden window reporting for unauthorized fund transfers).
- **National Consumer Helpline**: Dial **1915** or file online via [edaakhil.nic.in](https://edaakhil.nic.in).
