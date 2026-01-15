"""
Memory Engine: Forgetting + learning brain.
Direct functions that mutate state based on physics of memory.
"""

import math
from datetime import datetime


def days_since(last):
    """Calculate days elapsed since last revision."""
    if last == 0:
        return 7  # First exposure default
    return (datetime.now() - last).days


def decay(state):
    """Apply exponential decay to memory strength."""
    d = days_since(state["last_revision_time"])
    state["memory_strength"] *= math.exp(
        -state["decay_rate"]
        * state["stability_factor"]
        * state["interference_factor"]
        * d
    )


def predict_range(state):
    """Predict memory strength range with uncertainty bounds."""
    d = days_since(state["last_revision_time"])
    predicted = state["memory_strength"] * math.exp(-state["decay_rate"] * d)
    u = state["prediction_uncertainty"] * state["interference_factor"] * state["fatigue_modifier"]
    return predicted, predicted - u, predicted + u


def apply_recall(state, payload):
    """Update memory strength based on recall result."""
    correctness = payload["correctness"]

    if correctness in ["correct", "slow_correct"]:
        state["memory_strength"] += (1 - state["memory_strength"]) * state["reinforcement_gain"]
        state["successful_recalls"] += 1
    else:
        penalty = 0.7 if correctness == "wrong" else 0.5
        state["memory_strength"] *= penalty
        state["failed_recalls"] += 1

    state["last_revision_time"] = datetime.now()


def update_confidence(state):
    """Update confidence level based on memory strength."""
    if state["memory_strength"] >= 0.8 and state["successful_recalls"] >= 3:
        state["confidence_state"] = "Confident"
    elif state["memory_strength"] >= 0.4:
        state["confidence_state"] = "Partial"
    else:
        state["confidence_state"] = "Weak"


def review_window(state):
    """Determine when the concept should be reviewed next."""
    m = state["memory_strength"]
    if m < 0.3:
        return "today"
    if m < 0.5:
        return "1 day"
    if m < 0.7:
        return "7 days"
    if m < 0.85:
        return "14 days"
    return "30 days"


def process(state, payload):
    """
    Full pipeline: decay → predict → score → error detection → reinforce → confidence → window.
    This is the heart of the cognitive loop.
    """
    # Apply decay from time since last review
    decay(state)
    
    # Predict what we expect vs. what actually happened
    predicted, low, high = predict_range(state)

    # Score the answer
    score_map = {
        "correct": 1.0,
        "slow_correct": 0.8,
        "partial": 0.5,
        "wrong": 0.2,
        "blank": 0.0
    }
    actual = score_map.get(payload["correctness"], 0.0)
    error = 0

    # Detect prediction error
    if actual < low:
        error = actual - low  # Worse than expected
    if actual > high:
        error = actual - high  # Better than expected

    # Adapt model parameters based on prediction error
    severity = abs(error)

    if error < 0:
        # Actual worse than predicted: increase decay
        state["decay_rate"] *= (1 + severity)
        state["reinforcement_gain"] *= (1 - 0.5 * severity)
    else:
        # Actual better than predicted: decrease decay, increase stability
        state["decay_rate"] *= (1 - 0.7 * severity)
        state["stability_factor"] *= (1 + 0.4 * severity)

    # Apply the recall result
    apply_recall(state, payload)
    
    # Update confidence and next review window
    update_confidence(state)
    next_window = review_window(state)
    state["review_window"] = next_window

    return {
        "memory_strength": state["memory_strength"],
        "confidence_state": state["confidence_state"],
        "recommended_review_window": next_window
    }
