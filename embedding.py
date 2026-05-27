import requests
import os

GLM_API_KEY = os.getenv("GLM_API_KEY")

def embed_chunks(chunks):
    embeddings = []

    for text in chunks:
        res = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/embeddings",
            headers={
                "Authorization": f"Bearer {GLM_API_KEY}"
            },
            json={
                "model": "embedding-3",
                "input": text
            }
        )

        data = res.json()

        try:
            emb = data["data"][0]["embedding"]
        except:
            emb = [0.0] * 1024

        embeddings.append(emb)

    return embeddings