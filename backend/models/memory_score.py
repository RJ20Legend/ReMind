from pydantic import BaseModel

class MemoryScore(BaseModel):
    concept_id: int
    user_id: int
    score: float
    last_reviewed: str
