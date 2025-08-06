import pandas as pd

def build_bulk_csv_data(retrieved_bulk):
    rows = []
    for enriched_set in retrieved_bulk:
        if not isinstance(enriched_set, list):
            continue
        for item in enriched_set:
            rows.append({
                "Input Clause": item.get("query_clause", ""),
                "Matched Clause": item.get("match_clause", ""),
                "Clause Type": item.get("clause_type", ""),
                "Risk": item.get("risk_flag", ""),
                "Similarity Score": item.get("similarity", ""),
                "Simplified Clause": item.get("simplified", ""),
                "Negotiation Tip": item.get("tip", "")
            })
    return pd.DataFrame(rows)

