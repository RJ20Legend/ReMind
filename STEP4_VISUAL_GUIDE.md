# 🧠 Step 4 Implementation: Visual Guide

## The Three Layers of the Brain

```
┌─────────────────────────────────────────────────────────────────┐
│                       API GATEWAY                                │
│                   POST /submit-recall                            │
└───────────────┬─────────────────────────────────────┬───────────┘
                │                                     │
        ┌───────▼──────────┐             ┌───────────▼────────┐
        │   SUBMISSION     │             │   RESPONSES        │
        ├──────────────────┤             ├────────────────────┤
        │ • user_id        │             │ • memory_update    │
        │ • concept_id     │             │ • study_plan       │
        │ • correctness    │             │ • dashboard        │
        │ • response_time  │             └────────────────────┘
        │ • hint_used      │
        │ • fatigue_state  │
        └────────┬─────────┘
                 │
    ┌────────────▼──────────────────┐
    │                               │
    │   ORCHESTRATION LAYER         │
    │                               │
    │  1. Get/Create Memory State   │
    │  2. Create RecallSubmission   │
    │  3. Call MemoryEngine         │
    │  4. Update CognitiveState     │
    │  5. Call SchedulerEngine      │
    │  6. Return Response           │
    │                               │
    └───┬──────────────────────┬────┘
        │                      │
        ▼                      ▼
    ┌─────────────┐     ┌──────────────┐
    │   MEMORY    │     │  SCHEDULER   │
    │   ENGINE    │     │   ENGINE     │
    ├─────────────┤     ├──────────────┤
    │ • decay()   │     │ • priority() │
    │ • score()   │     │ • plan()     │
    │ • update()  │     │ • balance()  │
    │ • predict() │     │ • metrics()  │
    └──────┬──────┘     └──────┬───────┘
           │                   │
           │    ┌──────────────┘
           │    │
           ▼    ▼
    ┌─────────────────────┐
    │  COGNITIVE STATE    │
    │  (in-memory)        │
    │                     │
    │  users = {          │
    │    "u1": {          │
    │      "concept_id":  │
    │        MemoryState  │
    │    }                │
    │  }                  │
    │                     │
    │  study_plans = {}   │
    │  event_log = []     │
    └─────────────────────┘
```

---

## Data Transformation Journey

```
Raw Answer
    │
    ├─→ Score (0.0-1.0)
    │   └─→ instant_correct = 1.0
    │       slow_correct = 0.85
    │       partial = 0.50
    │       incorrect = 0.10
    │       (-15% if hint used)
    │
    ▼
Current Memory State
    ├─→ Apply decay over days
    │   └─→ Memory strength decreases
    │
    ├─→ Apply performance
    │   ├─→ Correct: reinforce
    │   └─→ Wrong: penalize
    │
    ├─→ Detect prediction error
    │   ├─→ Better than expected: stabilize
    │   └─→ Worse than expected: increase decay
    │
    ▼
Updated Memory State
    ├─→ New memory strength
    ├─→ New confidence level
    ├─→ New review window
    └─→ Adapt learning rate
    │
    ▼
Generate Study Plan
    ├─→ Compute priority for each concept
    │   ├─→ weakness: 1 - memory_strength
    │   ├─→ decay: high decay = high priority
    │   ├─→ importance: user-defined importance
    │   ├─→ difficulty: harder = more review
    │   └─→ overdue: review window status
    │
    ├─→ Sort by priority (descending)
    │
    └─→ Select ~15 for today
        ├─→ Respect time budget (120 min)
        └─→ Return next concept

Response to Frontend
    ├─→ Updated memory metrics
    ├─→ Next concept to study
    ├─→ Session statistics
    └─→ Real-time dashboard
```

---

## Memory Strength Over Time

```
SCENARIO: Learning "Integration by Parts"

Day 0 (First Study):
│
├─ Initial: 0.30 (forgot, have seen it)
├─ Answer: Correct (score: 0.85)
├─ Updated: 0.30 + (1-0.30) × 0.2 × 0.85 = 0.42
└─ Confidence: "Emerging" ✓

Day 1:
│
├─ Decay: 0.42 × e^(-0.1×1.0×1.0×1) ≈ 0.38
├─ Answer: Correct (score: 0.95)
├─ Updated: 0.38 + (1-0.38) × 0.2 × 0.95 ≈ 0.50
└─ Confidence: "Emerging" → "Solid" ✓✓

Day 3 (No review yet):
│
├─ Decay: 0.50 × e^(-0.1×1.0×1.0×3) ≈ 0.37
├─ Answer: Correct (score: 0.95)
├─ Updated: 0.37 + (1-0.37) × 0.2 × 0.95 ≈ 0.49
└─ Confidence: "Solid" (barely)

Day 7 (Scheduled review):
│
├─ Decay: 0.49 × e^(-0.1×1.0×1.0×7) ≈ 0.25
├─ Answer: Wrong (score: 0.15)
├─ Updated: 0.25 × 0.70 ≈ 0.18 ❌
└─ Confidence: "Solid" → "Weak" (back to square one)

Day 8 (Immediately reschedule):
│
├─ Next review: "today" (high priority)
├─ Answer: Correct (score: 0.95)
├─ Updated: 0.18 + (1-0.18) × 0.2 × 0.95 ≈ 0.34
└─ Confidence: "Weak" → "Emerging"

                    Memory Strength Chart
                    ▲
                 1.0┤
                    │                          ✓✓✓
                 0.8┤                      ✓✓
                    │                  ✓✓
                 0.6┤              ✓
                    │          ✓  \
                 0.4┤     ✓\       \        ✓
                    │  ✓   \        \    ✓
                 0.2┤       \    ❌  \
                    │         \      ✓
                 0.0┼─────────────────────────────►
                    0  1  2  3  4  5  6  7  8  Days
                    
    ✓ = Correct    ❌ = Wrong    \ = Decay between reviews
```

---

## Priority Scoring Formula

```
For each concept, Priority = 
    2.0 × (1 - memory_strength)           [Weakness]
  + 1.5 × decay_rate                      [Decay speed]
  + 1.2 × importance_level                [Importance]
  + 0.8 × difficulty_level                [Difficulty]
  + max(0, interference_factor - 1.0)     [Interference]
  × REVIEW_WINDOW_BOOST                   [Overdue boost]
    └─→ "today": 3.0x
    └─→ "1 day": 2.0x
    └─→ "7 days": 1.4x
    └─→ "14 days": 1.1x
    └─→ "30 days": 0.6x
  × (1.5 if episodic_replay_needed)       [Recall practice]

Example Calculation:
┌──────────────────────────────────────┐
│ Concept: "Integration by Parts"      │
├──────────────────────────────────────┤
│ memory_strength: 0.35                │
│ decay_rate: 0.12                     │
│ importance_level: 0.9                │
│ difficulty_level: 0.7                │
│ review_window: "today" (3.0x)        │
│ episodic_replay: false               │
├──────────────────────────────────────┤
│ Priority = 2.0 × (1 - 0.35)          │
│          + 1.5 × 0.12                │
│          + 1.2 × 0.9                 │
│          + 0.8 × 0.7                 │
│          = 1.30 + 0.18 + 1.08 + 0.56 │
│          = 3.12                      │
│          × 3.0 (overdue boost)       │
│          = 9.36 ← VERY HIGH PRIORITY │
└──────────────────────────────────────┘

Concept: "Derivatives" (solid, not overdue)
├─ memory_strength: 0.75
├─ decay_rate: 0.08
├─ importance_level: 0.6
├─ difficulty_level: 0.5
├─ review_window: "30 days" (0.6x)
│
Priority = 2.0 × 0.25 + 1.5 × 0.08 + 1.2 × 0.6 + 0.8 × 0.5
         = 0.50 + 0.12 + 0.72 + 0.40
         = 1.74
         × 0.6 (not overdue)
         = 1.04 ← LOW PRIORITY (study later)
```

---

## Response Structure

```
POST /memory/submit-recall
│
├─ Input
│  ├─ user_id: "u1"
│  ├─ concept_id: "integration_by_parts"
│  ├─ correctness: "slow_correct"
│  ├─ response_time: 7.2 (seconds)
│  ├─ hint_used: true
│  ├─ failure_type: null
│  ├─ transfer_flag: false
│  └─ fatigue_state: "normal"
│
├─ Processing
│  ├─ MemoryEngine.update_memory_on_recall()
│  ├─ CognitiveState.update_memory()
│  ├─ SchedulerEngine.generate_study_plan()
│  └─ Build response
│
└─ Output
   ├─ success: true
   │
   ├─ memory_update
   │  ├─ memory_strength: 0.58 (was 0.45)
   │  ├─ confidence_level: "Emerging"
   │  ├─ actual_score: 0.85 (performance metric)
   │  ├─ predicted_range: [0.42, 0.68] (what we expected)
   │  ├─ half_life_days: 4.2 (days until 50%)
   │  ├─ next_review_window: "7 days" (auto-scheduled)
   │  ├─ successful_recalls: 3
   │  └─ failed_recalls: 1
   │
   ├─ study_plan
   │  ├─ total_concepts: 15 (today's plan size)
   │  ├─ total_estimated_time_minutes: 120
   │  └─ next_concept
   │     ├─ concept_id: "partial_fractions"
   │     ├─ priority_score: 0.87 (why it's next)
   │     ├─ reason: "Due for review tomorrow"
   │     └─ estimated_time_minutes: 8
   │
   └─ dashboard
      ├─ user_id: "u1"
      ├─ total_concepts_studied: 42
      ├─ avg_memory_strength: 0.62
      └─ weakest_concepts (top 5)
         ├─ concept_id: "limits"
         ├─ memory_strength: 0.28
         ├─ confidence_level: "Weak"
         └─ next_review: "today"
```

---

## Frontend Flow

```
Dashboard Page
│
├─ Show MemoryHeatmap
├─ Show Statistics
│
└─ BUTTON: "🧠 Start Recall Session"
   │
   └─ Click
      │
      ▼
RecallInterface Component (Full Screen)
│
├─ Session Header
│  ├─ Progress: 2/15 completed
│  ├─ Average Score: 85%
│  ├─ Session Time: 12m 34s
│  └─ Button: "End Session"
│
├─ Concept Card
│  ├─ Concept ID: "integration_by_parts"
│  ├─ Priority: 94%
│  ├─ Reason: "Very weak memory - needs practice"
│  │
│  └─ Question Display
│     └─ "Solve: ∫ x·e^x dx using integration by parts"
│
├─ Answer Input
│  └─ <textarea> for user response
│
├─ Button Row
│  ├─ "💡 Show Hint" button
│  │  └─ Hint: "Use LIATE rule..."
│  │
│  └─ "✓ Submit Answer" button
│     │
│     └─ Sends to /submit-recall
│
└─ Feedback Section (after submit)
   ├─ Result Badge
   │  ├─ ✅ Correct!     OR     ❌ Incorrect
   │  │
   │  └─ Score: 85%
   │
   ├─ Memory Metrics
   │  ├─ Memory Strength: 58% (was 45%)
   │  ├─ Confidence: Emerging
   │  ├─ Next Review: 7 days
   │  └─ Half-life: 4.2 days
   │
   └─ Auto-loads next concept (2 sec delay)
      │
      └─ Next: "Partial Fractions"
         ├─ Priority: 87%
         ├─ "Due for review tomorrow"
         └─ Same Q→A→Feedback loop
```

---

## File Dependencies

```
frontend/src/
├─ pages/dashboard.js
│  └─ imports RecallInterface
│
└─ components/
   └─ RecallInterface.js
      ├─ Makes fetch() to /memory/submit-recall
      └─ Displays response in real-time

backend/
├─ app.py
│  └─ imports routes
│
├─ main.py
│  └─ includes routes
│
├─ routes/memory.py
│  ├─ imports brain modules
│  └─ defines @router.post("/submit-recall")
│
└─ brain/
   ├─ __init__.py
   │  └─ exports all classes
   │
   ├─ state.py
   │  ├─ MemoryState (data class)
   │  ├─ RecallSubmission (data class)
   │  ├─ StudyPlanItem (data class)
   │  └─ CognitiveState (store)
   │
   ├─ memory_engine.py
   │  ├─ decay()
   │  ├─ half_life()
   │  ├─ score_from_result()
   │  ├─ update_confidence()
   │  ├─ compute_review_window()
   │  └─ update_memory_on_recall()
   │
   └─ scheduler_engine.py
      ├─ _compute_priority()
      ├─ generate_study_plan()
      ├─ get_next_concept()
      └─ compute_session_metrics()
```

---

## The Magic Happens Here 🌟

### Memory Update Logic
```
Before:   strength=0.35 (Weak)
            │
Decay:      ├─ 3 days pass
            │  strength → 0.28
            │
Score:      ├─ User answers: 0.85 score
            │
Reinforce:  ├─ gain = (1-0.28) × 0.2 × 0.85 = 0.12
            │
After:      └─ strength = 0.28 + 0.12 = 0.40 ✓
                Confidence: Weak → Emerging
```

### Scheduler Magic
```
All Concepts (50+):
  ├─ calc_derivatives: weak, overdue → priority=12.4
  ├─ limits: emerging, recent → priority=3.2
  ├─ integration_parts: solid, not due → priority=0.9
  └─ ... 47 more

Sort by priority:
  1. calc_derivatives: 12.4 ← STUDY FIRST
  2. partial_fractions: 8.7
  3. arima_models: 7.2
  4. limits: 3.2
  5. integration_parts: 0.9 ← STUDY LAST
  ...

Select top 15 for today (120 min budget):
  ├─ calc_derivatives: 12 min (weak)
  ├─ partial_fractions: 8 min (weak)
  ├─ arima_models: 12 min (hard)
  ├─ ... 12 more
  └─ Total: 120 min 🎯
```

---

**The cognitive loop is now a living, breathing system.** 🧠✨

Every answer teaches it something new. Every decay calculation makes memory more real.
