import faiss
import pickle
from sentence_transformers import SentenceTransformer

DATA_DIR = "ContractClauseExplainer/data"
INDEX_PATH = f"{DATA_DIR}/faiss_index.idx"
TEXT_PATH = f"{DATA_DIR}/clause_texts.pkl"

def load_index():
    return faiss.read_index(INDEX_PATH)

def load_clause_texts():
    with open(TEXT_PATH, "rb") as f:
        return pickle.load(f)

def embed_query(query, model):
    return model.encode(query, normalize_embeddings=True)

def search_clauses(query, k=5):
    model = SentenceTransformer('multi-qa-MiniLM-cos-v1')
    index = load_index()
    clause_texts = load_clause_texts()

    query_embedding = embed_query(query, model)
    D, I = index.search(query_embedding.reshape(1, -1), k)
    return [clause_texts[i] for i in I[0]]