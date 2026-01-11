from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str
    email: str
    enrolled_concepts: List[int] = []
