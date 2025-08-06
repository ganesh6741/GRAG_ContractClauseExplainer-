# build_index.py

import joblib
import numpy as np
import faiss
from pathlib import Path

DATA_DIR   = Path(__file__).parent / "data"
EMBED_FILE = DATA_DIR / "embeddings.pkl"
INDEX_FILE = DATA_DIR / "faiss_index.idx"

def load_embeddings():
    data = joblib.load(str(EMBED_FILE))
    return data["clauses"], data["embeddings"]

def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)
    dim   = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index

def save_index(index: faiss.IndexFlatIP):
    Path(INDEX_FILE).parent.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_FILE))
    print(f"✅ FAISS index saved to {INDEX_FILE}")

if __name__ == "__main__":
    clauses, embeddings = load_embeddings()
    index = build_faiss_index(embeddings)
    save_index(index)