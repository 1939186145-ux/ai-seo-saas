# hybrid_retrieval.py（Render稳定版）

import numpy as np

def simple_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def hybrid_search(query_embedding, stored_embeddings, chunks, top_k=5):
    """
    替代 BM25 + FAISS 的轻量检索
    """

    if stored_embeddings is None or len(stored_embeddings) == 0:
        return []

    scores = []

    for i, emb in enumerate(stored_embeddings):
        score = simple_similarity(query_embedding, emb)
        scores.append((score, chunks[i]))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [c for _, c in scores[:top_k]]