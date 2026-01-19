from pydantic import BaseModel
from typing import List, Optional

class SimilarityRequest(BaseModel):
    text: str
    top_k: Optional[int] = 5
    min_score: Optional[float] = 0.8

class SimilarIncident(BaseModel):
    mongodb_id: str
    score: float
    text: str

class SimilarityResponse(BaseModel):
    matches: List[SimilarIncident]
