#!/usr/bin/env python3
"""
Test script to verify integration tests work with the modern pattern server

This script runs specific integration tests that cover the tools implemented
in app_modern_simple.py to ensure backward compatibility.
"""

import subprocess
import sys
import os

def run_tests():
    """Run integration tests that cover our modern pattern implementation"""
    
    # Tools we've implemented in the modern pattern
    implemented_tools = [
        "insert_track",
        "get_track_count", 
        "delete_track",
        "get_track_name",
        "set_track_name",
        "get_track_mute",
        "set_track_mute",
        "api_exists",
        "db_to_slider",
        "slider_to_db"
    ]
    
    print("=" * 80)
    print("TESTING MODERN PATTERN INTEGRATION")
    print("=" * 80)
    print(f"\nImplemented tools ({len(implemented_tools)}):")
    for tool in implemented_tools:
        print(f"  ✓ {tool}")
    
    print("\n" + "-" * 80)
    print("Running relevant integration tests...")
    print("-" * 80 + "\n")
    
    # Test files that cover our implemented tools
    test_files = [
        "tests/test_track_methods.py::test_delete_track",
        "tests/test_track_methods.py::test_track_mute",
        "tests/test_core_api_functions.py::test_api_exists",
        "tests/test_core_api_functions.py::test_db_slider_conversion",
    ]
    
    # Set environment variable to use modern server
    env = os.environ.copy()
    env['USE_MODERN_SERVER'] = '1'
    
    # Run each test
    failed_tests = []
    passed_tests = []
    
    for test in test_files:
        print(f"\nRunning: {test}")
        print("-" * 60)
        
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", test],
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ PASSED: {test}")
            passed_tests.append(test)
        else:
            print(f"❌ FAILED: {test}")
            print(f"Error output:\n{result.stderr}")
            failed_tests.append(test)
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {len(passed_tests)}")
    print(f"❌ Failed: {len(failed_tests)}")
    
    if failed_tests:
        print("\nFailed tests:")
        for test in failed_tests:
            print(f"  - {test}")
        return 1
    else:
        print("\n🎉 All tests passed! Modern pattern is working correctly.")
        return 0

if __name__ == "__main__":
    sys.exit(run_tests())