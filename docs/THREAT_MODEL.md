# NyayaMitra Threat Model & Security Posture

## 1. System Overview & Trust Boundaries
NyayaMitra processes sensitive citizen legal inquiries regarding tenant disputes, domestic situations, criminal complaints, and financial cyber frauds. Because users may input personally identifiable information (PII) or dispute records, strict trust boundaries are established:

```
[User Browser / Screen Reader]
       │
       ▼ (HTTPS / TLS 1.3 + Strict CSP)
[Rate Limiting & Security Headers Middleware]
       │
       ▼ (IP Filter + Sliding Window 30 req/min)
[FastAPI / Hono Routing Layer]
       │
       ├──► [Llama 8B Classification Service (Sub-100ms)]
       ├──► [Llama 70B Statutory Drafting Service (2024 BNS/BNSS Grounding)]
       └──► [Client-side PDF Exporter (Zero Database Persistence)]
```

## 2. Threat Analysis (STRIDE Model)

| Threat Category | Potential Risk | Mitigation in NyayaMitra |
| :--- | :--- | :--- |
| **Spoofing** | Fraudulent requests masquerading as legitimate users to drain LLM tokens | Sliding-window IP rate limiting (Upstash Redis / Memory) strictly caps bursts to 30 req/min per IP. |
| **Tampering** | Man-in-the-middle alteration of generated legal notices or citations | Full HTTPS enforcement, cryptographic SHA256 integrity checks, and deterministic statutory validation against BNS/BNSS 2024. |
| **Repudiation** | Lack of traceability regarding generated notices | Time-stamped statutory draft generation with unique client reference tokens. |
| **Information Disclosure** | Leakage of citizen queries or landlord/tenant PII | Zero database persistence of raw queries. Inquiries are processed transiently in memory. No logging of user PII. |
| **Denial of Service** | DDoS attack flooding the Groq inference endpoints | Two-tier routing: Small Llama 8B absorbs high-volume intake; Large 70B only triggers for formal drafting upon 3 answered questions. |
| **Elevation of Privilege** | Code injection via natural language prompt | Strict Pydantic input models, sanitization of user strings before PDF generation, and no execution of dynamic code. |

## 3. Defense-in-Depth Security Headers
- `Content-Security-Policy`: Restricts script and asset execution to vetted CDNs.
- `X-Frame-Options: DENY`: Prevents clickjacking attacks.
- `X-Content-Type-Options: nosniff`: Prevents MIME-type confusion attacks.
- `Permissions-Policy: microphone=(self)`: Restricts Web Speech audio access exclusively to the active origin.
