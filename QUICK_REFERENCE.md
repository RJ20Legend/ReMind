# 🧠 Quick Reference Card

## The Cognitive Loop in 30 Seconds

```
User answers question
    ↓
POST /memory/submit-recall
    ↓
MemoryEngine updates state
    ↓
SchedulerEngine generates plan
    ↓
Return new memory + next concept
    ↓
Frontend shows feedback + next question
```

---

## Key Files

| File | Purpose | Lines |
|------|---------|-------|
| `backend/brain/state.py` | In-memory state management | 176 |
| `backend/brain/memory_engine.py` | Decay, confidence, reinforcement | 301 |
| `backend/brain/scheduler_engine.py` | Priority scoring, study plans | 249 |
| `backend/routes/memory.py` | /submit-recall endpoint | +120 |
| `frontend/components/RecallInterface.js` | Study UI | 450+ |

---

## API Endpoint

```
POST /memory/submit-recall

Input:
{
  "user_id": "u1",
  "concept_id": "integration_by_parts",
  "correctness": "slow_correct",
  "response_time": 7.2,
  "hint_used": false,
  "failure_type": null,
  "transfer_flag": false,
  "fatigue_state": "normal"
}

Output:
{
  "success": true,
  "memory_update": { ... },
  "study_plan": { ... },
  "dashboard": { ... }
}
```

---

## Memory Engine

### Decay Formula
$$M(t) = M_0 \cdot e^{-\lambda \cdot \sigma \cdot \xi \cdot t}$$

### Half-life
$$t_{1/2} = \frac{\ln(2)}{\lambda \cdot \sigma \cdot \xi}$$

### Confidence Levels
- **Mastered**: strength ≥ 0.85
- **Solid**: 0.65 ≤ strength < 0.85
- **Emerging**: 0.40 ≤ strength < 0.65
- **Weak**: strength < 0.40

### Review Windows
- **today**: strength < 0.20
- **1 day**: 0.20 ≤ strength < 0.40
- **7 days**: 0.40 ≤ strength < 0.65
- **14 days**: 0.65 ≤ strength < 0.85
- **30 days**: strength ≥ 0.85

---

## Scheduler Engine

### Priority Scoring

```python
priority = (
    2.0 * (1 - memory_strength) +      # Weakness
    1.5 * decay_rate +                 # Decay speed
    1.2 * importance_level +           # Importance
    0.8 * difficulty_level             # Difficulty
)
priority *= REVIEW_WINDOW_BOOST[window]
```

### Review Window Boosts
- "today": 3.0x
- "1 day": 2.0x
- "7 days": 1.4x
- "14 days": 1.1x
- "30 days": 0.6x

---

## Testing

```bash
# Start backend
cd backend
python -m uvicorn app:app --reload

# Test API (correct answer)
curl -X POST http://localhost:8000/memory/submit-recall \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u1",
    "concept_id": "integration_by_parts",
    "correctness": "slow_correct",
    "response_time": 7.2,
    "hint_used": false,
    "failure_type": null,
    "transfer_flag": false,
    "fatigue_state": "normal"
  }'

# Start frontend
cd frontend
npm run dev
# Open http://localhost:3000/dashboard
# Click "🧠 Start Recall Session"
```

---

## Inspection

```python
from backend.brain import cognitive_state

# Get all concepts for user
concepts = cognitive_state.get_all_concepts_for_user("u1")

# Print memory strengths
for c in sorted(concepts, key=lambda x: x.memory_strength, reverse=True):
    print(f"{c.concept_id}: {c.memory_strength:.0%} ({c.confidence_level})")

# View event log
for event in cognitive_state.event_log[-5:]:
    print(event)

# Clear state (for testing)
cognitive_state.clear()
```

---

## Expected Results

### Correct Answer
- Memory strength: **increases**
- Confidence: **improves**
- Next review: **pushed back**
- Priority: **decreases**

### Wrong Answer
- Memory strength: **decreases**
- Confidence: **drops**
- Next review: **pulled forward**
- Priority: **increases**

### Multiple Correct Answers
- Memory: 0.30 → 0.42 → 0.50 → 0.56 (diminishing returns)
- Confidence: Weak → Emerging → Solid → Solid
- Half-life: increases (more stable)

---

## Common Mistakes to Avoid

❌ **Don't** modify `CognitiveState` directly - use the provided methods
✅ **Do** use `get_or_create_memory()` and `update_memory()`

❌ **Don't** call MemoryEngine methods with wrong parameter types
✅ **Do** pass floats, not percentages (0.5, not 50%)

❌ **Don't** restart the backend between tests (loses state)
✅ **Do** run multiple recalls before restarting

❌ **Don't** expect database persistence
✅ **Do** remember state is in-memory only

❌ **Don't** hardcode user_id
✅ **Do** pass it in the request payload

---

## Next Steps

1. **Test the loop**: Submit 5-10 recalls and watch memory change
2. **Inspect state**: Print cognitive_state to understand structure
3. **Verify math**: Calculate half-life by hand, compare with API
4. **Check priority**: See why concepts are ordered that way
5. **Plan Phase 5**: Database layer, real questions, AI evaluation

---

## Documentation

| Document | Purpose |
|----------|---------|
| `backend/brain/README.md` | Comprehensive architecture |
| `QUICK_START.md` | Step-by-step testing guide |
| `STEP4_COMPLETE.md` | Full implementation summary |
| `STEP4_VISUAL_GUIDE.md` | Diagrams and visuals |
| `STEP4_CHECKLIST.md` | Feature checklist |
| This file | Quick reference |

---

## Architecture at a Glance

```
┌─────────────────────────────────┐
│    POST /submit-recall          │
└────────┬────────────────────────┘
         │
         ├─→ MemoryEngine
         │   ├─ decay
         │   ├─ score
         │   ├─ update
         │   └─ predict
         │
         ├─→ CognitiveState
         │   ├─ store
         │   ├─ log
         │   └─ recall
         │
         └─→ SchedulerEngine
             ├─ priority
             ├─ plan
             └─ metrics
             
         ↓
         
    Response with:
    ├─ memory_update
    ├─ study_plan
    └─ dashboard
```

---

## Status

🟢 **STEP 4: COMPLETE**

- ✅ Memory Engine: 100%
- ✅ Scheduler Engine: 100%
- ✅ API Endpoint: 100%
- ✅ Frontend Component: 100%
- ✅ Documentation: 100%

**Ready for Phase 5: Persistence Layer**

---

## Support

### Error: "Module not found: brain"
```bash
cd backend
python -m uvicorn app:app --reload
```

### Error: "Cannot find memory_engine"
Check `backend/brain/__init__.py` exports the class

### Memory not changing
Check `cognitive_state.event_log` for what happened

### Frontend not connecting
Check backend is running on port 8000

---

**Remember: This is just the beginning. 🚀**
The cognitive loop is now beating.

Next: Add a heartbeat (database). 💓
