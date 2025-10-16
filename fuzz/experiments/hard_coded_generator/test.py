#!/usr/bin/env python3
"""
Comprehensive Test Suite

Runs 30-minute compilation test to verify code generator quality.
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Tuple
import subprocess
import tempfile
import time
import sys

sys.path.insert(0, str(Path(__file__).parent))
from generator import KotlinGenerator


def compile_kotlin(code: str, timeout: int = 10) -> Tuple[bool, str]:
    """Compile Kotlin code and return (success, error)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        kt_file = tmpdir_path / "test.kt"
        kt_file.write_text(code)
        
        try:
            result = subprocess.run(
                ["kotlinc", str(kt_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir
            )
            return result.returncode == 0, result.stderr
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)


def run_compilation_test(duration_minutes: int = 30, complexity: Tuple[int, int] = (5, 20)) -> None:
    """Run comprehensive compilation test"""
    print("=" * 70)
    print(f"Comprehensive Compilation Test ({duration_minutes} minutes)")
    print("=" * 70)
    print(f"Complexity: depth={complexity[0]}, statements={complexity[1]}")
    print()
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    total = 0
    success = 0
    failed: List[Tuple[int, str]] = []
    
    while time.time() < end_time:
        total += 1
        
        generator = KotlinGenerator(max_depth=complexity[0], max_statements=complexity[1])
        code = generator.generate()
        
        ok, error = compile_kotlin(code)
        if ok:
            success += 1
        else:
            failed.append((total, error[:100]))
        
        if total % 10 == 0:
            elapsed_min = (time.time() - start_time) / 60
            success_rate = (success / total) * 100 if total > 0 else 0
            print(f"[{elapsed_min:.1f}m] Tests: {total}, Success: {success} ({success_rate:.1f}%)")
    
    elapsed = time.time() - start_time
    success_rate = (success / total) * 100 if total > 0 else 0
    
    print(f"\n{'='*70}")
    print("Test Complete")
    print(f"{'='*70}")
    print(f"Duration: {elapsed/60:.1f} minutes")
    print(f"Total tests: {total}")
    print(f"Success: {success} ({success_rate:.1f}%)")
    print(f"Failed: {len(failed)}")
    
    if failed and len(failed) <= 10:
        print(f"\nFirst errors:")
        for idx, err in failed[:5]:
            print(f"  Test {idx}: {err}")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description='Comprehensive Test')
    parser.add_argument('--duration', type=int, default=30, help='Duration in minutes')
    parser.add_argument('--depth', type=int, default=5)
    parser.add_argument('--statements', type=int, default=20)
    
    args = parser.parse_args()
    
    run_compilation_test(args.duration, (args.depth, args.statements))


if __name__ == "__main__":
    main()
