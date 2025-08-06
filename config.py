from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Embedding & Index Paths
CLAUSES_PATH = DATA_DIR / "clauses.txt"
EMBEDDING_PATH = DATA_DIR / "clause_embeddings.npy"
LOOKUP_PATH = DATA_DIR / "clause_lookup.json"
FAISS_INDEX_PATH = DATA_DIR / "faiss_index.idx"
EMBED_CACHE_PATH = DATA_DIR / "embeddings.pkl"
CLAUSE_TEXTS_PATH = DATA_DIR/ "clause_texts.pkl"
EXPLANATION_CACHE_PATH = "data/explanations.json"
FEEDBACK_PATH = BASE_DIR / "data" / "user_feedback.json"
CLAUSE_METADATA_PATH = BASE_DIR / "data" / "clause_metadata.json"
CLAUSE_LOOKUP_PATH      = DATA_DIR / "clause_lookup.json"
CLAUSE_METADATA_PATH    = DATA_DIR / "clause_metadata.json"
CLAUSE_EMBED_NPY        = DATA_DIR / "clause_embeddings.npy"
FAISS_INDEX_PATH        = DATA_DIR / "faiss_index.idx"
EXPLANATION_CACHE_PATH  = DATA_DIR / "explanations.json"
FEEDBACK_PATH           = DATA_DIR / "user_feedback.json"

# Model & API
EMBEDDING_MODEL = "multi-qa-MiniLM-L6-cos-v1"
LLM_MODEL = "sonar-pro"
PERPLEXITY_ENDPOINT = "https://api.perplexity.ai/chat/completions"

# Cross-encoder model for reranking FAISS results
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

