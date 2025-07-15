#!/usr/bin/env python
"""Run a subset of tests that have been updated to use robust utilities"""

import subprocess
import sys

# Tests that have been updated with robust utilities
updated_tests = [
    "tests/test_fx_operations.py",
    "tests/test_automation_operations.py", 
    "tests/test_track_methods.py",
    "tests/test_midi_operations.py",
    "tests/test_media_items.py",
    "tests/test_envelope_operations.py"
]

print("Running updated tests that use robust utilities...\n")

for test_file in updated_tests:
    print(f"\n{'='*60}")
    print(f"Running: {test_file}")
    print(f"{'='*60}")
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode != 0:
        print(f"\n❌ {test_file} FAILED")
    else:
        print(f"\n✅ {test_file} PASSED")

print("\n" + "="*60)
print("Summary of updated tests complete")