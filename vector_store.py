# vector_store.py（Render稳定版）

import numpy as np

# 简单内存向量库（替代FAISS）
VECTOR_DB = {
    "chunks": [],
    "vectors": []
}

def save_faiss(chunks, embeddings):
    """
    用内存方式存储向量（替代FAISS）
    """
    VECTOR_DB["chunks"] = chunks
    VECTOR_DB["vectors"] = np.array(embeddings)

    print("向量库保存成功（内存版）")


def load_vectors():
    return VECTOR_DB


def search(query_vector, top_k=5):
    """
    简单余弦相似度搜索
    """
    if len(VECTOR_DB["vectors"]) == 0:
        return []

    vectors = VECTOR_DB["vectors"]

    scores = np.dot(vectors, query_vector) / (
        np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_vector)
    )

    top_idx = np.argsort(scores)[::-1][:top_k]

    return [VECTOR_DB["chunks"][i] for i in top_idx]