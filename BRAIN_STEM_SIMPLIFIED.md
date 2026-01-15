# Simplified Brain Stem Implementation

**Status:** ✅ COMPLETE - All three brain files refactored to simple, pragmatic design

## Architecture

The cognitive loop is now a clean, direct implementation using:
- **Simple dictionaries** for state (no classes)
- **Direct functions** that mutate state (no OOP)
- **In-memory storage** (no database)

## Files

### 1. `backend/brain/state.py` (38 lines)
**Purpose:** Holds runtime memory state for all users and concepts.

```python
DEFAULT_STATE = {
    "memory_strength": 0.6,           # 0-1 scale
    "last_revision_time": 0,          # timestamp
    "successful_recalls": 0,          # counter
    "failed_recalls": 0,              # counter
    "decay_rate": 0.1,                # how fast they forget
    "confidence_state": "Weak",       # Weak | Partial | Confident
    "review_window": "7 days",        # when to review next
    # ... 10 more fields for decay physics
}

users = {
    "u1": {
        "integration_by_parts": {...},  # One state dict per concept
        "arima": {...},
        "lstm": {...},
        "monte_carlo": {...}
    }
}

event_log = []  # Simple list for debugging/replay
```

**Key Features:**
- No classes, no dataclasses, no inheritance
- Direct dictionary mutations
- Initial user "u1" with 4 concepts pre-loaded

---

### 2. `backend/brain/memory_engine.py` (128 lines)
**Purpose:** Implements the memory decay model and recall feedback loop.

**Functions:**

| Function | Purpose |
|----------|---------|
| `days_since(last)` | Calculate days since last revision |
| `decay(state)` | Apply exponential decay: M(t) = M₀ * e^(-λ*σ*ξ*t) |
| `predict_range(state)` | Predict memory strength ± uncertainty bounds |
| `apply_recall(state, payload)` | Update memory based on answer correctness |
| `update_confidence(state)` | Set confidence level (Weak/Partial/Confident) |
| `review_window(state)` | Determine next review time (today/1 day/7 days/...) |
| `process(state, payload)` | **THE PIPELINE** - Full cognitive loop |

**The Memory Pipeline (process function):**

```
1. Apply decay:           M(t) = M₀ * e^(-λ*σ*ξ*t)
2. Predict range:         Expect certain performance ±uncertainty
3. Score the answer:      Convert "correct"/"wrong"/etc to 0.0-1.0
4. Detect errors:         Compare actual vs. predicted
5. Adapt parameters:      If wrong→increase decay, if right→decrease decay
6. Reinforce memory:      Increase M if correct, decrease if wrong
7. Update confidence:     Set "Weak"/"Partial"/"Confident"
8. Compute next window:   When should they review this again?
```

**Correctness Mapping:**
- `"correct"` → 1.0 (full credit)
- `"slow_correct"` → 0.8 (right but slow)
- `"partial"` → 0.5 (partial credit)
- `"wrong"` → 0.2 (wrong answer)
- `"blank"` → 0.0 (no answer)

---

### 3. `backend/brain/scheduler_engine.py` (62 lines)
**Purpose:** Ranks concepts by priority and generates study plan.

**Functions:**

| Function | Purpose |
|----------|---------|
| `priority(concept)` | Compute priority score (0 = study later, high = study now) |
| `schedule(user_concepts)` | Return top 5 concepts ranked by priority |

**Priority Formula:**
```
score = (1 - memory_strength) × (1 + decay_rate) × (1 + importance_level)
```

**Review Types:**
- `memory_strength < 0.3` → "relearn" (start from scratch)
- `0.3-0.6` → "active recall" (harder retrieval practice)
- `0.6-0.8` → "mixed recall" (combination of easy/hard)
- `≥0.8` → "quick check" (just verify, minimal effort)

---

### 4. `backend/brain/__init__.py` (28 lines)
**Purpose:** Export the public API.

```python
# State
DEFAULT_STATE, users, event_log

# Memory functions
process, decay, predict_range, apply_recall, update_confidence, review_window

# Scheduler functions
schedule, priority
```

---

### 5. `backend/routes/memory.py` (120 lines)
**Purpose:** FastAPI endpoint that ties everything together.

**Endpoint:** `POST /submit-recall`

```python
@router.post("/submit-recall")
def submit_recall(payload: SubmitRecallPayload):
    """
    The brain stem endpoint.
    
    1. Get or create user and concept state
    2. Call process() to update memory
    3. Call schedule() to generate study plan
    4. Return updated state + next 5 concepts to study
    """
    # ... implementation
```

**Payload:**
```json
{
    "user_id": "u1",
    "concept_id": "integration_by_parts",
    "correctness": "correct",
    "response_time": 3.5,
    "hint_used": false,
    "failure_type": null,
    "transfer_flag": false,
    "fatigue_state": "normal"
}
```

**Response:**
```json
{
    "success": true,
    "updated_memory": {
        "concept_id": "integration_by_parts",
        "memory_strength": 0.72,
        "confidence_state": "Partial",
        "successful_recalls": 1,
        "failed_recalls": 0,
        "review_window": "7 days"
    },
    "next_study_plan": [
        {
            "concept_id": "lstm",
            "review_type": "active recall",
            "priority": 0.67
        },
        // ... top 4 more concepts
    ]
}
```

---

## Why This Design?

### ✅ **Advantages of Simplicity**

| Old (OOP) | New (Functional) |
|-----------|-----------------|
| 256 lines of SchedulerEngine class | 62 lines of functions |
| 301 lines of MemoryEngine class | 128 lines of functions |
| 176 lines of dataclass definitions | 38 lines of dicts |
| Complex inheritance and threading locks | Direct dict mutations |
| Hard to debug | Easy to trace through |
| Requires understanding class hierarchy | Read top-to-bottom |

### 🎯 **What We Kept**

- ✅ Exponential memory decay model (physics-based)
- ✅ Adaptive reinforcement (learning from prediction errors)
- ✅ Confidence tracking
- ✅ Spaced repetition scheduling
- ✅ In-memory state management
- ✅ Event logging for replay/analysis

### 🚀 **What We Removed**

- ❌ Complex dataclass definitions
- ❌ Class methods and static methods
- ❌ Inheritance and mixins
- ❌ Threading locks
- ❌ Estimated time calculations
- ❌ Session metrics computation
- ❌ Dynamic plan rebalancing

**Result:** Same cognitive science, 60% less code, 10x easier to understand and modify.

---

## Testing

Run `python test_simplified_brain.py` to verify:
- ✅ All imports work
- ✅ DEFAULT_STATE has correct structure
- ✅ User "u1" has 4 concepts
- ✅ Memory engine process() function works
- ✅ Scheduler priority() and schedule() work
- ✅ Event log structure is ready

---

## Integration with Frontend

The `RecallInterface.js` component calls `POST /submit-recall` with the same payload structure. No changes needed to frontend.

---

## Next Steps (Phase 5)

- [ ] Add PostgreSQL database persistence
- [ ] Add user authentication
- [ ] Add more sophisticated error recovery
- [ ] Add analytics dashboard
- [ ] Deploy to production
