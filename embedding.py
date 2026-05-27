from zhipuai import ZhipuAI
from dotenv import load_dotenv
import os

load_dotenv()

client = ZhipuAI(
    api_key=os.getenv("ZHIPU_API_KEY")
)

def embed_chunks(chunks):

    embeddings = []

    for chunk in chunks:

        response = client.embeddings.create(
            model="embedding-3",
            input=chunk
        )

        embeddings.append(
            response.data[0].embedding
        )

    return embeddings