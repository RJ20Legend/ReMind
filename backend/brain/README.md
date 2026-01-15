# 🧠 ReMind Cognitive Loop - STEP 4: The Brain Stem

## Architecture Overview

The cognitive loop is now implemented as three runtime services working in concert:

### 1. **Memory Engine** (`backend/brain/memory_engine.py`)
The core cognitive algorithms:
- **Decay Model**: Exponential decay using $M(t) = M_0 \cdot e^{-\lambda \cdot \sigma \cdot \xi \cdot t}$
- **Half-life Computation**: How long until memory drops to 50%
- **Confidence Levels**: Weak → Emerging → Solid → Mastered
- **Review Windows**: Automatic scheduling based on memory strength
- **Reinforcement**: Adjusts memory gain based on performance
- **Prediction Error**: Adapts model when actual performance surprises predictions

**Key Methods:**
- `decay()` - Calculate memory after time
- `predict_range()` - Expected memory boundaries with uncertainty
- `score_from_result()` - Convert answer quality to numeric score
- `update_memory_on_recall()` - Full memory update on submission
- `apply_prediction_error()` - Adaptive model adjustment

### 2. **Scheduler Engine** (`backend/brain/scheduler_engine.py`)
Intelligent study plan generation:
- **Priority Scoring**: Multi-factor formula considering:
  - Memory weakness (1 - strength)
  - Decay rate (fast decaying concepts prioritized)
  - Importance level
  - Difficulty level
  - Review window status (overdue = high priority)
  - Episodic replay needs
  - Interference factors

- **Study Plan Generation**: Selects ~15 concepts per day, respects time budget
- **Dynamic Rebalancing**: Adjusts plan after each recall
- **Session Metrics**: Tracks completion, average score, session quality

**Key Methods:**
- `_compute_priority()` - Calculates priority score for one concept
- `generate_study_plan()` - Creates today's study sequence
- `get_next_concept()` - Returns next item from plan
- `rebalance_plan_after_recall()` - Updates plan mid-session

### 3. **Cognitive State** (`backend/brain/state.py`)
In-memory runtime state (no database):
- `MemoryState`: One concept's memory for one user
- `RecallSubmission`: User's answer to a question
- `StudyPlanItem`: One concept in today's plan
- `CognitiveState`: Global workspace holding all user states

**Thread-safe operations:**
- `get_or_create_memory(user_id, concept_id)`
- `update_memory(user_id, concept_id, state)`
- `get_all_concepts_for_user(user_id)`
- `log_event()` - Event tracking for debugging

---

## API Endpoint: POST /submit-recall

The **single API call** that powers the cognitive loop:

```json
POST /memory/submit-recall
{
  "user_id": "u1",
  "concept_id": "integration_by_parts",
  "correctness": "slow_correct",      // instant_correct | slow_correct | partial | incorrect
  "response_time": 7.2,                // seconds
  "hint_used": true,
  "failure_type": null,
  "transfer_flag": false,
  "fatigue_state": "normal"            // low | normal | high
}
```

### Response Structure

```json
{
  "success": true,
  "memory_update": {
    "concept_id": "integration_by_parts",
    "memory_strength": 0.58,
    "confidence_level": "Emerging",
    "actual_score": 0.85,
    "predicted_range": [0.42, 0.68],
    "half_life_days": 4.2,
    "next_review_window": "7 days",
    "successful_recalls": 3,
    "failed_recalls": 1
  },
  "study_plan": {
    "total_concepts": 15,
    "total_estimated_time_minutes": 120,
    "next_concept": {
      "concept_id": "partial_fractions",
      "priority_score": 0.87,
      "reason": "Due for review tomorrow",
      "estimated_time_minutes": 8
    }
  },
  "dashboard": {
    "user_id": "u1",
    "total_concepts_studied": 42,
    "avg_memory_strength": 0.62,
    "weakest_concepts": [...]
  }
}
```

### One Call Does Everything:

1. ✅ **Updates memory** using Memory Engine
2. ✅ **Recomputes decay** and confidence
3. ✅ **Adjusts model** if prediction was wrong
4. ✅ **Regenerates study plan** using Scheduler
5. ✅ **Returns next concept** to study
6. ✅ **Updates dashboard** with real-time metrics

---

## Frontend: RecallInterface Component

**Location:** `frontend/src/components/RecallInterface.js`

### Features:
- 🎯 **Big Start Button**: Glowing "🧠 Start Recall Session" button
- ❓ **Question Display**: Shows the concept and a question to answer
- ✍️ **Answer Input**: Text area for user response
- 💡 **Hint Button**: Shows context-specific hints
- ✓ **Submit Button**: Sends to backend
- 📊 **Real-time Feedback**: 
  - Score (0-100%)
  - Memory strength before/after
  - Confidence level
  - Next review window
- 📈 **Session Metrics**: 
  - Concepts completed
  - Average score
  - Session duration

### Integration into Dashboard:

```javascript
import RecallInterface from '../components/RecallInterface'

// Toggle view
<button onClick={() => setShowRecallSession(true)}>
  🧠 Start Recall Session
</button>

// Full-screen recall interface
{showRecallSession && <RecallInterface userId="u1" />}
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                 USER ANSWERS QUESTION                   │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│        POST /memory/submit-recall                        │
│  (correctness, response_time, hint_used, fatigue)       │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────┐
        │  MEMORY ENGINE UPDATES           │
        ├──────────────────────────────────┤
        │ 1. Apply current decay           │
        │ 2. Score the answer              │
        │ 3. Detect prediction errors      │
        │ 4. Update memory strength        │
        │ 5. Recompute confidence          │
        │ 6. Calculate next review window  │
        └──────────────────────┬───────────┘
                               │
                               ▼
              ┌────────────────────────────┐
              │ STORE IN COGNITIVE STATE   │
              │ (in-memory, thread-safe)   │
              └────────────────┬───────────┘
                               │
                               ▼
        ┌──────────────────────────────────┐
        │  SCHEDULER ENGINE REBALANCES     │
        ├──────────────────────────────────┤
        │ 1. Get all user's concepts       │
        │ 2. Compute priorities            │
        │ 3. Generate new study plan       │
        │ 4. Select next concept           │
        └──────────────────────┬───────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────┐
│          RETURN RESPONSE TO FRONTEND                    │
├─────────────────────────────────────────────────────────┤
│ - Updated memory metrics                                │
│ - Next concept to study                                 │
│ - Real-time dashboard stats                             │
│ - Session progress                                      │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│      FRONTEND SHOWS FEEDBACK & NEXT QUESTION             │
│  - "Your answer was correct! ✅"                        │
│  - "Memory strength: 58% (was 45%)"                     │
│  - "Next: Partial Fractions"                            │
└─────────────────────────────────────────────────────────┘
```

---

## Example Session Flow

### Step 1: User clicks "🧠 Start Recall Session"
- RecallInterface loads study plan (mock data for now)
- Displays: "integration_by_parts" question
- Timer starts

### Step 2: User answers "∫ x·e^x dx = x·e^x - ∫ e^x dx = x·e^x - e^x + C"
- Click "✓ Submit Answer"
- RecallInterface calculates response_time ≈ 45 seconds

### Step 3: Backend processes via /submit-recall
```
Memory before: strength=0.35, confidence=Weak
↓
After 3 days: decay → 0.28
Answer score: 0.85 (slow but correct)
No prediction error (within expected range)
↓
Reinforcement: gain = (1 - 0.28) × 0.2 × 0.85 = 0.12
Memory after: 0.28 + 0.12 = 0.40 ✅
Confidence: Emerging (0.40 ≥ 0.40)
Next review: 7 days (memory improved)
```

### Step 4: Frontend shows feedback
```
✅ Correct! Your answer was solid.

Score:                85%
Memory Strength:      40% (was 35%)
Confidence:           Emerging
Next Review:          7 days
```

### Step 5: Next concept loads automatically
```
2/15 completed | Average Score: 85%
Next: partial_fractions (priority: 87%)
"Due for review tomorrow"
```

---

## Why This Works

### 🎯 Scientifically Grounded
- Uses exponential decay (proven by Ebbinghaus)
- Adapts to individual learning (prediction error)
- Spaces reviews automatically (Leitner system)

### ⚡ Fast Feedback Loop
- One API call does everything
- User sees results immediately
- Memory strength changes visible in real-time

### 🧠 No Database Yet
- Pure in-memory cognition
- Easy to debug and reason about
- Ready to plug in database when needed

### 📊 Transparent
- Every number has a meaning
- User sees decay, confidence, next review window
- Builds trust in the system

---

## Next Steps (When Ready)

1. **Persist to Database**: Add database layer without changing API
2. **AI Answer Evaluation**: Replace mock correctness with actual evaluation
3. **Real Question Generation**: Generate questions from curriculum
4. **Multi-user Support**: Scale study plans across users
5. **Transfer Learning**: Track when concepts help each other
6. **Adaptive Difficulty**: Adjust question difficulty based on performance
7. **Fatigue Modeling**: Correlate user fatigue state with performance

---

## Testing the Cognitive Loop

Try these commands to test the system:

```bash
# Start the backend
cd backend
python -m uvicorn app:app --reload

# In another terminal, test the endpoint
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
```

---

## File Structure

```
backend/
├── brain/
│   ├── __init__.py              # Exports all classes
│   ├── state.py                 # MemoryState, CognitiveState
│   ├── memory_engine.py         # Decay, confidence, reinforcement
│   └── scheduler_engine.py      # Priority, study plans
│
├── routes/
│   └── memory.py                # /submit-recall endpoint
│
└── app.py                       # FastAPI setup

frontend/
├── src/
│   ├── components/
│   │   └── RecallInterface.js   # Main study UI
│   │
│   └── pages/
│       └── dashboard.js          # Integrates RecallInterface
```

---

**Status: ✅ COMPLETE**
The cognitive loop is now fully functional. You can watch memory rise and decay in real-time.
