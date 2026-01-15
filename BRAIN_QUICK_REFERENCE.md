# Quick Reference: Simplified Brain API

## The Core Loop (3 steps)

```python
from backend.brain import DEFAULT_STATE, users, process, schedule

# Step 1: Get or create user and concept state
if user_id not in users:
    users[user_id] = {}
user_concepts = users[user_id]

if concept_id not in user_concepts:
    user_concepts[concept_id] = DEFAULT_STATE.copy()

# Step 2: Update memory based on recall
state = user_concepts[concept_id]
result = process(state, {
    "correctness": "correct",      # or "wrong", "partial", etc.
    "response_time": 3.5,
    "hint_used": False,
    "failure_type": None,
    "transfer_flag": False,
    "fatigue_state": "normal"
})

# Step 3: Get study plan
study_plan = schedule(user_concepts)
```

## State Structure

```python
# 17 fields per concept
state = {
    "memory_strength": 0.6,                    # How well they know it (0-1)
    "last_revision_time": 0,                   # When they last studied (timestamp)
    "successful_recalls": 5,                   # Number of correct answers
    "failed_recalls": 2,                       # Number of wrong answers
    "avg_response_time": 3.5,                  # Average time in seconds
    "hint_usage_rate": 0.2,                    # Fraction of attempts with hints
    "difficulty_level": 0.5,                   # How hard (0-1)
    "cognitive_load": 0.5,                     # Current mental load
    "importance_level": 0.8,                   # How important (0-1)
    "decay_rate": 0.1,                         # How fast they forget
    "stability_factor": 1.0,                   # Memory consolidation
    "interference_factor": 1.0,                # Other concepts interfering
    "fatigue_modifier": 1.0,                   # Tiredness effect
    "reinforcement_gain": 0.2,                 # How much correct answers help
    "prediction_uncertainty": 0.15,            # Confidence bounds width
    "confidence_state": "Weak",                # Weak | Partial | Confident
    "review_window": "7 days"                  # Next review deadline
}
```

## Memory Engine Functions

### `process(state, payload)` - THE MAIN FUNCTION
Runs the full cognitive loop. Mutates `state` in place.

```python
result = process(state, {
    "correctness": "correct",      # "correct", "slow_correct", "partial", "wrong", "blank"
    "response_time": 3.5,
    "hint_used": False,
    "failure_type": None,
    "transfer_flag": False,
    "fatigue_state": "normal"      # "low", "normal", "high"
})

# Returns:
# {
#     "memory_strength": 0.68,
#     "confidence_state": "Partial",
#     "recommended_review_window": "7 days"
# }
```

### `decay(state)` - Apply forgetting
Reduces memory_strength based on time elapsed.

### `predict_range(state)` - Estimate performance
Returns (predicted, low, high) bounds of expected memory strength.

### `apply_recall(state, payload)` - Update memory
Increases memory if correct, decreases if wrong. Increments counters.

### `update_confidence(state)` - Set confidence level
"Weak" if strength < 0.4, "Partial" if < 0.8 with <3 successes, else "Confident".

### `review_window(state)` - Next review time
Returns "today" (m<0.3), "1 day" (m<0.5), "7 days" (m<0.7), "14 days" (m<0.85), or "30 days".

---

## Scheduler Functions

### `schedule(user_concepts)` - Generate study plan
Takes dict of {concept_id: state} and returns top 5 to study today.

```python
study_plan = schedule(user_concepts)

# Returns list of:
# [
#     {
#         "concept_id": "integration_by_parts",
#         "review_type": "active recall",      # relearn, active recall, mixed recall, quick check
#         "priority": 0.67                     # Higher = study sooner
#     },
#     ...
# ]
```

### `priority(concept)` - Compute priority score
Higher = study sooner.

Formula: `(1 - memory_strength) × (1 + decay_rate) × (1 + importance_level)`

---

## Review Types (by difficulty)

| Memory Strength | Type | Effort | Example |
|---|---|---|---|
| < 0.3 | relearn | High | Start from chapter 1 |
| 0.3-0.6 | active recall | Medium-High | Practice problems w/o hints |
| 0.6-0.8 | mixed recall | Medium | Some hints, some free recall |
| ≥ 0.8 | quick check | Low | Quick quiz or summary |

---

## Confidence States

| State | Memory Strength | Successful Recalls | Meaning |
|---|---|---|---|
| Weak | < 0.4 | Any | Still learning |
| Partial | 0.4-0.8 | < 3 | Getting there |
| Confident | ≥ 0.8 | ≥ 3 | Knows it well |

---

## Example: Full Flow

```python
# User submits an answer
user_id = "u1"
concept_id = "integration_by_parts"
correctness = "correct"
response_time = 3.5

# 1. Get state
user_concepts = users[user_id]
state = user_concepts[concept_id]

print(f"Before: strength={state['memory_strength']:.2f}, confidence={state['confidence_state']}")

# 2. Process recall
result = process(state, {
    "correctness": correctness,
    "response_time": response_time,
    "hint_used": False,
    "failure_type": None,
    "transfer_flag": False,
    "fatigue_state": "normal"
})

print(f"After: strength={result['memory_strength']:.2f}, confidence={result['confidence_state']}")
print(f"Review next in: {result['recommended_review_window']}")

# 3. Get study plan
study_plan = schedule(user_concepts)
print(f"Study plan for today:")
for item in study_plan:
    print(f"  - {item['concept_id']}: {item['review_type']} (priority {item['priority']:.2f})")
```

---

## Magic Numbers

| Parameter | Default | Meaning |
|---|---|---|
| λ (decay_rate) | 0.1 | How fast they forget (exponential) |
| σ (stability_factor) | 1.0 | Memory consolidation multiplier |
| ξ (interference_factor) | 1.0 | Effect of other concepts |
| reinforcement_gain | 0.2 | Percentage boost per correct answer |
| prediction_uncertainty | 0.15 | Bounds width (±15% of predicted) |

These are stored in each concept's state and adapt over time based on prediction errors.

---

## Debugging

### Check state structure
```python
from backend.brain import DEFAULT_STATE
print(DEFAULT_STATE.keys())  # Should be 17 keys
```

### Check event log
```python
from backend.brain import event_log
print(len(event_log))  # Should increase as recalls are submitted
```

### Trace a memory update
```python
state = DEFAULT_STATE.copy()
print(f"Initial: {state['memory_strength']:.2f}")

process(state, {"correctness": "correct", "response_time": 3.0, ...})
print(f"After correct: {state['memory_strength']:.2f}")

process(state, {"correctness": "wrong", "response_time": 10.0, ...})
print(f"After wrong: {state['memory_strength']:.2f}")
```

---

## Common Issues

**Q: Why did memory_strength decrease after a correct answer?**  
A: Decay is applied first (time-based), then reinforcement. If enough time has passed, decay > reinforcement.

**Q: How do I add a new user?**  
A: `users["new_user_id"] = {}` - they get concepts on first recall submission.

**Q: How do I add a new concept?**  
A: `users["u1"]["new_concept"] = DEFAULT_STATE.copy()` - gets default values.

**Q: Can I change magic numbers?**  
A: Yes! Edit the state dict directly. Each concept tracks its own decay_rate, etc.

---

## See Also

- `backend/brain/state.py` - State management
- `backend/brain/memory_engine.py` - Memory decay algorithms
- `backend/brain/scheduler_engine.py` - Scheduling algorithm
- `backend/routes/memory.py` - FastAPI endpoint
- `frontend/src/components/RecallInterface.js` - Frontend component
