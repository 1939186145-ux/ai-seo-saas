import pickle
import os
import numpy as np
import jieba
import faiss
from rank_bm25 import BM25Okapi

VECTOR_DIR = "vector_db"

class V11Engine:

    def __init__(self):
        self.chunks = []
        self.bm25 = None
        self.index = None
        self._load()

    def _load(self):
        faiss_path = os.path.join(VECTOR_DIR, "faiss.index")
        chunk_path = os.path.join(VECTOR_DIR, "chunks.pkl")

        if not os.path.exists(chunk_path):
            return

        with open(chunk_path, "rb") as f:
            self.chunks = pickle.load(f)

        tokenized = [list(jieba.cut(c)) for c in self.chunks]
        self.bm25 = BM25Okapi(tokenized)

        if os.path.exists(faiss_path):
            self.index = faiss.read_index(faiss_path)

    # =========================
    # 快速检索（V11优化）
    # =========================
    def search(self, query, top_k=5):

        if not self.chunks:
            return []

        try:
            bm25_scores = self.bm25.get_scores(list(jieba.cut(query)))
        except:
            bm25_scores = []

        try:
            if self.index:
                return self._faiss_search(query, top_k)
        except:
            pass

        return self.chunks[:top_k]

    def _faiss_search(self, query, top_k):

        from zhipuai import ZhipuAI
        import os

        client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))

        resp = client.embeddings.create(
            model="embedding-3",
            input=query
        )

        emb = np.array([resp.data[0].embedding], dtype="float32")

        scores, ids = self.index.search(emb, top_k)

        return [self.chunks[i] for i in ids[0] if i < len(self.chunks)]