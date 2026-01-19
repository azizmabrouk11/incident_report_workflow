from fastapi import FastAPI
from dotenv import load_dotenv
from .embedding import embed_text
from .pinecone_client import query_similar
from .schemas import SimilarityRequest, SimilarityResponse

load_dotenv()

app = FastAPI(title="Incident Similarity Service")

@app.post("/similar-incidents", response_model=SimilarityResponse)
def find_similar_incidents(payload: SimilarityRequest):
    embedding = embed_text(payload.text)

    results = query_similar(
        vector=embedding,
        top_k=payload.top_k
    )

    matches = []
    for match in results["matches"]:
        if match["score"] >= payload.min_score:
            matches.append({
                "mongodb_id": match["metadata"].get("mongodb_id"),
                "score": match["score"],
                "text": match["metadata"].get("text")
            })

    return {"matches": matches}
