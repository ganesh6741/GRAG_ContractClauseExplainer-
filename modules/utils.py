def classify_clause_type(clause_text: str) -> str:
    clause = clause_text.lower()
    if any(kw in clause for kw in ["terminate", "termination", "cancel"]):
        return "Termination"
    elif any(kw in clause for kw in ["confidential", "non-disclosure", "privacy"]):
        return "Confidentiality"
    elif any(kw in clause for kw in ["payment", "fee", "charge", "compensation"]):
        return "Payment"
    elif any(kw in clause for kw in ["dispute", "arbitration", "jurisdiction", "governing law"]):
        return "Dispute Resolution"
    else:
        return "Other"

import hashlib

def clause_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

# def classify_clause_type(clause_text: str) -> str:
#     clause = clause_text.lower()
#     if any(kw in clause for kw in ["terminate", "termination", "cancel"]):
#         return "Termination"
#     elif any(kw in clause for kw in ["confidential", "non-disclosure", "privacy"]):
#         return "Confidentiality"
#     elif any(kw in clause for kw in ["payment", "fee", "charge", "compensation"]):
#         return "Payment"
#     elif any(kw in clause for kw in ["dispute", "arbitration", "jurisdiction", "governing law"]):
#         return "Dispute Resolution"
#     else:
#         return "Other"