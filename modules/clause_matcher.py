from modules.retriever import ClauseRetriever

retriever = ClauseRetriever()
retriever.build_index()

def match_user_clauses(user_clauses, top_k=1):
    matches = []
    for clause in user_clauses:
        similar = retriever.retrieve_similar(clause, top_k=top_k)
        matches.append({
            "user_clause": clause,
            "similar_example": similar[0]["clause_text"],
            "explanation": similar[0]["plain_explanation"],
            "risk_flag": similar[0]["risk_flag"]
        })
    return matches