"""
Scheduler Engine: Chooses what to study next.
Simple priority algorithm that respects weakness and decay.
"""


def priority(concept):
    """
    Compute priority score for a concept.
    Higher score = study sooner.
    
    Factors:
    - Weakness (1 - memory_strength): forgetting things first
    - Decay rate: fast-decaying concepts need attention
    - Importance: user-defined importance weight
    """
    return (
        (1 - concept["memory_strength"])
        * (1 + concept["decay_rate"])
        * (1 + concept["importance_level"])
    )


def schedule(user_concepts):
    """
    Generate study plan: rank concepts by priority, assign review types.
    
    Args:
        user_concepts: dict of {concept_id: concept_state}
    
    Returns:
        List of top 5 concepts with review types and priorities
    """
    ranked = sorted(
        user_concepts.items(),
        key=lambda x: priority(x[1]),
        reverse=True
    )

    plan = []
    for cid, c in ranked[:5]:  # Top 5 for today
        # Assign review type based on memory strength
        if c["memory_strength"] < 0.3:
            t = "relearn"
        elif c["memory_strength"] < 0.6:
            t = "active recall"
        elif c["memory_strength"] < 0.8:
            t = "mixed recall"
        else:
            t = "quick check"

        plan.append({
            "concept_id": cid,
            "review_type": t,
            "priority": round(priority(c), 2)
        })

    return plan



