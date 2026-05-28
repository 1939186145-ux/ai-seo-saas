```python
import os
import pickle
import faiss
import numpy as np

VECTOR_DIR = "vector_db"

FAISS_FILE = os.path.join(VECTOR_DIR, "faiss.index")
CHUNK_FILE = os.path.join(VECTOR_DIR, "chunks.pkl")

# 自动创建目录
os.makedirs(VECTOR_DIR, exist_ok=True)


# =========================
# 保存向量库
# =========================
def save_faiss(chunks, embeddings):

    if not chunks or embeddings is None:
        return

    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    # 保存索引
    faiss.write_index(index, FAISS_FILE)

    # 保存文本块
    with open(CHUNK_FILE, "wb") as f:
        pickle.dump(chunks, f)


# =========================
# 加载向量库
# =========================
def load_faiss():

    # 文件不存在
    if not os.path.exists(FAISS_FILE):
        return None, []

    if not os.path.exists(CHUNK_FILE):
        return None, []

    try:

        index = faiss.read_index(FAISS_FILE)

        with open(CHUNK_FILE, "rb") as f:
            chunks = pickle.load(f)

        return index, chunks

    except:
        return None, []
