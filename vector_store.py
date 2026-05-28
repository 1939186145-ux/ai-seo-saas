import os
import pickle
import faiss
import numpy as np

VECTOR_DIR = "vector_db"

FAISS_FILE = os.path.join(VECTOR_DIR, "faiss.index")
CHUNK_FILE = os.path.join(VECTOR_DIR, "chunks.pkl")

os.makedirs(VECTOR_DIR, exist_ok=True)


# =========================
# 保存向量库（V10稳定版）
# =========================
def save_faiss(chunks, embeddings):

    # =========================
    # 防空
    # =========================
    if not chunks or embeddings is None:
        return False

    try:
        embeddings = np.array(embeddings, dtype="float32")

        # 空数组保护
        if embeddings.ndim != 2 or len(embeddings) == 0:
            return False

        dim = embeddings.shape[1]

        # FAISS index
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        # 保存 index
        faiss.write_index(index, FAISS_FILE)

        # 保存 chunks
        with open(CHUNK_FILE, "wb") as f:
            pickle.dump(chunks, f)

        return True

    except Exception as e:
        print("[vector_store] save_faiss error:", e)
        return False


# =========================
# 加载向量库（V10稳定版）
# =========================
def load_faiss():

    # =========================
    # 文件不存在直接降级
    # =========================
    if not os.path.exists(FAISS_FILE):
        return None, []

    if not os.path.exists(CHUNK_FILE):
        return None, []

    try:
        index = faiss.read_index(FAISS_FILE)

        with open(CHUNK_FILE, "rb") as f:
            chunks = pickle.load(f)

        # 防止数据不一致
        if len(chunks) == 0:
            return None, []

        return index, chunks

    except Exception as e:
        print("[vector_store] load_faiss error:", e)
        return None, []