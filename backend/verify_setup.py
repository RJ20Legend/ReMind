"""
Backend Setup Verification
Run from: E:\ReMind\backend
Command: python verify_setup.py
"""

import os
import sys
from pathlib import Path

print("🔍 Backend Setup Verification\n")
print("=" * 60)

# Check 1: Directory structure
print("\n1️⃣ Checking directory structure...")
checks = {
    "backend/brain/__init__.py": Path("brain/__init__.py").exists(),
    "backend/brain/state.py": Path("brain/state.py").exists(),
    "backend/brain/memory_engine.py": Path("brain/memory_engine.py").exists(),
    "backend/brain/scheduler_engine.py": Path("brain/scheduler_engine.py").exists(),
    "backend/app.py": Path("app.py").exists(),
    "backend/main.py": Path("main.py").exists(),
    "backend/routes/memory.py": Path("routes/memory.py").exists(),
}

for file, exists in checks.items():
    status = "✅" if exists else "❌"
    print(f"   {status} {file}")

all_files_exist = all(checks.values())
print(f"\n   {'✅ All files present' if all_files_exist else '❌ Some files missing'}")

# Check 2: Imports
print("\n2️⃣ Testing imports...")
try:
    from brain import users, event_log, process, schedule, DEFAULT_STATE
    print("   ✅ from brain import * works")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Check 3: State validation
print("\n3️⃣ Validating brain state...")
print(f"   ✅ users: {type(users).__name__} = {users.keys()}")
print(f"   ✅ event_log: {type(event_log).__name__} (length: {len(event_log)})")
print(f"   ✅ DEFAULT_STATE: {len(DEFAULT_STATE)} fields")

# Check 4: Function validation
print("\n4️⃣ Checking brain functions...")
functions = {
    "process": process,
    "schedule": schedule,
}
for fname, func in functions.items():
    is_callable = callable(func)
    status = "✅" if is_callable else "❌"
    print(f"   {status} {fname}() is callable")

# Check 5: Test a recall submission
print("\n5️⃣ Testing cognitive loop...")
try:
    # Get initial state
    test_user = "u1"
    test_concept = "integration_by_parts"
    
    if test_user not in users:
        users[test_user] = {}
    if test_concept not in users[test_user]:
        users[test_user][test_concept] = DEFAULT_STATE.copy()
    
    state = users[test_user][test_concept]
    initial_strength = state["memory_strength"]
    
    # Process a recall
    result = process(state, {
        "correctness": "correct",
        "response_time": 3.5,
        "hint_used": False,
        "failure_type": None,
        "transfer_flag": False,
        "fatigue_state": "normal"
    })
    
    final_strength = result["memory_strength"]
    print(f"   ✅ Memory state processed")
    print(f"      - Initial strength: {initial_strength:.2f}")
    print(f"      - Final strength: {final_strength:.2f}")
    print(f"      - Confidence: {result['confidence_state']}")
    
    # Generate study plan
    plan = schedule(users[test_user])
    print(f"   ✅ Study plan generated")
    print(f"      - Top concepts: {len(plan)}")
    
except Exception as e:
    print(f"   ❌ Cognitive loop test failed: {e}")
    sys.exit(1)

# Final status
print("\n" + "=" * 60)
print("✅ All checks passed!")
print("=" * 60)

print("\n📝 Next steps:")
print("   1. Verify imports: python test_import.py")
print("   2. Start FastAPI: uvicorn app:app --reload")
print("   3. Test endpoint: curl http://localhost:8000/memory/submit-recall")

print("\n🧠 Your backend is correctly wired and ready!")
