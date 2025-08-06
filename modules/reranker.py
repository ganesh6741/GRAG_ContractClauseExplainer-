from typing import List, Dict, Tuple
from sentence_transformers import CrossEncoder
from config import RERANKER_MODEL_NAME
import logging

# Configure logging to catch malformed inputs
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Load the cross-encoder once (adjust device if you have a GPU)
reranker = CrossEncoder(RERANKER_MODEL_NAME, device="cpu")


def rerank_clauses(
    query: str,
    retrieved_clauses: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """
    Takes a user query and a list of clauses (with key "clause_text"),
    scores them with the cross-encoder, and returns them sorted by descending score.
    """

    # Ensure the query is a proper string
    query_str = str(query)

    # Build (query, clause_text) pairs, validating types
    pairs: List[Tuple[str, str]] = []
    valid_clauses: List[Dict[str, str]] = []

    for idx, item in enumerate(retrieved_clauses):
        raw_clause = item.get("clause_text", "")
        clause_str = str(raw_clause) if raw_clause is not None else ""

        # Skip empty or non-string clause_texts
        if not clause_str:
            logger.warning(f"Skipping invalid clause_text at index {idx}: {raw_clause!r}")
            continue

        pairs.append((query_str, clause_str))
        valid_clauses.append(item)

    # If nothing valid to rerank, return the originals with a warning
    if not pairs:
        logger.warning("No valid clause-text pairs found; returning original list unmodified.")
        return retrieved_clauses

    # Predict relevance scores
    scores = reranker.predict(pairs, convert_to_numpy=True)

    # Attach scores to validated clauses
    for clause_item, score in zip(valid_clauses, scores):
        clause_item["rerank_score"] = float(score)

    # For any clauses skipped above, assign a very low score so they sort last
    for item in retrieved_clauses:
        if "rerank_score" not in item:
            item["rerank_score"] = float("-inf")

    # Return all clauses sorted by rerank_score descending
    return sorted(
        retrieved_clauses,
        key=lambda x: x["rerank_score"],
        reverse=True
    )