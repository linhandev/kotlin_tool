#!/usr/bin/env python3
"""
Differential Fuzzing Pipeline for Kotlin Native Compiler

Generates diverse Kotlin code and compares behavior between two Kotlin Native compiler versions.
Identifies and saves test cases that show differences in compilation or execution behavior.
"""

import argparse
import hashlib
import multiprocessing as mp
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# Import the generator
from generate import generate_diverse_program


@dataclass
class CompilerConfig:
    """Configuration for a Kotlin Native compiler"""
    version: str
    path: Path
    
    def __post_init__(self):
        self.path = Path(self.path).resolve()


@dataclass
class TestResult:
    """Result of a single test case"""
    test_id: str
    source_code: str
    baseline_compiled: bool
    sut_compiled: bool
    baseline_output: Optional[str] = None
    sut_output: Optional[str] = None
    baseline_error: Optional[str] = None
    sut_error: Optional[str] = None
    execution_match: bool = True
    
    def is_interesting(self) -> bool:
        """Check if this test case shows a difference between compilers"""
        # Different compilation results
        if self.baseline_compiled != self.sut_compiled:
            return True
        
        # Both compiled but different outputs
        if self.baseline_compiled and self.sut_compiled:
            if self.baseline_output != self.sut_output:
                return True
        
        return False
    
    def get_summary(self) -> str:
        """Get a summary of the result"""
        if not self.baseline_compiled and not self.sut_compiled:
            return "both_failed"
        elif self.baseline_compiled and self.sut_compiled:
            if self.baseline_output == self.sut_output:
                return "both_passed_match"
            else:
                return "both_passed_differ"
        elif self.baseline_compiled:
            return "baseline_only"
        else:
            return "sut_only"


class KotlinNativeFuzzer:
    """Fuzzer for Kotlin Native compiler"""
    
    def __init__(
        self,
        baseline: CompilerConfig,
        sut: CompilerConfig,
        output_dir: Path,
        num_features: int = 15,
        timeout: int = 30
    ):
        self.baseline = baseline
        self.sut = sut
        self.output_dir = Path(output_dir).resolve()
        self.num_features = num_features
        self.timeout = timeout
        
        # Create output directories
        self.failed_tests_dir = self.output_dir / "failed_tests"
        self.failed_tests_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats_file = self.output_dir / "stats.txt"
    
    def compile_and_run(
        self,
        compiler: CompilerConfig,
        source_file: Path,
        work_dir: Path
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Compile and run a Kotlin file with given compiler.
        
        Returns:
            (compiled_successfully, output, error_message)
        """
        try:
            # Compile
            output_name = "program.kexe"
            output_path = work_dir / output_name
            
            compile_cmd = [
                str(compiler.path / "bin" / "kotlinc-native"),
                str(source_file),
                "-o", str(work_dir / "program")
            ]
            
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=work_dir
            )
            
            if compile_result.returncode != 0:
                return False, None, compile_result.stderr
            
            # Run
            run_cmd = [str(output_path)]
            run_result = subprocess.run(
                run_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=work_dir
            )
            
            return True, run_result.stdout, None
            
        except subprocess.TimeoutExpired:
            return False, None, "Timeout"
        except Exception as e:
            return False, None, str(e)
    
    def test_single_case(self, test_id: int) -> TestResult:
        """Test a single generated program"""
        # Generate code
        source_code = generate_diverse_program(self.num_features)
        
        test_id_str = f"test_{test_id:06d}"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            source_file = tmpdir / "test.kt"
            source_file.write_text(source_code)
            
            # Test with baseline compiler
            baseline_dir = tmpdir / "baseline"
            baseline_dir.mkdir()
            baseline_compiled, baseline_output, baseline_error = self.compile_and_run(
                self.baseline, source_file, baseline_dir
            )
            
            # Test with SUT compiler
            sut_dir = tmpdir / "sut"
            sut_dir.mkdir()
            sut_compiled, sut_output, sut_error = self.compile_and_run(
                self.sut, source_file, sut_dir
            )
            
            result = TestResult(
                test_id=test_id_str,
                source_code=source_code,
                baseline_compiled=baseline_compiled,
                sut_compiled=sut_compiled,
                baseline_output=baseline_output,
                sut_output=sut_output,
                baseline_error=baseline_error,
                sut_error=sut_error,
                execution_match=(baseline_output == sut_output) if (baseline_compiled and sut_compiled) else True
            )
            
            # Save interesting test cases
            if result.is_interesting():
                self.save_failed_test(result)
            
            return result
    
    def save_failed_test(self, result: TestResult):
        """Save a test case that shows differences"""
        # Create test directory
        test_dir = self.failed_tests_dir / result.test_id
        test_dir.mkdir(exist_ok=True)
        
        # Save source code
        (test_dir / "test.kt").write_text(result.source_code)
        
        # Save summary
        summary = [
            f"Test ID: {result.test_id}",
            f"Summary: {result.get_summary()}",
            f"",
            f"Baseline (v{self.baseline.version}): {'COMPILED' if result.baseline_compiled else 'FAILED'}",
            f"SUT (v{self.sut.version}): {'COMPILED' if result.sut_compiled else 'FAILED'}",
            f""
        ]
        
        if result.baseline_compiled:
            summary.append("=== Baseline Output ===")
            summary.append(result.baseline_output or "(empty)")
            summary.append("")
        else:
            summary.append("=== Baseline Error ===")
            summary.append(result.baseline_error or "(no error message)")
            summary.append("")
        
        if result.sut_compiled:
            summary.append("=== SUT Output ===")
            summary.append(result.sut_output or "(empty)")
            summary.append("")
        else:
            summary.append("=== SUT Error ===")
            summary.append(result.sut_error or "(no error message)")
            summary.append("")
        
        (test_dir / "summary.txt").write_text("\n".join(summary))
    
    def run_fuzzing(self, num_tests: int, num_workers: int = 1) -> dict:
        """Run fuzzing campaign"""
        print(f"Starting fuzzing campaign:")
        print(f"  Tests: {num_tests}")
        print(f"  Workers: {num_workers}")
        print(f"  Baseline: Kotlin Native {self.baseline.version}")
        print(f"  SUT: Kotlin Native {self.sut.version}")
        print(f"  Output: {self.output_dir}")
        print()
        
        start_time = time.time()
        
        if num_workers == 1:
            # Single-threaded
            results = [self.test_single_case(i) for i in range(num_tests)]
        else:
            # Multi-threaded
            with mp.Pool(num_workers) as pool:
                results = pool.map(self.test_single_case, range(num_tests))
        
        elapsed = time.time() - start_time
        
        # Collect statistics
        stats = {
            'total': num_tests,
            'both_compiled': sum(1 for r in results if r.baseline_compiled and r.sut_compiled),
            'both_failed': sum(1 for r in results if not r.baseline_compiled and not r.sut_compiled),
            'baseline_only': sum(1 for r in results if r.baseline_compiled and not r.sut_compiled),
            'sut_only': sum(1 for r in results if not r.baseline_compiled and r.sut_compiled),
            'output_differ': sum(1 for r in results if r.baseline_compiled and r.sut_compiled and r.baseline_output != r.sut_output),
            'interesting': sum(1 for r in results if r.is_interesting()),
            'elapsed': elapsed
        }
        
        # Save statistics
        self.save_stats(stats)
        
        # Print statistics
        self.print_stats(stats)
        
        return stats
    
    def save_stats(self, stats: dict):
        """Save statistics to file"""
        lines = [
            f"Fuzzing Campaign Statistics",
            f"Generated: {datetime.now().isoformat()}",
            f"",
            f"Configuration:",
            f"  Baseline: Kotlin Native {self.baseline.version}",
            f"  SUT: Kotlin Native {self.sut.version}",
            f"  Features per test: {self.num_features}",
            f"",
            f"Results:",
            f"  Total tests: {stats['total']}",
            f"  Both compiled: {stats['both_compiled']} ({100*stats['both_compiled']/stats['total']:.1f}%)",
            f"  Both failed: {stats['both_failed']} ({100*stats['both_failed']/stats['total']:.1f}%)",
            f"  Baseline only: {stats['baseline_only']}",
            f"  SUT only: {stats['sut_only']}",
            f"  Output differs: {stats['output_differ']}",
            f"  Interesting cases: {stats['interesting']} ({100*stats['interesting']/stats['total']:.1f}%)",
            f"",
            f"Performance:",
            f"  Elapsed time: {stats['elapsed']:.1f}s",
            f"  Tests per second: {stats['total']/stats['elapsed']:.2f}",
            f""
        ]
        
        self.stats_file.write_text("\n".join(lines))
    
    def print_stats(self, stats: dict):
        """Print statistics to console"""
        print("\n" + "="*60)
        print("Fuzzing Campaign Results")
        print("="*60)
        print(f"Total tests: {stats['total']}")
        print(f"  Both compiled: {stats['both_compiled']} ({100*stats['both_compiled']/stats['total']:.1f}%)")
        print(f"  Both failed: {stats['both_failed']} ({100*stats['both_failed']/stats['total']:.1f}%)")
        print(f"  Baseline only compiled: {stats['baseline_only']}")
        print(f"  SUT only compiled: {stats['sut_only']}")
        print(f"  Output differs: {stats['output_differ']}")
        print(f"  Interesting cases: {stats['interesting']} ({100*stats['interesting']/stats['total']:.1f}%)")
        print(f"\nElapsed time: {stats['elapsed']:.1f}s")
        print(f"Tests per second: {stats['total']/stats['elapsed']:.2f}")
        print(f"\nFailed tests saved to: {self.failed_tests_dir}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Differential fuzzing for Kotlin Native compiler'
    )
    parser.add_argument('--baseline', default='/usr/local/kotlinc-2.0.0',
                       help='Path to baseline Kotlin Native compiler (default: v2.0.0)')
    parser.add_argument('--sut', default='/usr/local/kotlinc-2.2.20',
                       help='Path to SUT Kotlin Native compiler (default: v2.2.20)')
    parser.add_argument('-n', '--num-tests', type=int, default=100,
                       help='Number of tests to run (default: 100)')
    parser.add_argument('-f', '--features', type=int, default=15,
                       help='Number of features per program (default: 15)')
    parser.add_argument('-w', '--workers', type=int, default=mp.cpu_count(),
                       help=f'Number of worker processes (default: {mp.cpu_count()})')
    parser.add_argument('-o', '--output', default='fuzz_results',
                       help='Output directory (default: fuzz_results)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Timeout per test in seconds (default: 30)')
    
    args = parser.parse_args()
    
    # Verify compilers exist
    baseline_path = Path(args.baseline)
    sut_path = Path(args.sut)
    
    if not (baseline_path / "bin" / "kotlinc-native").exists():
        print(f"Error: Baseline compiler not found at {baseline_path}")
        print(f"Expected: {baseline_path / 'bin' / 'kotlinc-native'}")
        return 1
    
    if not (sut_path / "bin" / "kotlinc-native").exists():
        print(f"Error: SUT compiler not found at {sut_path}")
        print(f"Expected: {sut_path / 'bin' / 'kotlinc-native'}")
        return 1
    
    # Create fuzzer
    baseline = CompilerConfig(version="2.0.0", path=baseline_path)
    sut = CompilerConfig(version="2.2.20", path=sut_path)
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    fuzzer = KotlinNativeFuzzer(
        baseline=baseline,
        sut=sut,
        output_dir=output_dir,
        num_features=args.features,
        timeout=args.timeout
    )
    
    # Run fuzzing
    try:
        fuzzer.run_fuzzing(args.num_tests, args.workers)
    except KeyboardInterrupt:
        print("\nFuzzing interrupted by user")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
