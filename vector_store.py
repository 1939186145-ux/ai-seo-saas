import faiss
import numpy as np
import pickle
import os

def save_faiss(chunks, embeddings):

    if not os.path.exists("vector_db"):
        os.makedirs("vector_db")

    embeddings_np = np.array(
        embeddings,
        dtype="float32"
    )

    dim = embeddings_np.shape[1]

    index = faiss.IndexFlatL2(dim)

    index.add(embeddings_np)

    faiss.write_index(
        index,
        "vector_db/faiss.index"
    )

    with open(
        "vector_db/chunks.pkl",
        "wb"
    ) as f:

        pickle.dump(chunks, f)

    print("FAISS 保存成功")