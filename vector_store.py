# vector_store.py（Render稳定版）

import numpy as np

# =========================
# 简易内存向量库（替代FAISS）
# =========================

_VECTOR_DB = {
    "embeddings": None,
    "chunks": None
}


def save_faiss(chunks, embeddings):
    """
    保存向量（替代 FAISS）
    """
    _VECTOR_DB["chunks"] = chunks
    _VECTOR_DB["embeddings"] = np.array(embeddings)
    return True


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def hybrid_search(query_embedding, top_k=5):
    """
    简化检索（替代 FAISS search）
    """
    if _VECTOR_DB["embeddings"] is None:
        return []

    scores = []

    for i, emb in enumerate(_VECTOR_DB["embeddings"]):
        score = cosine_similarity(query_embedding, emb)
        scores.append((score, _VECTOR_DB["chunks"][i]))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [text for _, text in scores[:top_k]]