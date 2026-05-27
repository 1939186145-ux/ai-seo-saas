import numpy as np

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def hybrid_search(query_embedding, stored_embeddings, chunks, top_k=5):

    if stored_embeddings is None or len(stored_embeddings) == 0:
        return []

    scores = []

    for i, emb in enumerate(stored_embeddings):
        score = cosine(query_embedding, emb)
        scores.append((score, chunks[i]))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [x[1] for x in scores[:top_k]]