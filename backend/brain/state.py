"""
Simple in-memory state management for the cognitive loop.
Living brain: holds runtime memory state for all users and concepts.
"""

from datetime import datetime

# Default state template for any new concept
DEFAULT_STATE = {
    "memory_strength": 0.6,
    "last_revision_time": 0,  # day 0
    "successful_recalls": 0,
    "failed_recalls": 0,
    "avg_response_time": 5.0,
    "hint_usage_rate": 0.0,
    "difficulty_level": 0.5,
    "cognitive_load": 0.5,
    "importance_level": 0.5,
    "decay_rate": 0.1,
    "stability_factor": 1.0,
    "interference_factor": 1.0,
    "fatigue_modifier": 1.0,
    "reinforcement_gain": 0.2,
    "prediction_uncertainty": 0.15,
    "confidence_state": "Weak",
    "review_window": "7 days"
}

# The living brain: all user memory states
users = {
    "u1": {
        "integration_by_parts": DEFAULT_STATE.copy(),
        "arima": DEFAULT_STATE.copy(),
        "lstm": DEFAULT_STATE.copy(),
        "monte_carlo": DEFAULT_STATE.copy()
    }
}

# Event log for debugging and replay
event_log = []
