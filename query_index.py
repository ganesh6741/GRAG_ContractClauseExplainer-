import json
import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer

DATA_DIR    = "data"
INDEX_FILE  = f"{DATA_DIR}/faiss_index.idx"
LOOKUP_FILE = f"{DATA_DIR}/clause_lookup.json"
MODEL_NAME  = "multi-qa-MiniLM-L6-cos-v1"

@st.cache_resource(show_spinner=False)
def load_resources():
    """
    Load FAISS index, clause lookup, and embedding model.
    """
    index = faiss.read_index(INDEX_FILE)

    with open(LOOKUP_FILE, "r", encoding="utf-8") as f:
        clause_lookup = json.load(f)

    model = SentenceTransformer(MODEL_NAME)
    return index, clause_lookup, model

def query_index(question: str, k: int = 5):
    index, clause_lookup, model = load_resources()

    # Embed and normalize query
    q_vec = model.encode([question], convert_to_numpy=True)
    faiss.normalize_L2(q_vec)

    # Search index
    scores, idxs = index.search(q_vec, k)
    results = []
    for score, idx in zip(scores[0], idxs[0]):
        try:
            clause = clause_lookup[idx]
        except IndexError:
            clause = "[Clause not found]"
        results.append({
            "clause": clause,
            "score": float(score)
        })
    return results


if __name__ == "__main__":
    q = "What is the termination notice period?"
    top_clauses = query_index(q, k=3)
    for i, hit in enumerate(top_clauses, start=1):
        print(f"{i}. [score={hit['score']:.3f}] {hit['clause']}\n")