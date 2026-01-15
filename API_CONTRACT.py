"""
API Contract: Simplified Brain Stem

This document specifies the exact input/output for all brain functions.
Copy-paste ready for integration.
"""

# ============================================================================
# STATE STRUCTURE
# ============================================================================

DEFAULT_STATE = {
    # Core memory metrics
    "memory_strength": 0.6,              # float [0, 1] - how well they know it
    "last_revision_time": 0,             # int - timestamp of last review (0 for untouched)
    "successful_recalls": 0,             # int - number of correct answers
    "failed_recalls": 0,                 # int - number of wrong answers
    
    # Decay parameters
    "decay_rate": 0.1,                   # float - how fast they forget (Ebbinghaus curve)
    "stability_factor": 1.0,             # float - memory consolidation
    "interference_factor": 1.0,          # float - other concepts interfering
    
    # Response characteristics
    "avg_response_time": 5.0,            # float - seconds
    "hint_usage_rate": 0.0,              # float [0, 1] - proportion of attempts with hints
    "difficulty_level": 0.5,             # float [0, 1] - intrinsic difficulty
    
    # State modifiers
    "cognitive_load": 0.5,               # float [0, 1] - mental load during review
    "fatigue_modifier": 1.0,             # float - fatigue effect multiplier
    "reinforcement_gain": 0.2,           # float - boost per correct answer
    
    # Model confidence
    "prediction_uncertainty": 0.15,      # float - uncertainty bounds width
    
    # Current state
    "confidence_state": "Weak",          # str: "Weak" | "Partial" | "Confident"
    "review_window": "7 days"            # str: "today" | "1 day" | "7 days" | "14 days" | "30 days"
}

# ============================================================================
# MEMORY ENGINE FUNCTIONS
# ============================================================================

def days_since(last: int) -> int:
    """
    Calculate days elapsed since last revision.
    
    Args:
        last: timestamp of last revision (0 = never revised)
    
    Returns:
        int: days elapsed (default 7 if last=0)
    
    Example:
        >>> days_since(0)
        7
        >>> days_since(int(datetime.now().timestamp()) - 86400)
        1
    """
    pass


def decay(state: dict) -> None:
    """
    Apply exponential decay to memory_strength.
    
    Physics: M(t) = M₀ * exp(-λ*σ*ξ*t)
        λ = decay_rate
        σ = stability_factor
        ξ = interference_factor
        t = days_since
    
    MUTATES: state["memory_strength"]
    
    Args:
        state: concept memory state dict
    
    Returns:
        None
    
    Example:
        >>> state = {"memory_strength": 0.8, "decay_rate": 0.1, ...}
        >>> decay(state)
        >>> state["memory_strength"]
        0.7234  # (decreased)
    """
    pass


def predict_range(state: dict) -> tuple:
    """
    Predict memory strength range with uncertainty bounds.
    
    Returns: (predicted, low, high)
    
    Args:
        state: concept memory state dict
    
    Returns:
        tuple: (predicted_strength, low_bound, high_bound)
    
    Example:
        >>> predicted, low, high = predict_range(state)
        >>> predicted
        0.72
        >>> low
        0.62
        >>> high
        0.82
    """
    pass


def apply_recall(state: dict, payload: dict) -> None:
    """
    Update memory_strength based on recall result.
    
    MUTATES:
        state["memory_strength"]
        state["successful_recalls"] or state["failed_recalls"]
        state["last_revision_time"]
    
    Args:
        state: concept memory state dict
        payload: dict with "correctness" key
    
    Returns:
        None
    
    Example:
        >>> apply_recall(state, {"correctness": "correct", ...})
        >>> state["memory_strength"]
        0.84  # (increased)
    """
    pass


def update_confidence(state: dict) -> None:
    """
    Update confidence_state based on memory_strength.
    
    Rules:
        "Confident" if strength >= 0.8 AND successful_recalls >= 3
        "Partial" if strength >= 0.4
        "Weak" otherwise
    
    MUTATES: state["confidence_state"]
    
    Args:
        state: concept memory state dict
    
    Returns:
        None
    
    Example:
        >>> update_confidence({"memory_strength": 0.85, "successful_recalls": 4, ...})
        >>> state["confidence_state"]
        "Confident"
    """
    pass


def review_window(state: dict) -> str:
    """
    Determine when the concept should be reviewed next.
    
    Rules:
        strength < 0.3  → "today"
        strength < 0.5  → "1 day"
        strength < 0.7  → "7 days"
        strength < 0.85 → "14 days"
        strength >= 0.85 → "30 days"
    
    Args:
        state: concept memory state dict
    
    Returns:
        str: "today" | "1 day" | "7 days" | "14 days" | "30 days"
    
    Example:
        >>> review_window({"memory_strength": 0.35, ...})
        "1 day"
    """
    pass


def process(state: dict, payload: dict) -> dict:
    """
    THE MAIN FUNCTION - Full cognitive loop pipeline.
    
    Pipeline:
        1. Apply decay (time-based forgetting)
        2. Predict expected performance ± uncertainty
        3. Score the answer (0.0-1.0)
        4. Detect prediction error
        5. Adapt model parameters (decay_rate, stability_factor)
        6. Reinforce memory (boost if correct, reduce if wrong)
        7. Update confidence state
        8. Compute next review window
    
    MUTATES: state dict (all fields may be modified)
    
    Args:
        state: concept memory state dict (will be modified)
        payload: dict with keys:
            "correctness" str: "correct" | "slow_correct" | "partial" | "wrong" | "blank"
            "response_time" float: seconds
            "hint_used" bool
            "failure_type" str or None
            "transfer_flag" bool
            "fatigue_state" str: "low" | "normal" | "high"
    
    Returns:
        dict with keys:
            "memory_strength" float: updated strength [0, 1]
            "confidence_state" str: "Weak" | "Partial" | "Confident"
            "recommended_review_window" str: next review deadline
    
    Example:
        >>> state = DEFAULT_STATE.copy()
        >>> result = process(state, {
        ...     "correctness": "correct",
        ...     "response_time": 3.5,
        ...     "hint_used": False,
        ...     "failure_type": None,
        ...     "transfer_flag": False,
        ...     "fatigue_state": "normal"
        ... })
        >>> result
        {
            "memory_strength": 0.72,
            "confidence_state": "Partial",
            "recommended_review_window": "7 days"
        }
    """
    pass


# ============================================================================
# SCHEDULER FUNCTIONS
# ============================================================================

def priority(concept: dict) -> float:
    """
    Compute priority score for a concept.
    
    Higher score = study sooner.
    
    Formula:
        score = (1 - memory_strength) × (1 + decay_rate) × (1 + importance_level)
    
    Factors:
        (1 - memory_strength): Study weak concepts first
        (1 + decay_rate): Fast-decaying concepts are prioritized
        (1 + importance_level): User-defined importance multiplier
    
    Args:
        concept: dict with keys "memory_strength", "decay_rate", "importance_level"
    
    Returns:
        float: priority score (typically 0.0-10.0, higher = study sooner)
    
    Example:
        >>> priority({"memory_strength": 0.2, "decay_rate": 0.15, "importance_level": 0.8})
        1.872
        
        >>> priority({"memory_strength": 0.9, "decay_rate": 0.05, "importance_level": 0.3})
        0.155  # High memory = low priority
    """
    pass


def schedule(user_concepts: dict) -> list:
    """
    Generate study plan: rank concepts by priority, assign review types.
    
    Args:
        user_concepts: dict of {concept_id: state_dict}
    
    Returns:
        list of dicts, each with keys:
            "concept_id" str
            "review_type" str: "relearn" | "active recall" | "mixed recall" | "quick check"
            "priority" float: rounded to 2 decimals
    
    Review type assignment rules:
        memory_strength < 0.3  → "relearn"
        memory_strength < 0.6  → "active recall"
        memory_strength < 0.8  → "mixed recall"
        memory_strength >= 0.8 → "quick check"
    
    Returns: Top 5 concepts sorted by priority (highest first)
    
    Example:
        >>> user_concepts = {
        ...     "concept_a": {"memory_strength": 0.2, "decay_rate": 0.1, "importance_level": 0.5},
        ...     "concept_b": {"memory_strength": 0.5, "decay_rate": 0.15, "importance_level": 0.8},
        ...     "concept_c": {"memory_strength": 0.9, "decay_rate": 0.05, "importance_level": 0.3}
        ... }
        >>> schedule(user_concepts)
        [
            {
                "concept_id": "concept_a",
                "review_type": "relearn",
                "priority": 1.45
            },
            {
                "concept_id": "concept_b",
                "review_type": "active recall",
                "priority": 0.99
            },
            {
                "concept_id": "concept_c",
                "review_type": "quick check",
                "priority": 0.15
            }
        ]
    """
    pass


# ============================================================================
# STATE MANAGEMENT
# ============================================================================

# Global dictionaries (in-memory)
users: dict = {}  # {user_id: {concept_id: state_dict}}
event_log: list = []  # List of recall events for debugging/replay


# ============================================================================
# EXAMPLE: FULL INTEGRATION
# ============================================================================

"""
from backend.brain import DEFAULT_STATE, users, event_log, process, schedule

# Step 1: Initialize user and concept if needed
user_id = "user123"
concept_id = "exponential_functions"

if user_id not in users:
    users[user_id] = {}

if concept_id not in users[user_id]:
    users[user_id][concept_id] = DEFAULT_STATE.copy()

# Step 2: User submits a recall
state = users[user_id][concept_id]

result = process(state, {
    "correctness": "correct",
    "response_time": 4.2,
    "hint_used": False,
    "failure_type": None,
    "transfer_flag": False,
    "fatigue_state": "normal"
})

print(f"Memory: {result['memory_strength']:.2f}")
print(f"Confidence: {result['confidence_state']}")
print(f"Next review: {result['recommended_review_window']}")

# Step 3: Generate study plan
study_plan = schedule(users[user_id])

print(f"Study plan for today:")
for item in study_plan:
    print(f"  - {item['concept_id']}: {item['review_type']} (priority {item['priority']})")

# Step 4: Log the event
event_log.append({
    "user_id": user_id,
    "concept_id": concept_id,
    "correctness": "correct",
    "memory_strength": result['memory_strength'],
    "confidence_state": result['confidence_state']
})

print(f"Total events: {len(event_log)}")
"""
