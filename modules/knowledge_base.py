def load_sample_clauses():
    return [
        {
            "clause_text": "Either party may terminate this agreement with 30 days’ notice.",
            "clause_type": "Termination",
            "contract_type": "NDA",
            "plain_explanation": "Either side can end the agreement with 30 days' notice.",
            "risk_flag": "✅ Safe",
        },
        {
            "clause_text": "Employee shall not disclose proprietary information indefinitely.",
            "clause_type": "Confidentiality",
            "contract_type": "Employment",
            "plain_explanation": "The employee must never share company secrets.",
            "risk_flag": "⚠️ Indefinite obligation",
        }
    ]