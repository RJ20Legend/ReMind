from pydantic import BaseModel

class Concept(BaseModel):
    id: int
    title: str
    topic: str
    difficulty: float = 1.0
