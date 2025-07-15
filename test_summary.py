#!/usr/bin/env python3

import subprocess
import sys
import re
from pathlib import Path

def run_test_file(test_file):
    """Run a test file and return summary"""
    try:
        cmd = [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Parse output for passed/failed counts
        output = result.stdout + result.stderr
        
        # Look for summary line
        summary_match = re.search(r'(\d+) failed.*?(\d+) passed', output)
        if summary_match:
            failed = int(summary_match.group(1))
            passed = int(summary_match.group(2))
            return {'passed': passed, 'failed': failed, 'total': passed + failed}
        
        # Look for all passed
        passed_match = re.search(r'(\d+) passed', output)
        if passed_match:
            passed = int(passed_match.group(1))
            return {'passed': passed, 'failed': 0, 'total': passed}
        
        # Look for all failed
        failed_match = re.search(r'(\d+) failed', output)
        if failed_match:
            failed = int(failed_match.group(1))
            return {'passed': 0, 'failed': failed, 'total': failed}
            
        # Check if no tests
        if "no tests ran" in output or "collected 0 items" in output:
            return {'passed': 0, 'failed': 0, 'total': 0}
            
        return None
        
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return None

def main():
    test_dir = Path("tests")
    test_files = sorted(test_dir.glob("test_*.py"))
    
    print("REAPER MCP Integration Test Summary")
    print("=" * 80)
    print()
    
    total_passed = 0
    total_failed = 0
    total_tests = 0
    
    results = []
    
    for test_file in test_files:
        print(f"Running {test_file.name}...", end='', flush=True)
        result = run_test_file(test_file)
        
        if result:
            passed = result['passed']
            failed = result['failed']
            total = result['total']
            
            total_passed += passed
            total_failed += failed
            total_tests += total
            
            status = "✓" if failed == 0 else "✗"
            print(f" {status} {passed}/{total} passed")
            
            results.append({
                'file': test_file.name,
                'passed': passed,
                'failed': failed,
                'total': total
            })
        else:
            print(" ⚠ Error or no tests")
            results.append({
                'file': test_file.name,
                'passed': 0,
                'failed': 0,
                'total': 0
            })
    
    print()
    print("=" * 80)
    print("Summary by Test File:")
    print("=" * 80)
    
    for result in sorted(results, key=lambda x: x['failed'], reverse=True):
        if result['total'] > 0:
            pass_rate = (result['passed'] / result['total']) * 100
            status = "PASS" if result['failed'] == 0 else "FAIL"
            print(f"{result['file']:40} {result['passed']:3}/{result['total']:3} ({pass_rate:5.1f}%) [{status}]")
    
    print()
    print("=" * 80)
    if total_tests > 0:
        overall_pass_rate = (total_passed / total_tests) * 100
        print(f"Overall: {total_passed}/{total_tests} tests passed ({overall_pass_rate:.1f}%)")
        print(f"Failed: {total_failed} tests")
    else:
        print("No tests found!")
    print("=" * 80)

if __name__ == "__main__":
    main()