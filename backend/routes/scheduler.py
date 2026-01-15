from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.memory import ConceptMemory
from backend.agents.scheduler import priority

router = APIRouter(prefix="/scheduler")


@router.get("/plan")
def plan(db: Session = Depends(get_db)):
    concepts = db.query(ConceptMemory).all()

    scored = [(c, priority(c)) for c in concepts]
    scored.sort(key=lambda x: x[1], reverse=True)

    plan = []
    for c, p in scored:
        if len(plan) >= 8:
            break
        plan.append({
            "concept_id": c.concept_id,
            "priority": p,
            "review_type": "relearn" if (c.memory_strength or 0) < 0.3 else "active recall"
        })

    return plan
