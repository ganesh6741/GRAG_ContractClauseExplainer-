# File: modules/embed_utils.py

import joblib
import pickle
import numpy as np
import faiss
from pathlib import Path
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
from config import (
    DATA_DIR, CLAUSE_TEXTS_PATH, EMBED_CACHE_PATH,
    EMBEDDING_MODEL, FAISS_INDEX_PATH
)

# 1. Model loader
def load_model(model_name: str = None):
    name = model_name or EMBEDDING_MODEL
    return SentenceTransformer(name)

def encode_clauses(clauses, model=None, batch_size=32):
    model = model or load_model()
    all_embeddings = []

    # create batches of clauses
    batches = [
        clauses[i : i + batch_size]
        for i in range(0, len(clauses), batch_size)
    ]

    # tqdm description can include total clauses, batch size, etc.
    for batch in tqdm(batches, desc="Encoding clauses", unit="batch"):
        embs = model.encode(batch, convert_to_numpy=True)
        all_embeddings.append(embs)

    # stack into one big numpy array
    return np.vstack(all_embeddings)

import pickle
from pathlib import Path

def save_embeddings(clauses, embeddings, cache_path=None):
    cache_path = cache_path or (Path(__file__).parent.parent / "data" / "embeddings.pkl")
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    # make sure to open in 'wb'!
    with open(cache_path, "wb") as f:
        pickle.dump((clauses, embeddings), f)


def load_embeddings():
    data = joblib.load(EMBED_CACHE_PATH)
    return data["clauses"], data["embeddings"]

# 3. FAISS index builder + loader
def build_index(embeddings: np.ndarray):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    Path(FAISS_INDEX_PATH).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    return index

def load_index():
    return faiss.read_index(str(FAISS_INDEX_PATH))

