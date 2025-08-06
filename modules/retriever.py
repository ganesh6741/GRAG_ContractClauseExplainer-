from sentence_transformers import SentenceTransformer
from modules.embed_utils import load_embeddings, build_index, load_index,save_embeddings
from modules.knowledge_base import load_sample_clauses
from modules.utils import classify_clause_type

class ClauseRetriever:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.index = None
        self.clauses = []
        self.embeddings = None
        self.id_map = {}

    def build_index(self):
        self.clauses = load_sample_clauses()
        for clause in self.clauses:
            clause["clause_type"] = classify_clause_type(clause["clause_text"])
        texts = [c["clause_text"] for c in self.clauses]
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        self.index = build_index(embeddings)
        save_embeddings(embeddings, list(range(len(self.clauses))))
        save_clause_texts(self.clauses)
        self.id_map = {i: clause for i, clause in enumerate(self.clauses)}

    def load_index(self):
        self.index = load_index()
        self.clauses = load_clause_texts()
        ids, self.embeddings = load_embeddings()
        self.id_map = {i: self.clauses[i] for i in ids}

    def retrieve_similar(self, query_text, top_k=3, type_filter=None):
        query_vec = self.model.encode([query_text], normalize_embeddings=True)
        D, I = self.index.search(query_vec, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            clause = self.id_map[idx]
            if type_filter and clause.get("clause_type") != type_filter:
                continue
            clause["similarity"] = round(float(score), 4)
            results.append(clause)
        return results


