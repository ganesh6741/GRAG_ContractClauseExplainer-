from typing import List, Dict
from sentence_transformers import CrossEncoder
from config import RERANKER_MODEL_NAME

# Load the cross-encoder once (adjust device if you have a GPU)
reranker = CrossEncoder(RERANKER_MODEL_NAME, device="cpu")

def rerank_clauses(
    query: str,
    retrieved_clauses: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """
    Takes a user query and a list of clauses (with key "clause_text"),
    scores them with the cross-encoder, and returns them sorted.
    """
    # Prepare pairs for the reranker
    pairs = [[query, item["clause_text"]] for item in retrieved_clauses]

    # Get relevance scores
    scores = reranker.predict(pairs, convert_to_numpy=True)

    # Attach and sort
    for item, score in zip(retrieved_clauses, scores):
        item["rerank_score"] = float(score)

    return sorted(
        retrieved_clauses,
        key=lambda x: x["rerank_score"],
        reverse=True
    )