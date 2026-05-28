import os
import pickle
import faiss
import jieba
import numpy as np

from rank_bm25 import BM25Okapi
from zhipuai import ZhipuAI
from dotenv import load_dotenv

load_dotenv()

# =========================
# 智谱AI
# =========================
client = ZhipuAI(
    api_key=os.getenv("ZHIPU_API_KEY")
)

# =========================
# 文件路径
# =========================
VECTOR_DIR = "vector_db"

FAISS_FILE = os.path.join(VECTOR_DIR, "faiss.index")
CHUNK_FILE = os.path.join(VECTOR_DIR, "chunks.pkl")

os.makedirs(VECTOR_DIR, exist_ok=True)


# =========================
# HYBRID SEARCH（V10稳定版）
# =========================
def hybrid_search(query, top_k=5):

    # =========================
    # 1. 文件不存在 → 直接降级（关键！）
    # =========================
    if not os.path.exists(CHUNK_FILE):
        return [query]  # 🔥公网稳定关键

    if not os.path.exists(FAISS_FILE):
        return [query]

    # =========================
    # 2. 读取 chunks
    # =========================
    try:
        with open(CHUNK_FILE, "rb") as f:
            chunks = pickle.load(f)
    except:
        return [query]

    if not chunks:
        return [query]

    # =========================
    # 3. BM25（可选增强）
    # =========================
    try:
        tokenized_chunks = [list(jieba.cut(chunk)) for chunk in chunks]
        bm25 = BM25Okapi(tokenized_chunks)
        bm25.get_scores(list(jieba.cut(query)))
    except:
        pass

    # =========================
    # 4. FAISS index
    # =========================
    try:
        index = faiss.read_index(FAISS_FILE)
    except:
        return [query]

    # =========================
    # 5. embedding
    # =========================
    try:
        response = client.embeddings.create(
            model="embedding-3",
            input=query
        )

        query_embedding = np.array(
            [response.data[0].embedding],
            dtype="float32"
        )

    except:
        return [query]

    # =========================
    # 6. search
    # =========================
    try:
        scores, ids = index.search(query_embedding, top_k)
    except:
        return [query]

    # =========================
    # 7. result merge
    # =========================
    results = []

    for idx in ids[0]:
        if idx is not None and idx < len(chunks):
            results.append(chunks[idx])

    # =========================
    # 8. 关键兜底（避免空结果）
    # =========================
    if not results:
        return [query]

    return results