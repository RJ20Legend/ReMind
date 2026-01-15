def priority(c):
    p = (1 - (c.memory_strength or 0))
    p *= (1 + (c.weakness_severity or 0))
    p *= (1 + (c.decay_rate or 0))
    p *= (c.interference_factor or 1)
    p *= (1 + (c.importance_level or 0))
    p *= (1 + (c.difficulty_level or 0))

    boosts = {
        "today": 3,
        "1 day": 2,
        "7 days": 1.4,
        "14 days": 1.1,
        "30 days": 0.6
    }

    window = (c.recommended_review_window or "7 days").lower()
    p *= boosts.get(window, 1.0)
    if getattr(c, 'episodic_replay_needed', False):
        p *= 1.5
    return p
