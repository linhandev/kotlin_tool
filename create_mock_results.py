#!/usr/bin/env python3
"""
Mock Fuzzer Demo

This demonstrates what the fuzzer would produce if Kotlin Native compilers were installed.
Creates a mock directory structure showing example results.
"""

import os
from pathlib import Path
from generate import generate_diverse_program


def create_mock_results():
    """Create mock fuzzer results directory structure"""
    
    # Create output directory
    output_dir = Path("/tmp/mock_fuzz_results")
    output_dir.mkdir(exist_ok=True)
    
    failed_tests_dir = output_dir / "failed_tests"
    failed_tests_dir.mkdir(exist_ok=True)
    
    print("Creating mock fuzzer results...")
    print(f"Output directory: {output_dir}")
    print()
    
    # Create a few mock test cases
    test_cases = [
        {
            'id': 'test_000042',
            'summary': 'both_passed_differ',
            'description': 'Both compilers succeeded but outputs differ',
            'baseline_compiled': True,
            'sut_compiled': True,
            'baseline_output': '=== Program started ===\nValue: 42\nSum: 15\n=== Completed ===',
            'sut_output': '=== Program started ===\nValue: 43\nSum: 15\n=== Completed ===',
        },
        {
            'id': 'test_000123',
            'summary': 'baseline_only',
            'description': 'Only baseline compiled (regression in SUT)',
            'baseline_compiled': True,
            'sut_compiled': False,
            'baseline_output': '=== Program started ===\nTest passed\n',
            'sut_error': 'error: unresolved reference: someFunction\n  someFunction()\n  ^',
        },
        {
            'id': 'test_000256',
            'summary': 'sut_only',
            'description': 'Only SUT compiled (new feature or fix)',
            'baseline_compiled': False,
            'sut_compiled': True,
            'baseline_error': 'error: unsupported feature: value classes\n',
            'sut_output': '=== Program started ===\nNew feature works!\n',
        },
    ]
    
    for test_case in test_cases:
        test_dir = failed_tests_dir / test_case['id']
        test_dir.mkdir(exist_ok=True)
        
        # Generate and save Kotlin code
        code = generate_diverse_program(12)
        (test_dir / "test.kt").write_text(code)
        
        # Create summary
        summary_lines = [
            f"Test ID: {test_case['id']}",
            f"Summary: {test_case['summary']}",
            f"Description: {test_case['description']}",
            f"",
            f"Baseline (v2.0.0): {'COMPILED' if test_case['baseline_compiled'] else 'FAILED'}",
            f"SUT (v2.2.20): {'COMPILED' if test_case['sut_compiled'] else 'FAILED'}",
            f"",
        ]
        
        if test_case['baseline_compiled']:
            summary_lines.append("=== Baseline Output ===")
            summary_lines.append(test_case.get('baseline_output', ''))
            summary_lines.append("")
        else:
            summary_lines.append("=== Baseline Error ===")
            summary_lines.append(test_case.get('baseline_error', ''))
            summary_lines.append("")
        
        if test_case['sut_compiled']:
            summary_lines.append("=== SUT Output ===")
            summary_lines.append(test_case.get('sut_output', ''))
            summary_lines.append("")
        else:
            summary_lines.append("=== SUT Error ===")
            summary_lines.append(test_case.get('sut_error', ''))
            summary_lines.append("")
        
        (test_dir / "summary.txt").write_text("\n".join(summary_lines))
        
        print(f"✓ Created {test_case['id']}: {test_case['description']}")
    
    # Create stats file
    stats = """Fuzzing Campaign Statistics
Generated: 2025-10-17T16:53:00

Configuration:
  Baseline: Kotlin Native 2.0.0
  SUT: Kotlin Native 2.2.20
  Features per test: 12

Results:
  Total tests: 1000
  Both compiled: 328 (32.8%)
  Both failed: 624 (62.4%)
  Baseline only: 21 (2.1%)
  SUT only: 15 (1.5%)
  Output differs: 12 (1.2%)
  Interesting cases: 48 (4.8%)

Performance:
  Elapsed time: 3245.6s
  Tests per second: 0.31
"""
    
    (output_dir / "stats.txt").write_text(stats)
    print(f"✓ Created stats.txt")
    print()
    
    print("Mock results created successfully!")
    print()
    print("Directory structure:")
    print(f"  {output_dir}/")
    print(f"    ├── failed_tests/")
    for test_case in test_cases:
        print(f"    │   ├── {test_case['id']}/")
        print(f"    │   │   ├── test.kt")
        print(f"    │   │   └── summary.txt")
    print(f"    └── stats.txt")
    print()
    
    print("View results:")
    print(f"  cat {output_dir}/stats.txt")
    print(f"  cat {output_dir}/failed_tests/test_000042/summary.txt")
    print()


if __name__ == '__main__':
    create_mock_results()
