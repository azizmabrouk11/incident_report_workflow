from pinecone import Pinecone
import os

def query_similar(vector: list[float], top_k: int = 5):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX"))
    return index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )
