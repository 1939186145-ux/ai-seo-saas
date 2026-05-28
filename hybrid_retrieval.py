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

FAISS_FILE = os.path.join(
    VECTOR_DIR,
    "faiss.index"
)

CHUNK_FILE = os.path.join(
    VECTOR_DIR,
    "chunks.pkl"
)

# 自动创建目录
os.makedirs(VECTOR_DIR, exist_ok=True)


# =========================
# HYBRID SEARCH
# =========================
def hybrid_search(query, top_k=5):

    # =========================
    # 向量库不存在
    # =========================
    if not os.path.exists(CHUNK_FILE):
        return []

    if not os.path.exists(FAISS_FILE):
        return []

    # =========================
    # 加载 chunks
    # =========================
    try:

        with open(CHUNK_FILE, "rb") as f:
            chunks = pickle.load(f)

    except:
        return []

    if not chunks:
        return []

    # =========================
    # BM25
    # =========================
    tokenized_chunks = [
        list(jieba.cut(chunk))
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    bm25_scores = bm25.get_scores(
        list(jieba.cut(query))
    )

    # =========================
    # FAISS
    # =========================
    try:

        index = faiss.read_index(
            FAISS_FILE
        )

    except:
        return []

    # =========================
    # EMBEDDING
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
        return []

    # =========================
    # SEARCH
    # =========================
    try:

        scores, ids = index.search(
            query_embedding,
            top_k
        )

    except:
        return []

    # =========================
    # RESULTS
    # =========================
    results = []

    for idx in ids[0]:

        if idx < len(chunks):
            results.append(chunks[idx])

    return results
