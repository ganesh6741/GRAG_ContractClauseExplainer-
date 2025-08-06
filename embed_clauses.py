# embed_clauses.py

import sys
from pathlib import Path
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer
from config import CLAUSES_PATH

DATA_DIR = Path("data")
INDEX_FILE = DATA_DIR / "faiss_index.idx"
LOOKUP_FILE = DATA_DIR / "clause_lookup.json"

def main():
    # Load clause texts
    clauses = [
        line.strip()
        for line in open(CLAUSES_PATH, "r", encoding="utf-8")
        if line.strip()
    ]

    # Embed clauses
    model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
    embeddings = model.encode(clauses, convert_to_numpy=True)
    faiss.normalize_L2(embeddings)

    # Build FAISS index
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_FILE))

    # Save clause lookup
    with open(LOOKUP_FILE, "w", encoding="utf-8") as f:
        json.dump({str(i): clause for i, clause in enumerate(clauses)}, f, indent=2)

    print(f"✅ Embedded {len(clauses)} clauses and saved index + lookup.")

if __name__ == "__main__":
    main()

