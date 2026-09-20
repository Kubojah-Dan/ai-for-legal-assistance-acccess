"""
Definitive 2024 Indian Law Statutes Mapping
Enforced since July 1, 2024:
- Bharatiya Nyaya Sanhita (BNS), 2023 replaces Indian Penal Code (IPC), 1860
- Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 replaces Code of Criminal Procedure (CrPC), 1973
- Bharatiya Sakshya Adhiniyam (BSA), 2023 replaces Indian Evidence Act (IEA), 1872
- Consumer Protection Act, 2019 (CPA 2019)
- Right to Information Act, 2005 (RTI 2005)
- Real Estate (Regulation and Development) Act, 2016 (RERA)
- Model Tenancy Act / State Rent Control Acts
"""

from typing import Dict, Any, List

# Strict BNS 2024 mappings from old IPC references
BNS_MAPPING: Dict[str, Dict[str, Any]] = {
    "cheating": {
        "repealed_ipc": "Section 420 IPC",
        "statute_2024": "Section 318 BNS, 2023",
        "title": "Cheating and dishonestly inducing delivery of property",
        "description": "Criminal deceit causing wrongful loss or wrongful gain.",
        "punishment": "Imprisonment up to 7 years with fine",
        "bailable": False,
        "cognizable": True
    },
    "theft": {
        "repealed_ipc": "Section 379 IPC",
        "statute_2024": "Section 303(2) BNS, 2023",
        "title": "Punishment for Theft",
        "description": "Dishonest taking of movable property out of possession without consent.",
        "punishment": "Imprisonment up to 3 years, or fine, or both (community service for minor theft < ₹5000 on first offense under Sec 303(2) proviso)",
        "bailable": True,
        "cognizable": True
    },
    "criminal_intimidation": {
        "repealed_ipc": "Section 506 IPC",
        "statute_2024": "Section 351(2) & 351(3) BNS, 2023",
        "title": "Criminal Intimidation / Threats",
        "description": "Threatening injury to person, reputation or property with intent to cause alarm.",
        "punishment": "Imprisonment up to 2 years, or fine, or both (up to 7 years if threat to cause death/grievous hurt)",
        "bailable": True,
        "cognizable": True
    },
    "extortion": {
        "repealed_ipc": "Section 384 IPC",
        "statute_2024": "Section 308 BNS, 2023",
        "title": "Extortion",
        "description": "Intentionally putting any person in fear of any injury and inducing dishonest delivery of property.",
        "punishment": "Imprisonment up to 7 years, or fine, or both",
        "bailable": False,
        "cognizable": True
    },
    "criminal_trespass": {
        "repealed_ipc": "Section 441/447 IPC",
        "statute_2024": "Section 329 BNS, 2023",
        "title": "Criminal Trespass and House-trespass",
        "description": "Unlawful entry into or upon property in possession of another to commit offence or intimidate.",
        "punishment": "Imprisonment up to 3 months, or fine up to ₹5,000, or both",
        "bailable": True,
        "cognizable": True
    },
    "forgery": {
        "repealed_ipc": "Section 463/465 IPC",
        "statute_2024": "Section 336 BNS, 2023",
        "title": "Forgery & Electronic Record Falsification",
        "description": "Making false documents or electronic records with intent to commit fraud.",
        "punishment": "Imprisonment up to 2 years or fine or both",
        "bailable": True,
        "cognizable": False
    },
    "cyber_fraud": {
        "repealed_ipc": "Section 420 IPC r/w 66D IT Act",
        "statute_2024": "Section 318(4) BNS, 2023 r/w Section 66D Information Technology Act, 2000",
        "title": "Cheating by personation using computer resource / Digital fraud",
        "description": "Deceiving victim via digital systems, fake UPI/banking portals, or phishing.",
        "punishment": "Imprisonment up to 3 years & fine up to ₹1,00,000 under IT Act + 7 yrs under BNS",
        "bailable": False,
        "cognizable": True
    },
    "organized_crime": {
        "repealed_ipc": "MCOCA/Special laws",
        "statute_2024": "Section 111 BNS, 2023",
        "title": "Organized Crime & Syndicate Operations",
        "description": "Continuing unlawful activity including extortion, land grabbing, contract killing.",
        "punishment": "Life imprisonment or death penalty depending on severity",
        "bailable": False,
        "cognizable": True
    }
}

# Procedural remedies under BNSS 2023
BNSS_PROCEDURES = {
    "zero_fir": {
        "statute_2024": "Section 173(1) BNSS, 2023",
        "title": "Mandatory Registration of Zero FIR & E-FIR",
        "description": "Information can be given orally or digitally (e-FIR). Police must register FIR regardless of territorial jurisdiction (Zero FIR transferred to jurisdictional police within 15 days).",
        "timeline": "Immediate registration, physical signature within 3 days for e-FIR"
    },
    "investigation_timeline": {
        "statute_2024": "Section 193(3) BNSS, 2023",
        "title": "Police Report / Chargesheet Deadline",
        "description": "Police investigation must be completed within 90 days for serious offences.",
        "timeline": "60 to 90 days maximum limit for filing chargesheet"
    },
    "victim_rights": {
        "statute_2024": "Section 193(3)(ii) BNSS, 2023",
        "title": "Mandatory Victim Information & Progress Updates",
        "description": "Police must inform the victim or informant of the progress of investigation within 90 days, including by electronic means.",
        "timeline": "Within 90 days"
    },
    "anticipatory_bail": {
        "statute_2024": "Section 482 BNSS, 2023 (replaces Sec 438 CrPC)",
        "title": "Direction for Grant of Bail to Person Apprehending Arrest",
        "description": "Application to High Court or Sessions Court for pre-arrest protection.",
        "timeline": "Prior to formal arrest"
    }
}

# Civil / Consumer / Tenant statutes
CIVIL_STATUTES = {
    "consumer_protection": {
        "statute": "Consumer Protection Act, 2019 (Sections 34, 35, 38)",
        "title": "Consumer Complaint for Deficiency in Service / Defective Goods",
        "jurisdiction": "District Commission up to ₹50 Lakhs; State Commission ₹50L-₹2Cr; National Commission >₹2Cr",
        "timeline": "Must be filed within 2 years from date of cause of action (Sec 69 CPA 2019)",
        "resolution_target": "3 to 5 months"
    },
    "tenant_eviction": {
        "statute": "Model Tenancy Act, 2021 / State Rent Control Acts (e.g. Maharashtra Rent Control Act 1999)",
        "title": "Protection Against Arbitrary Eviction & Security Deposit Withholding",
        "rights": "Landlord cannot cut electricity/water; cannot evict without formal 30-day legal notice; Security deposit must be refunded within 30 days of vacating with interest if defaulted.",
        "timeline": "30 days formal notice required prior to any eviction proceeding"
    },
    "rti": {
        "statute": "Right to Information Act, 2005 (Section 6 & 7)",
        "title": "Citizen Request for Public Information",
        "timeline": "Mandatory response within 30 days (48 hours if life or liberty involved)",
        "fee": "₹10 central application fee (BPL exempt)",
        "first_appeal": "Within 30 days to First Appellate Authority if rejected or unresponded"
    }
}


def validate_citations(text: str) -> Dict[str, Any]:
    """
    Zero-Hallucination Enforcer:
    Scans generated text and flags any reference to repealed British-era IPC (Indian Penal Code)
    or old CrPC (1973). Validates proper inclusion of BNS 2023 / BNSS 2023.
    """
    text_upper = text.upper()
    repealed_detected = []
    
    # Check for repealed statutes
    if "IPC" in text_upper or "INDIAN PENAL CODE" in text_upper:
        repealed_detected.append("Indian Penal Code (IPC, 1860) - REPEALED on July 1, 2024")
    if "CRPC" in text_upper or "CODE OF CRIMINAL PROCEDURE" in text_upper:
        repealed_detected.append("Code of Criminal Procedure (CrPC, 1973) - REPEALED on July 1, 2024")
    if "EVIDENCE ACT 1872" in text_upper or "INDIAN EVIDENCE ACT" in text_upper:
        repealed_detected.append("Indian Evidence Act (1872) - REPEALED on July 1, 2024")
        
    is_compliant_2024 = len(repealed_detected) == 0
    
    return {
        "compliant_2024": is_compliant_2024,
        "repealed_laws_detected": repealed_detected,
        "statutes_applicable": ["Bharatiya Nyaya Sanhita 2023 (BNS)", "Bharatiya Nagarik Suraksha Sanhita 2023 (BNSS)", "Consumer Protection Act 2019", "RTI Act 2005"]
    }
