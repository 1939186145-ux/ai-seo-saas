from rank_bm25 import BM25Okapi
import jieba
import pickle
import faiss
import numpy as np

from zhipuai import ZhipuAI
from dotenv import load_dotenv
import os

load_dotenv()

client = ZhipuAI(
    api_key=os.getenv("ZHIPU_API_KEY")
)

def hybrid_search(query, top_k=5):

    with open(
        "vector_db/chunks.pkl",
        "rb"
    ) as f:
        chunks = pickle.load(f)

    tokenized_chunks = [
        list(jieba.cut(chunk))
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    bm25_scores = bm25.get_scores(
        list(jieba.cut(query))
    )

    index = faiss.read_index(
        "vector_db/faiss.index"
    )

    response = client.embeddings.create(
        model="embedding-3",
        input=query
    )

    query_embedding = np.array(
        [response.data[0].embedding],
        dtype="float32"
    )

    scores, ids = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in ids[0]:

        if idx < len(chunks):

            results.append(chunks[idx])

    return results