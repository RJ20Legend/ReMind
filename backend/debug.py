"""
Debug script to verify the brain package is working.
Run from: E:\ReMind\backend
Command: python debug.py
"""

print("🧠 Brain Debug Script")
print("=" * 60)
print()

# Test 1: Direct state import
print("1️⃣ Testing: from brain.state import users")
try:
    from brain.state import users
    print(f"   ✅ Success! users = {users}")
    print(f"   ✅ Type: {type(users)}")
    print(f"   ✅ Keys: {list(users.keys())}")
except ImportError as e:
    print(f"   ❌ Failed: {e}")
    print()
    print("⚠️  FIX: Make sure you're running from E:\\ReMind\\backend")
    print("   Run: cd E:\\ReMind\\backend")
    print("   Then: python debug.py")
    exit(1)

print()

# Test 2: Process function import
print("2️⃣ Testing: from brain import process")
try:
    from brain import process
    print(f"   ✅ Success! process = {process}")
    print(f"   ✅ Callable: {callable(process)}")
except ImportError as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

print()

# Test 3: Schedule function import
print("3️⃣ Testing: from brain import schedule")
try:
    from brain import schedule
    print(f"   ✅ Success! schedule = {schedule}")
    print(f"   ✅ Callable: {callable(schedule)}")
except ImportError as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

print()

# Test 4: DEFAULT_STATE import
print("4️⃣ Testing: from brain.state import DEFAULT_STATE")
try:
    from brain.state import DEFAULT_STATE
    print(f"   ✅ Success! DEFAULT_STATE has {len(DEFAULT_STATE)} fields")
    print(f"   ✅ Fields: {list(DEFAULT_STATE.keys())[:5]}...")
except ImportError as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

print()
print("=" * 60)
print("✅ All imports successful!")
print("=" * 60)
print()
print("🧠 Your brain is alive and ready!")
print()
print("Next: Start FastAPI")
print("  cd E:\\ReMind\\backend")
print("  uvicorn main:app --reload")
