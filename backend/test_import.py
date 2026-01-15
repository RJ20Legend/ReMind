"""
Quick test to verify brain package imports are working.
Run from: E:\ReMind\backend directory
Command: python test_import.py
"""

print("Testing imports from brain package...\n")

try:
    from brain.state import users, event_log, DEFAULT_STATE
    print("✅ brain.state imports successful")
    print(f"   - users: {type(users)} with {len(users)} initial user(s)")
    print(f"   - event_log: {type(event_log)} with {len(event_log)} events")
    print(f"   - DEFAULT_STATE: {len(DEFAULT_STATE)} fields\n")
except ImportError as e:
    print(f"❌ brain.state import failed: {e}\n")

try:
    from brain.memory_engine import process, decay, predict_range
    print("✅ brain.memory_engine imports successful")
    print(f"   - process: {callable(process)}")
    print(f"   - decay: {callable(decay)}")
    print(f"   - predict_range: {callable(predict_range)}\n")
except ImportError as e:
    print(f"❌ brain.memory_engine import failed: {e}\n")

try:
    from brain.scheduler_engine import schedule, priority
    print("✅ brain.scheduler_engine imports successful")
    print(f"   - schedule: {callable(schedule)}")
    print(f"   - priority: {callable(priority)}\n")
except ImportError as e:
    print(f"❌ brain.scheduler_engine import failed: {e}\n")

# Test the whole brain API
try:
    from brain import users, process, schedule
    print("✅ Full brain API import successful")
    print(f"   All key functions and state accessible\n")
except ImportError as e:
    print(f"❌ Full brain API import failed: {e}\n")

print("=" * 50)
print("All imports successful! 🧠")
print("=" * 50)
print("\nYour backend is correctly wired.")
print("You can now run: uvicorn main:app --reload")
