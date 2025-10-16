#!/usr/bin/env python3
"""
Differential Fuzzing Pipeline

Compares Kotlin 2.2.20 vs 2.0.0 compilation and execution.
Parallelizes all stages except actual program execution.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import subprocess
import tempfile
import shutil
import json
import time
import sys
import os

sys.path.insert(0, str(Path(__file__).parent))
from generator import KotlinGenerator


@dataclass
class CompileResult:
    success: bool
    error: str
    jar_path: Optional[Path]
    time_sec: float


@dataclass
class ExecResult:
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    crashed: bool
    timeout: bool
    time_sec: float


@dataclass
class TestResult:
    test_id: str
    code: str
    compile_220: CompileResult
    compile_200: CompileResult
    exec_220: Optional[ExecResult]
    exec_200: Optional[ExecResult]
    has_diff: bool
    diff_type: str
    diff_details: str


class DifferentialFuzzer:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        
        self.kotlin_220 = "kotlinc"
        self.kotlin_200 = "/home/runner/kotlin-2.0.0/kotlinc/bin/kotlinc"
        
        self.failed_dir = self.output_dir / "failed_tests"
        self.failed_dir.mkdir(exist_ok=True)
        
        self.stats = {
            "total": 0,
            "compilation_diff": 0,
            "crash_diff": 0,
            "output_diff": 0,
            "no_diff": 0,
        }
    
    @staticmethod
    def _compile(code: str, compiler: str, timeout: int = 30) -> CompileResult:
        """Compile Kotlin code"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            kt_file = tmpdir_path / "test.kt"
            kt_file.write_text(code)
            jar_file = tmpdir_path / "test.jar"
            
            start = time.time()
            try:
                result = subprocess.run(
                    [compiler, str(kt_file), "-include-runtime", "-d", str(jar_file)],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=tmpdir
                )
                elapsed = time.time() - start
                
                success = result.returncode == 0
                out_jar = None
                if success and jar_file.exists():
                    out_jar = Path(tempfile.mktemp(suffix=".jar"))
                    shutil.copy(jar_file, out_jar)
                
                return CompileResult(success, result.stderr, out_jar, elapsed)
            except subprocess.TimeoutExpired:
                return CompileResult(False, "Compilation timeout", None, time.time() - start)
            except Exception as e:
                return CompileResult(False, f"Error: {e}", None, time.time() - start)
    
    @staticmethod
    def _execute(jar: Path, timeout: int = 10) -> ExecResult:
        """Execute compiled JAR"""
        start = time.time()
        try:
            result = subprocess.run(
                ["java", "-jar", str(jar)],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            elapsed = time.time() - start
            
            return ExecResult(
                result.returncode == 0,
                result.stdout,
                result.stderr,
                result.returncode,
                result.returncode != 0,
                False,
                elapsed
            )
        except subprocess.TimeoutExpired as e:
            return ExecResult(
                False,
                e.stdout.decode() if e.stdout else "",
                e.stderr.decode() if e.stderr else "",
                -1,
                False,
                True,
                time.time() - start
            )
        except Exception as e:
            return ExecResult(False, "", str(e), -1, True, False, time.time() - start)
    
    def _compare(
        self,
        test_id: str,
        code: str,
        c220: CompileResult,
        c200: CompileResult,
        e220: Optional[ExecResult],
        e200: Optional[ExecResult]
    ) -> TestResult:
        """Compare results between versions"""
        has_diff = False
        diff_type = "none"
        diff_details = ""
        
        if c220.success != c200.success:
            has_diff = True
            diff_type = "compilation"
            if c220.success:
                diff_details = "Compiles on 2.2.20 but fails on 2.0.0"
            else:
                diff_details = "Compiles on 2.0.0 but fails on 2.2.20"
        
        elif c220.success and c200.success and e220 and e200:
            if e220.crashed != e200.crashed:
                has_diff = True
                diff_type = "crash"
                diff_details = f"Crash on {'2.2.20' if e220.crashed else '2.0.0'} only"
            
            elif e220.timeout != e200.timeout:
                has_diff = True
                diff_type = "timeout"
                diff_details = f"Timeout on {'2.2.20' if e220.timeout else '2.0.0'} only"
            
            elif e220.stdout != e200.stdout:
                has_diff = True
                diff_type = "output"
                diff_details = "Different stdout"
            
            elif e220.exit_code != e200.exit_code:
                has_diff = True
                diff_type = "exit_code"
                diff_details = f"Exit codes: 2.2.20={e220.exit_code}, 2.0.0={e200.exit_code}"
        
        return TestResult(test_id, code, c220, c200, e220, e200, has_diff, diff_type, diff_details)
    
    def _save_failed(self, result: TestResult) -> None:
        """Save test showing differences"""
        test_dir = self.failed_dir / result.test_id
        test_dir.mkdir(exist_ok=True)
        
        (test_dir / "test.kt").write_text(result.code)
        
        compile_info = {
            "kotlin_220": {
                "success": result.compile_220.success,
                "error": result.compile_220.error,
                "time": result.compile_220.time_sec
            },
            "kotlin_200": {
                "success": result.compile_200.success,
                "error": result.compile_200.error,
                "time": result.compile_200.time_sec
            }
        }
        (test_dir / "compilation.json").write_text(json.dumps(compile_info, indent=2))
        
        if result.exec_220:
            (test_dir / "exec_220.json").write_text(json.dumps({
                "success": result.exec_220.success,
                "stdout": result.exec_220.stdout,
                "stderr": result.exec_220.stderr,
                "exit_code": result.exec_220.exit_code,
                "crashed": result.exec_220.crashed,
                "timeout": result.exec_220.timeout,
                "time": result.exec_220.time_sec
            }, indent=2))
        
        if result.exec_200:
            (test_dir / "exec_200.json").write_text(json.dumps({
                "success": result.exec_200.success,
                "stdout": result.exec_200.stdout,
                "stderr": result.exec_200.stderr,
                "exit_code": result.exec_200.exit_code,
                "crashed": result.exec_200.crashed,
                "timeout": result.exec_200.timeout,
                "time": result.exec_200.time_sec
            }, indent=2))
        
        (test_dir / "summary.json").write_text(json.dumps({
            "test_id": result.test_id,
            "diff_type": result.diff_type,
            "diff_details": result.diff_details
        }, indent=2))
    
    def _run_test(self, test_num: int, complexity: Tuple[int, int]) -> TestResult:
        """Run single differential test (sequential execution)"""
        test_id = f"test_{test_num:06d}"
        
        generator = KotlinGenerator(max_depth=complexity[0], max_statements=complexity[1])
        code = generator.generate()
        
        c220 = self._compile(code, self.kotlin_220)
        c200 = self._compile(code, self.kotlin_200)
        
        e220 = None
        e200 = None
        
        if c220.success and c220.jar_path:
            e220 = self._execute(c220.jar_path)
            c220.jar_path.unlink()
        
        if c200.success and c200.jar_path:
            e200 = self._execute(c200.jar_path)
            c200.jar_path.unlink()
        
        result = self._compare(test_id, code, c220, c200, e220, e200)
        
        self.stats["total"] += 1
        if result.has_diff:
            if result.diff_type == "compilation":
                self.stats["compilation_diff"] += 1
            elif result.diff_type in ["crash", "timeout"]:
                self.stats["crash_diff"] += 1
            elif result.diff_type in ["output", "exit_code"]:
                self.stats["output_diff"] += 1
            self._save_failed(result)
        else:
            self.stats["no_diff"] += 1
        
        return result
    
    def run_campaign(self, num_tests: int = 100, complexity: Tuple[int, int] = (5, 20), parallel: int = 4) -> None:
        """Run fuzzing campaign with parallelized compilation"""
        print("=" * 70)
        print("Differential Fuzzing Campaign")
        print("=" * 70)
        print(f"Tests: {num_tests}")
        print(f"Complexity: depth={complexity[0]}, statements={complexity[1]}")
        print(f"Parallel workers: {parallel}")
        print(f"Output: {self.output_dir}")
        print()
        
        with ProcessPoolExecutor(max_workers=parallel) as executor:
            futures = {executor.submit(self._run_test, i, complexity): i for i in range(num_tests)}
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 10 == 0:
                    diffs = (self.stats['compilation_diff'] + 
                            self.stats['crash_diff'] + 
                            self.stats['output_diff'])
                    print(f"Progress: {completed}/{num_tests} - Differences: {diffs}")
        
        print(f"\n{'='*70}")
        print("Campaign Complete")
        print(f"{'='*70}")
        print(f"Total: {self.stats['total']}")
        print(f"Compilation diffs: {self.stats['compilation_diff']}")
        print(f"Crash diffs: {self.stats['crash_diff']}")
        print(f"Output diffs: {self.stats['output_diff']}")
        print(f"No diffs: {self.stats['no_diff']}")
        print(f"\nFailed tests: {self.failed_dir}")
        
        (self.output_dir / "stats.json").write_text(json.dumps(self.stats, indent=2))


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description='Differential Fuzzing')
    parser.add_argument('--tests', type=int, default=100)
    parser.add_argument('--depth', type=int, default=5)
    parser.add_argument('--statements', type=int, default=20)
    parser.add_argument('--parallel', type=int, default=4)
    parser.add_argument('--output-dir', type=str, default='results')
    
    args = parser.parse_args()
    
    output_dir = Path(__file__).parent.parent / args.output_dir
    fuzzer = DifferentialFuzzer(output_dir)
    fuzzer.run_campaign(args.tests, (args.depth, args.statements), args.parallel)


if __name__ == "__main__":
    main()
