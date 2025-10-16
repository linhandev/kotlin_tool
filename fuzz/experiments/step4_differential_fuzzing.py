#!/usr/bin/env python3
"""
Step 4: Differential Fuzzing Pipeline

This script implements differential testing between Kotlin 2.2.20 and 2.0.0.
It generates random Kotlin code, compiles with both versions, runs both binaries,
and looks for differences in:
- Compilation success/failure
- Runtime crashes
- Output differences

Only tests that show differences are kept for analysis.
Tests are executed sequentially to avoid resource conflicts.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from step2_refined_generator import RefinedKotlinGenerator, Scope
from pathlib import Path
import subprocess
import tempfile
import shutil
import json
import hashlib
from typing import Tuple, Optional, Dict
from dataclasses import dataclass
import time


@dataclass
class CompilationResult:
    """Result of compiling Kotlin code"""
    success: bool
    error: str
    output_file: Optional[Path]
    compile_time: float


@dataclass
class ExecutionResult:
    """Result of executing compiled Kotlin code"""
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    crashed: bool
    timeout: bool
    execution_time: float


@dataclass
class DifferentialTestResult:
    """Result of differential testing"""
    test_id: str
    code: str
    kotlin_220_compile: CompilationResult
    kotlin_200_compile: CompilationResult
    kotlin_220_exec: Optional[ExecutionResult]
    kotlin_200_exec: Optional[ExecutionResult]
    has_difference: bool
    difference_type: str  # "compilation", "crash", "output", "none"
    difference_details: str


class DifferentialFuzzer:
    """Differential fuzzing between Kotlin versions"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        
        # Kotlin compiler paths
        self.kotlin_220 = "kotlinc"  # System kotlinc 2.2.20
        self.kotlin_200 = "/home/runner/kotlin-2.0.0/kotlinc/bin/kotlinc"
        
        self.failed_tests_dir = self.output_dir / "failed_tests"
        self.failed_tests_dir.mkdir(exist_ok=True)
        
        self.stats = {
            "total_tests": 0,
            "compilation_differences": 0,
            "crash_differences": 0,
            "output_differences": 0,
            "no_differences": 0,
        }
    
    def generate_test_code(self, complexity: str = "medium") -> str:
        """Generate Kotlin code with print statements for observability"""
        generator = RefinedKotlinGenerator.from_complexity(complexity)
        
        # Temporarily modify generator to add more print statements
        original_generate = generator.generate_print_statement
        
        def enhanced_print():
            # Generate print with meaningful output
            var = generator.get_random_variable()
            if var and var[1] in ['Int', 'String', 'Boolean', 'Double', 'Long']:
                return f'{generator.indent()}println("DEBUG: {var[0]} = ${{{var[0]}}}")'
            return f'{generator.indent()}println("DEBUG: checkpoint")'
        
        generator.generate_print_statement = enhanced_print
        code = generator.generate()
        
        return code
    
    def compile_kotlin(
        self,
        code: str,
        compiler_path: str,
        timeout: int = 30
    ) -> CompilationResult:
        """Compile Kotlin code with specified compiler"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            kt_file = tmpdir_path / "test.kt"
            kt_file.write_text(code)
            
            start_time = time.time()
            try:
                result = subprocess.run(
                    [compiler_path, str(kt_file), "-include-runtime", "-d", str(tmpdir_path / "test.jar")],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=tmpdir
                )
                compile_time = time.time() - start_time
                
                success = result.returncode == 0
                jar_file = tmpdir_path / "test.jar"
                
                # Copy jar to persistent location if successful
                output_file = None
                if success and jar_file.exists():
                    # Create unique temp file
                    output_file = Path(tempfile.mktemp(suffix=".jar"))
                    shutil.copy(jar_file, output_file)
                
                return CompilationResult(
                    success=success,
                    error=result.stderr,
                    output_file=output_file,
                    compile_time=compile_time
                )
                
            except subprocess.TimeoutExpired:
                compile_time = time.time() - start_time
                return CompilationResult(
                    success=False,
                    error="Compilation timeout",
                    output_file=None,
                    compile_time=compile_time
                )
            except Exception as e:
                compile_time = time.time() - start_time
                return CompilationResult(
                    success=False,
                    error=f"Compilation error: {str(e)}",
                    output_file=None,
                    compile_time=compile_time
                )
    
    def execute_jar(
        self,
        jar_file: Path,
        timeout: int = 10
    ) -> ExecutionResult:
        """Execute compiled JAR file"""
        start_time = time.time()
        try:
            result = subprocess.run(
                ["java", "-jar", str(jar_file)],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                crashed=result.returncode != 0,
                timeout=False,
                execution_time=execution_time
            )
            
        except subprocess.TimeoutExpired as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                stdout=e.stdout.decode() if e.stdout else "",
                stderr=e.stderr.decode() if e.stderr else "",
                exit_code=-1,
                crashed=False,
                timeout=True,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                crashed=True,
                timeout=False,
                execution_time=execution_time
            )
    
    def compare_results(
        self,
        test_id: str,
        code: str,
        compile_220: CompilationResult,
        compile_200: CompilationResult,
        exec_220: Optional[ExecutionResult],
        exec_200: Optional[ExecutionResult]
    ) -> DifferentialTestResult:
        """Compare results and determine if there's a difference"""
        
        has_difference = False
        difference_type = "none"
        difference_details = ""
        
        # Check compilation differences
        if compile_220.success != compile_200.success:
            has_difference = True
            difference_type = "compilation"
            if compile_220.success and not compile_200.success:
                difference_details = "Compiles on 2.2.20 but fails on 2.0.0"
            else:
                difference_details = "Compiles on 2.0.0 but fails on 2.2.20"
        
        # If both compiled successfully, check execution
        elif compile_220.success and compile_200.success and exec_220 and exec_200:
            # Check for crash differences
            if exec_220.crashed != exec_200.crashed:
                has_difference = True
                difference_type = "crash"
                if exec_220.crashed:
                    difference_details = "Crashes on 2.2.20 but not on 2.0.0"
                else:
                    difference_details = "Crashes on 2.0.0 but not on 2.2.20"
            
            # Check for timeout differences
            elif exec_220.timeout != exec_200.timeout:
                has_difference = True
                difference_type = "timeout"
                if exec_220.timeout:
                    difference_details = "Times out on 2.2.20 but not on 2.0.0"
                else:
                    difference_details = "Times out on 2.0.0 but not on 2.2.20"
            
            # Check for output differences
            elif exec_220.stdout != exec_200.stdout:
                has_difference = True
                difference_type = "output"
                difference_details = "Different stdout output"
            
            elif exec_220.exit_code != exec_200.exit_code:
                has_difference = True
                difference_type = "exit_code"
                difference_details = f"Different exit codes: 2.2.20={exec_220.exit_code}, 2.0.0={exec_200.exit_code}"
        
        return DifferentialTestResult(
            test_id=test_id,
            code=code,
            kotlin_220_compile=compile_220,
            kotlin_200_compile=compile_200,
            kotlin_220_exec=exec_220,
            kotlin_200_exec=exec_200,
            has_difference=has_difference,
            difference_type=difference_type,
            difference_details=difference_details
        )
    
    def save_failed_test(self, result: DifferentialTestResult):
        """Save failed test case for analysis"""
        test_dir = self.failed_tests_dir / result.test_id
        test_dir.mkdir(exist_ok=True)
        
        # Save source code
        (test_dir / "test.kt").write_text(result.code)
        
        # Save compilation results
        compile_info = {
            "kotlin_220": {
                "success": result.kotlin_220_compile.success,
                "error": result.kotlin_220_compile.error,
                "compile_time": result.kotlin_220_compile.compile_time
            },
            "kotlin_200": {
                "success": result.kotlin_200_compile.success,
                "error": result.kotlin_200_compile.error,
                "compile_time": result.kotlin_200_compile.compile_time
            }
        }
        (test_dir / "compilation.json").write_text(json.dumps(compile_info, indent=2))
        
        # Save execution results if available
        if result.kotlin_220_exec:
            exec_220_info = {
                "success": result.kotlin_220_exec.success,
                "stdout": result.kotlin_220_exec.stdout,
                "stderr": result.kotlin_220_exec.stderr,
                "exit_code": result.kotlin_220_exec.exit_code,
                "crashed": result.kotlin_220_exec.crashed,
                "timeout": result.kotlin_220_exec.timeout,
                "execution_time": result.kotlin_220_exec.execution_time
            }
            (test_dir / "execution_220.json").write_text(json.dumps(exec_220_info, indent=2))
        
        if result.kotlin_200_exec:
            exec_200_info = {
                "success": result.kotlin_200_exec.success,
                "stdout": result.kotlin_200_exec.stdout,
                "stderr": result.kotlin_200_exec.stderr,
                "exit_code": result.kotlin_200_exec.exit_code,
                "crashed": result.kotlin_200_exec.crashed,
                "timeout": result.kotlin_200_exec.timeout,
                "execution_time": result.kotlin_200_exec.execution_time
            }
            (test_dir / "execution_200.json").write_text(json.dumps(exec_200_info, indent=2))
        
        # Save difference summary
        summary = {
            "test_id": result.test_id,
            "difference_type": result.difference_type,
            "difference_details": result.difference_details
        }
        (test_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    
    def run_differential_test(self, test_num: int, complexity: str = "medium") -> DifferentialTestResult:
        """Run a single differential test"""
        test_id = f"test_{test_num:06d}"
        
        # Generate code
        code = self.generate_test_code(complexity)
        
        # Compile with both versions
        compile_220 = self.compile_kotlin(code, self.kotlin_220)
        compile_200 = self.compile_kotlin(code, self.kotlin_200)
        
        # Execute if both compiled successfully
        exec_220 = None
        exec_200 = None
        
        if compile_220.success and compile_220.output_file:
            exec_220 = self.execute_jar(compile_220.output_file)
            compile_220.output_file.unlink()  # Clean up
        
        if compile_200.success and compile_200.output_file:
            exec_200 = self.execute_jar(compile_200.output_file)
            compile_200.output_file.unlink()  # Clean up
        
        # Compare results
        result = self.compare_results(
            test_id, code, compile_220, compile_200, exec_220, exec_200
        )
        
        # Update stats
        self.stats["total_tests"] += 1
        if result.has_difference:
            if result.difference_type == "compilation":
                self.stats["compilation_differences"] += 1
            elif result.difference_type in ["crash", "timeout"]:
                self.stats["crash_differences"] += 1
            elif result.difference_type in ["output", "exit_code"]:
                self.stats["output_differences"] += 1
            
            # Save failed test
            self.save_failed_test(result)
        else:
            self.stats["no_differences"] += 1
        
        return result
    
    def run_fuzzing_campaign(self, num_tests: int = 100, complexity: str = "medium"):
        """Run differential fuzzing campaign"""
        print("=" * 70)
        print("Step 4: Differential Fuzzing Campaign")
        print("=" * 70)
        print(f"Tests: {num_tests}")
        print(f"Complexity: {complexity}")
        print(f"Kotlin 2.2.20: {self.kotlin_220}")
        print(f"Kotlin 2.0.0: {self.kotlin_200}")
        print(f"Output: {self.output_dir}")
        print()
        
        for i in range(num_tests):
            if (i + 1) % 10 == 0:
                print(f"Progress: {i+1}/{num_tests} - Differences found: {self.stats['compilation_differences'] + self.stats['crash_differences'] + self.stats['output_differences']}")
            
            result = self.run_differential_test(i, complexity)
        
        # Print final statistics
        print(f"\n{'='*70}")
        print("Fuzzing Campaign Complete")
        print(f"{'='*70}")
        print(f"Total tests: {self.stats['total_tests']}")
        print(f"Compilation differences: {self.stats['compilation_differences']}")
        print(f"Crash differences: {self.stats['crash_differences']}")
        print(f"Output differences: {self.stats['output_differences']}")
        print(f"No differences: {self.stats['no_differences']}")
        print(f"\nFailed tests saved to: {self.failed_tests_dir}")
        
        # Save statistics
        stats_file = self.output_dir / "statistics.json"
        stats_file.write_text(json.dumps(self.stats, indent=2))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Differential Fuzzing (Step 4)')
    parser.add_argument('--tests', type=int, default=100, help='Number of tests to run')
    parser.add_argument('--complexity', default='medium',
                       choices=['low', 'medium', 'high', 'very_high', 'extreme'])
    parser.add_argument('--output-dir', type=str, default='step4_results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    output_dir = Path(__file__).parent / args.output_dir
    fuzzer = DifferentialFuzzer(output_dir)
    fuzzer.run_fuzzing_campaign(args.tests, args.complexity)


if __name__ == "__main__":
    main()
