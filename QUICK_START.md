# Quick Start: Testing the Cognitive Loop

## 1. Start the Backend

```bash
cd backend
python -m uvicorn app:app --reload --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

## 2. Test the API with cURL

### Test 1: Submit a CORRECT answer

```bash
curl -X POST http://localhost:8000/memory/submit-recall \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u1",
    "concept_id": "integration_by_parts",
    "correctness": "instant_correct",
    "response_time": 4.2,
    "hint_used": false,
    "failure_type": null,
    "transfer_flag": false,
    "fatigue_state": "normal"
  }'
```

**Expected Response:**
- ✅ `success: true`
- Memory strength should INCREASE
- Confidence level should be "Solid" or higher
- Next review window: "14 days" or "30 days"

### Test 2: Submit a WRONG answer

```bash
curl -X POST http://localhost:8000/memory/submit-recall \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u1",
    "concept_id": "integration_by_parts",
    "correctness": "incorrect",
    "response_time": 8.5,
    "hint_used": true,
    "failure_type": "wrong",
    "transfer_flag": false,
    "fatigue_state": "high"
  }'
```

**Expected Response:**
- ✅ `success: true`
- Memory strength should DECREASE
- Confidence level should drop to "Weak" or "Emerging"
- Next review window: "today" or "1 day"
- Hint penalty should reduce score

### Test 3: Check the Study Plan

```bash
# After submitting a few recalls, check what's next
curl -X POST http://localhost:8000/memory/submit-recall \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u1",
    "concept_id": "partial_fractions",
    "correctness": "slow_correct",
    "response_time": 6.1,
    "hint_used": false,
    "failure_type": null,
    "transfer_flag": false,
    "fatigue_state": "normal"
  }'
```

**Expected in Response:**
- `study_plan.next_concept` should show a different concept
- `study_plan.total_concepts` should be ~15
- Priorities should reflect overdue concepts first

## 3. Python: Inspect the Cognitive State

```python
from backend.brain import cognitive_state, MemoryEngine

# Check all concepts for user u1
concepts = cognitive_state.get_all_concepts_for_user("u1")
print(f"Total concepts: {len(concepts)}\n")

for concept in sorted(concepts, key=lambda x: x.memory_strength, reverse=True):
    half_life = MemoryEngine.half_life(
        concept.decay_rate,
        concept.stability_factor,
        concept.interference_factor
    )
    print(f"{concept.concept_id}:")
    print(f"  Memory: {concept.memory_strength:.2%}")
    print(f"  Confidence: {concept.confidence_level}")
    print(f"  Half-life: {half_life:.1f} days")
    print(f"  Next review: {concept.recommended_review_window}")
    print(f"  Successful/Failed: {concept.successful_recalls}/{concept.failed_recalls}")
    print()

# View event log
print("\nEvent Log:")
for event in cognitive_state.event_log[-5:]:  # Last 5 events
    print(f"[{event['timestamp']}] {event['event_type']}")
    print(f"  User: {event['user_id']}, Concept: {event['concept_id']}")
    print(f"  Data: {event['data']}")
    print()
```

## 4. Frontend: Start a Recall Session

```bash
cd frontend
npm run dev
```

Navigate to http://localhost:3000/dashboard

Click the big **🧠 Start Recall Session** button:
- Read the question
- Type your answer
- Click "Show Hint" if needed
- Click "✓ Submit Answer"
- **Watch memory strength update in real-time** ✨
- **See confidence level change**
- **Check next review window**

## 5. Verify the Cognitive Loop Works

### Scenario A: Improve by getting it right multiple times
1. Submit "correct" for "integration_by_parts"
   - Memory: 0.30 → 0.38 ✅
   - Confidence: Weak → Emerging
2. Wait (mentally - just submit again)
3. Submit "correct" again
   - Memory: 0.38 → 0.48 ✅
   - Confidence: Emerging → Solid
4. Watch the priority drop (less urgent)

### Scenario B: Forget by getting it wrong
1. User u1 has "calculus_derivatives" at memory=0.75
2. Submit "incorrect" for it
   - Memory: 0.75 → 0.38 (50% penalty) ❌
   - Confidence: Solid → Emerging
   - Next review: "today" (high priority again)

### Scenario C: Watch the Scheduler reorder
1. Check current study plan (high memory items toward end)
2. Get one concept very wrong
3. Check new study plan
   - That concept should move to the TOP
   - Priority score should spike
   - Estimated time should be realistic

## 6. Examine the Math

### Decay Function
```python
from backend.brain.memory_engine import MemoryEngine

# How much does memory decay after 3 days?
memory_before = 0.75
days = 3
decay_rate = 0.1
stability = 1.0
interference = 1.0

memory_after = MemoryEngine.decay(
    memory_before, decay_rate, stability, interference, days
)

print(f"Memory: {memory_before:.2%} → {memory_after:.2%} after {days} days")
# Output: Memory: 75% → 54.31% after 3 days
```

### Half-Life Calculation
```python
# How long until memory drops to 50%?
half_life = MemoryEngine.half_life(0.1, 1.0, 1.0)
print(f"Half-life: {half_life:.1f} days")
# Output: Half-life: 6.9 days
```

### Priority Scoring
```python
from backend.brain.scheduler_engine import SchedulerEngine
from backend.brain.state import MemoryState

concept = MemoryState(
    user_id="u1",
    concept_id="integration_by_parts",
    memory_strength=0.3,
    decay_rate=0.15,
    importance_level=0.8
)

priority = SchedulerEngine._compute_priority(concept)
print(f"Priority: {priority:.2f}")
# Higher = study sooner
```

## 7. Expected Output Example

**First call to /submit-recall:**

```json
{
  "success": true,
  "memory_update": {
    "concept_id": "integration_by_parts",
    "memory_strength": 0.476,
    "confidence_level": "Emerging",
    "actual_score": 0.85,
    "predicted_range": [0.15, 0.65],
    "half_life_days": 6.93,
    "next_review_window": "7 days",
    "successful_recalls": 1,
    "failed_recalls": 0
  },
  "study_plan": {
    "total_concepts": 15,
    "total_estimated_time_minutes": 120,
    "next_concept": {
      "concept_id": "partial_fractions",
      "priority_score": 0.94,
      "reason": "Very weak memory - needs practice",
      "estimated_time_minutes": 8
    }
  },
  "dashboard": {
    "user_id": "u1",
    "total_concepts_studied": 1,
    "avg_memory_strength": 0.476,
    "weakest_concepts": [
      {
        "concept_id": "integration_by_parts",
        "memory_strength": 0.476,
        "confidence_level": "Emerging",
        "next_review": "7 days"
      }
    ]
  }
}
```

---

## Troubleshooting

### "Module not found: brain"
```bash
# Make sure you're in the backend directory
cd backend

# Restart the server
python -m uvicorn app:app --reload
```

### CORS errors from frontend
The endpoint is already set up. If you get CORS errors:
```python
# In backend/app.py, ensure CORS is configured
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Memory state not persisting between calls
**This is expected!** The state is in-memory only. Each time you restart the backend, state resets.

To persist state:
- Don't restart the backend between tests
- Or implement database layer (Phase 5)

---

## Success Checklist

- [ ] Backend starts with `/memory/submit-recall` endpoint
- [ ] Can submit a correct answer via cURL
- [ ] Can submit a wrong answer via cURL
- [ ] Memory strength increases on correct answers
- [ ] Memory strength decreases on wrong answers
- [ ] Confidence levels update appropriately
- [ ] Study plan contains ~15 concepts
- [ ] Next concept changes after submission
- [ ] Frontend button visible on dashboard
- [ ] Can start a recall session from frontend
- [ ] Can see real-time feedback
- [ ] Can inspect cognitive state in Python
- [ ] Half-life calculations make sense
- [ ] Priority scores reflect weakness + decay

---

**You now have a fully functional cognitive loop! 🧠✨**

Try submitting 5-10 recalls and watch how the system adapts.
