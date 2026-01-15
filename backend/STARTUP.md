# 🚀 Backend Startup Guide

## ✅ Setup is Complete!

Your backend is now correctly wired with the cognitive loop brain. All imports are working.

---

## 📋 Quick Checklist

- ✅ `backend/brain/__init__.py` exists and exports all functions
- ✅ `brain/state.py`, `memory_engine.py`, `scheduler_engine.py` all present
- ✅ Imports verified (test_import.py passes)
- ✅ Cognitive loop tested (verify_setup.py passes)
- ✅ FastAPI routes configured

---

## 🎯 Running the Backend

### Step 1: Install Dependencies
```bash
cd E:\ReMind\backend
pip install -r requirements.txt
```

### Step 2: Start FastAPI Server
```bash
cd E:\ReMind\backend
uvicorn app:app --reload
```

**Important:** Always run from `backend/` directory, not from `ReMind/`

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 3: Test the API
```bash
curl -X POST http://localhost:8000/memory/submit-recall \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u1",
    "concept_id": "integration_by_parts",
    "correctness": "correct",
    "response_time": 3.5,
    "hint_used": false,
    "failure_type": null,
    "transfer_flag": false,
    "fatigue_state": "normal"
  }'
```

Or open in browser:
```
http://localhost:8000/docs
```
(Click "Try it out" on POST /submit-recall endpoint)

---

## 🔌 API Endpoints

### POST /memory/submit-recall
**Purpose:** Submit a recall attempt and get memory update + study plan

**Request:**
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
    // ... top 5 concepts
  ]
}
```

### GET /memory/user/{user_id}/concepts
**Purpose:** Get all concepts for a user

### GET /memory/events
**Purpose:** Get recent recall events (for debugging)

---

## 🧠 Brain System Overview

### What Happens When You Submit a Recall

1. **Get state** → Retrieve user's memory state for the concept
2. **Process recall** → Run the cognitive loop:
   - Apply memory decay (forgetting over time)
   - Predict expected performance
   - Score the answer (0.0-1.0)
   - Detect prediction errors
   - Adapt model parameters
   - Reinforce memory (boost if correct, reduce if wrong)
   - Update confidence level
   - Determine next review window
3. **Schedule** → Rank all concepts by priority
4. **Return** → Send updated state + top 5 concepts to study

All of this happens in ~1ms.

---

## 📊 State Structure

Each concept has 17 fields:
```python
{
    "memory_strength": 0.6,           # 0-1 scale
    "last_revision_time": 0,          # timestamp
    "successful_recalls": 0,          # counter
    "failed_recalls": 0,              # counter
    "decay_rate": 0.1,                # how fast they forget
    "confidence_state": "Weak",       # Weak | Partial | Confident
    "review_window": "7 days",        # when to review next
    # ... 10 more fields for decay physics
}
```

---

## 🧪 Verification Tests

### Test 1: Import Verification
```bash
cd E:\ReMind\backend
python test_import.py
```
Should output:
```
✅ brain.state imports successful
✅ brain.memory_engine imports successful
✅ brain.scheduler_engine imports successful
✅ Full brain API import successful
```

### Test 2: Full Setup Verification
```bash
cd E:\ReMind\backend
python verify_setup.py
```
Should output:
```
✅ All checks passed!
```

---

## 📁 Project Structure

```
E:\ReMind\
├── backend/
│   ├── __init__.py              ✅ Backend is a package
│   ├── app.py                   ✅ FastAPI app entry point
│   ├── main.py                  ✅ Router setup
│   ├── brain/
│   │   ├── __init__.py          ✅ Brain is a package (REQUIRED)
│   │   ├── state.py             ✅ In-memory state management
│   │   ├── memory_engine.py     ✅ Memory decay + learning
│   │   └── scheduler_engine.py  ✅ Priority-based scheduling
│   ├── routes/
│   │   └── memory.py            ✅ /submit-recall endpoint
│   ├── test_import.py           ✅ Test imports
│   └── verify_setup.py          ✅ Full verification
└── frontend/
    └── ...
```

---

## ❓ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'brain'"
**Problem:** Running from wrong directory
**Solution:** 
```bash
cd E:\ReMind\backend  # NOT E:\ReMind
uvicorn app:app --reload
```

### Error: "ImportError: cannot import name 'users' from 'brain'"
**Problem:** brain/__init__.py is missing or empty
**Solution:** Check that `brain/__init__.py` has proper exports:
```python
from .state import users, event_log
from .memory_engine import process
from .scheduler_engine import schedule
```

### Error: "No module named 'brain.state'"
**Problem:** brain/ is not a package (missing __init__.py)
**Solution:** Verify `backend/brain/__init__.py` exists (can be empty)

---

## 🚀 Next Steps

1. **Start the server:**
   ```bash
   cd E:\ReMind\backend
   uvicorn app:app --reload
   ```

2. **Test with the frontend:**
   - Frontend calls `POST /submit-recall`
   - Backend processes recall through cognitive loop
   - Returns updated memory + study plan

3. **Monitor requests:**
   - Check `http://localhost:8000/docs` for interactive API docs
   - Check event log: `GET /memory/events`

---

## 💡 Key Points

- ✅ **Always run from backend/ directory** - This makes Python treat backend as root
- ✅ **__init__.py is required** - Makes folders into packages
- ✅ **Imports are relative** - Use `from ..brain import` in routes
- ✅ **State is in-memory** - Resets on server restart (Phase 5: add database)
- ✅ **API is stateless** - Each request is independent

---

## 📞 Reference

- **Documentation:** See [backend/INDEX.md](../INDEX.md)
- **Quick Reference:** See [backend/../BRAIN_QUICK_REFERENCE.md](../BRAIN_QUICK_REFERENCE.md)
- **API Contract:** See [backend/../API_CONTRACT.py](../API_CONTRACT.py)

---

🧠 **Your brain is ready to run. Let's go!** 🚀
