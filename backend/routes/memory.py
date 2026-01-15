from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from brain import users, event_log, process, schedule

router = APIRouter(prefix="/memory")


class SubmitRecallPayload(BaseModel):
    """Recall submission from student."""
    user_id: str
    concept_id: str
    correctness: str  # "correct", "slow_correct", "partial", "wrong", "blank"
    response_time: float
    hint_used: bool = False
    failure_type: Optional[str] = None
    transfer_flag: bool = False
    fatigue_state: str = "normal"


@router.post("/submit-recall")
def submit_recall(payload: SubmitRecallPayload):
    """
    Cognitive loop core endpoint.
    
    1. Get user's memory state for concept
    2. Run memory engine (decay → predict → score → error → reinforce → window)
    3. Run scheduler (rank all concepts by priority)
    4. Return updated state + next study plan
    
    This is the brain stem.
    """
    
    # Validate user exists
    if payload.user_id not in users:
        users[payload.user_id] = {}
    
    user_concepts = users[payload.user_id]
    
    # Get or create memory state for this concept
    if payload.concept_id not in user_concepts:
        from ..brain import DEFAULT_STATE
        user_concepts[payload.concept_id] = DEFAULT_STATE.copy()
    
    concept_state = user_concepts[payload.concept_id]
    
    # Run memory engine: update memory based on this recall
    updated_state = process(concept_state, {
        "correctness": payload.correctness,
        "response_time": payload.response_time,
        "hint_used": payload.hint_used,
        "failure_type": payload.failure_type,
        "transfer_flag": payload.transfer_flag,
        "fatigue_state": payload.fatigue_state
    })
    
    # Store back
    user_concepts[payload.concept_id] = updated_state
    
    # Log the event
    event_log.append({
        "timestamp": None,  # Can add timestamp later
        "user_id": payload.user_id,
        "concept_id": payload.concept_id,
        "correctness": payload.correctness,
        "memory_strength": updated_state["memory_strength"],
        "confidence": updated_state["confidence_state"]
    })
    
    # Generate study plan: top 5 concepts to study next
    study_plan = schedule(user_concepts)
    
    # Return response
    return {
        "success": True,
        "updated_memory": {
            "concept_id": payload.concept_id,
            "memory_strength": round(updated_state["memory_strength"], 3),
            "confidence_state": updated_state["confidence_state"],
            "successful_recalls": updated_state["successful_recalls"],
            "failed_recalls": updated_state["failed_recalls"],
            "review_window": updated_state["review_window"]
        },
        "next_study_plan": study_plan
    }


@router.get("/user/{user_id}/concepts")
def get_user_concepts(user_id: str):
    """Get all concepts for a user with current memory states."""
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    concepts = users[user_id]
    return {
        "user_id": user_id,
        "concepts": [
            {
                "concept_id": cid,
                "memory_strength": c["memory_strength"],
                "confidence_state": c["confidence_state"],
                "review_window": c["review_window"],
                "successful_recalls": c["successful_recalls"],
                "failed_recalls": c["failed_recalls"]
            }
            for cid, c in concepts.items()
        ]
    }


@router.get("/events")
def get_event_log():
    """Get recent recall events."""
    return {
        "total_events": len(event_log),
        "recent_events": event_log[-50:]  # Last 50 events
    }

