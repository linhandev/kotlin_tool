#!/usr/bin/env python3
"""
Step 4: Differential Fuzzing Pipeline
Generate Kotlin code, compile with both 2.2.20 and 2.0.0, run and compare outputs
Keep only failed tests (where outputs differ or one crashes)
Use multi-threading for scalability
"""

import os
import sys
import subprocess
import json
import random
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

BASE_DIR = Path(__file__).parent.absolute()
EXPERIMENTS_DIR = BASE_DIR / "experiments" / "step4_results"
KOTLINC_2_2_20 = BASE_DIR / "kotlin-compilers" / "kotlinc-2.2.20" / "bin" / "kotlinc"
KOTLIN_2_2_20 = BASE_DIR / "kotlin-compilers" / "kotlinc-2.2.20" / "bin" / "kotlin"
KOTLINC_2_0_0 = BASE_DIR / "kotlin-compilers" / "kotlinc-2.0.0" / "bin" / "kotlinc"
KOTLIN_2_0_0 = BASE_DIR / "kotlin-compilers" / "kotlinc-2.0.0" / "bin" / "kotlin"

NUM_SAMPLES = 50   # Number of test cases to generate
MAX_WORKERS = 4    # Number of parallel threads
COMPILE_TIMEOUT = 20  # seconds
RUN_TIMEOUT = 5       # seconds

# Thread-safe counter
lock = threading.Lock()
stats = {
    "generated": 0,
    "compile_220_success": 0,
    "compile_220_failed": 0,
    "compile_200_success": 0,
    "compile_200_failed": 0,
    "both_compiled": 0,
    "run_220_success": 0,
    "run_220_failed": 0,
    "run_200_success": 0,
    "run_200_failed": 0,
    "output_match": 0,
    "output_differ": 0,
    "failures_saved": 0
}


class ComplexCodeGenerator:
    """Generate complex Kotlin code with print statements for observability"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load code generation templates"""
        return [
            self._template_collections,
            self._template_generics,
            self._template_lambdas,
            self._template_classes,
            self._template_operators,
            self._template_when,
            self._template_sequences,
            self._template_null_safety,
            self._template_delegation,
            self._template_sealed_class,
        ]
    
    def generate(self, idx):
        """Generate a random Kotlin program"""
        template = self.templates[idx % len(self.templates)]
        return template(idx)
    
    def _template_collections(self, idx):
        ops = random.randint(3, 8)
        return f"""
fun main() {{
    println("Collections Test {idx}")
    val numbers = (1..{random.randint(10, 30)}).toList()
    println("Original: ${{numbers.take(5)}}")
    
    val result = numbers
        .filter {{ it % 2 == 0 }}
        .map {{ it * {random.randint(2, 5)} }}
        .take({random.randint(3, 10)})
    println("Filtered and mapped: $result")
    
    val sum = result.sum()
    println("Sum: $sum")
    
    val grouped = numbers.groupBy {{ it % {random.randint(2, 5)} }}
    println("Grouped by modulo: ${{grouped.keys}}")
    
    println("Test {idx} completed")
}}
"""
    
    def _template_generics(self, idx):
        return f"""
class Box<T>(val value: T) {{
    fun get(): T = value
    override fun toString() = "Box($value)"
}}

fun <T> createBox(value: T): Box<T> = Box(value)

fun <T, R> Box<T>.map(f: (T) -> R): Box<R> = Box(f(value))

fun main() {{
    println("Generics Test {idx}")
    
    val intBox = createBox({random.randint(1, 100)})
    println("Int box: $intBox")
    
    val doubled = intBox.map {{ it * 2 }}
    println("Doubled: $doubled")
    
    val stringBox = createBox("Hello")
    println("String box: $stringBox")
    
    val upperBox = stringBox.map {{ it.uppercase() }}
    println("Upper: $upperBox")
    
    println("Test {idx} completed")
}}
"""
    
    def _template_lambdas(self, idx):
        return f"""
fun operate(a: Int, b: Int, op: (Int, Int) -> Int): Int = op(a, b)

fun main() {{
    println("Lambda Test {idx}")
    
    val add = {{ x: Int, y: Int -> x + y }}
    val multiply = {{ x: Int, y: Int -> x * y }}
    
    val a = {random.randint(1, 20)}
    val b = {random.randint(1, 20)}
    
    println("a = $a, b = $b")
    println("add: ${{operate(a, b, add)}}")
    println("multiply: ${{operate(a, b, multiply)}}")
    
    val numbers = listOf({', '.join(str(random.randint(1, 50)) for _ in range(5))})
    val transformed = numbers.map {{ it * 2 }}.filter {{ it > {random.randint(10, 30)} }}
    println("Transformed: $transformed")
    
    println("Test {idx} completed")
}}
"""
    
    def _template_classes(self, idx):
        return f"""
data class Person(val name: String, val age: Int) {{
    fun greet() = "Hello, I'm $name"
    fun isAdult() = age >= 18
}}

fun main() {{
    println("Classes Test {idx}")
    
    val person1 = Person("Alice", {random.randint(18, 60)})
    val person2 = Person("Bob", {random.randint(18, 60)})
    
    println("Person 1: $person1")
    println("Greeting: ${{person1.greet()}}")
    println("Is adult: ${{person1.isAdult()}}")
    
    println("Person 2: $person2")
    println("Is adult: ${{person2.isAdult()}}")
    
    val people = listOf(person1, person2)
    val adults = people.filter {{ it.isAdult() }}
    println("Adults: ${{adults.size}}")
    
    println("Test {idx} completed")
}}
"""
    
    def _template_operators(self, idx):
        return f"""
data class Vector(val x: Int, val y: Int) {{
    operator fun plus(other: Vector) = Vector(x + other.x, y + other.y)
    operator fun times(scalar: Int) = Vector(x * scalar, y * scalar)
    override fun toString() = "($x, $y)"
}}

fun main() {{
    println("Operators Test {idx}")
    
    val v1 = Vector({random.randint(1, 10)}, {random.randint(1, 10)})
    val v2 = Vector({random.randint(1, 10)}, {random.randint(1, 10)})
    
    println("v1: $v1")
    println("v2: $v2")
    
    val v3 = v1 + v2
    println("v1 + v2: $v3")
    
    val v4 = v1 * {random.randint(2, 5)}
    println("v1 * scalar: $v4")
    
    println("Test {idx} completed")
}}
"""
    
    def _template_when(self, idx):
        return f"""
sealed class Result {{
    data class Success(val value: Int) : Result()
    data class Error(val message: String) : Result()
    object Loading : Result()
}}

fun process(result: Result): String = when (result) {{
    is Result.Success -> "Success: ${{result.value}}"
    is Result.Error -> "Error: ${{result.message}}"
    Result.Loading -> "Loading..."
}}

fun main() {{
    println("When Test {idx}")
    
    val results = listOf(
        Result.Success({random.randint(1, 100)}),
        Result.Error("Failed"),
        Result.Loading
    )
    
    results.forEach {{
        println(process(it))
    }}
    
    println("Test {idx} completed")
}}
"""
    
    def _template_sequences(self, idx):
        size = random.randint(20, 50)
        return f"""
fun main() {{
    println("Sequences Test {idx}")
    
    val sequence = generateSequence(1) {{ it + 1 }}
        .take({size})
        .filter {{ it % 2 == 0 }}
        .map {{ it * it }}
        .toList()
    
    println("Sequence length: ${{sequence.size}}")
    println("First few: ${{sequence.take(5)}}")
    println("Sum: ${{sequence.sum()}}")
    
    println("Test {idx} completed")
}}
"""
    
    def _template_null_safety(self, idx):
        return f"""
fun findValue(id: Int): String? = if (id > 0) "Value$id" else null

fun main() {{
    println("Null Safety Test {idx}")
    
    val ids = listOf({', '.join(str(random.randint(-5, 10)) for _ in range(5))})
    
    ids.forEach {{ id ->
        val value = findValue(id)
        println("ID $id: ${{value ?: "null"}}")
    }}
    
    val values = ids.mapNotNull {{ findValue(it) }}
    println("Non-null values: $values")
    
    println("Test {idx} completed")
}}
"""
    
    def _template_delegation(self, idx):
        return f"""
interface Printer {{
    fun print(message: String)
}}

class ConsolePrinter : Printer {{
    override fun print(message: String) {{
        println("Console: $message")
    }}
}}

class Logger(printer: Printer) : Printer by printer {{
    fun log(message: String) {{
        print("LOG: $message")
    }}
}}

fun main() {{
    println("Delegation Test {idx}")
    
    val logger = Logger(ConsolePrinter())
    logger.log("Message {idx}")
    logger.print("Direct print")
    
    println("Test {idx} completed")
}}
"""
    
    def _template_sealed_class(self, idx):
        return f"""
sealed class Expr {{
    data class Const(val value: Int) : Expr()
    data class Add(val left: Expr, val right: Expr) : Expr()
    data class Mul(val left: Expr, val right: Expr) : Expr()
}}

fun eval(expr: Expr): Int = when (expr) {{
    is Expr.Const -> expr.value
    is Expr.Add -> eval(expr.left) + eval(expr.right)
    is Expr.Mul -> eval(expr.left) * eval(expr.right)
}}

fun main() {{
    println("Sealed Class Test {idx}")
    
    val expr = Expr.Add(
        Expr.Const({random.randint(1, 10)}),
        Expr.Mul(Expr.Const({random.randint(1, 10)}), Expr.Const({random.randint(1, 10)}))
    )
    
    val result = eval(expr)
    println("Expression result: $result")
    
    println("Test {idx} completed")
}}
"""


class DifferentialTester:
    """Run differential testing between two Kotlin versions"""
    
    def __init__(self, test_id, code):
        self.test_id = test_id
        self.code = code
        self.work_dir = EXPERIMENTS_DIR / "temp" / f"test_{test_id}"
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        self.kt_file = self.work_dir / "Test.kt"
        self.jar_220 = self.work_dir / "test_220.jar"
        self.jar_200 = self.work_dir / "test_200.jar"
        
        self.result = {
            "test_id": test_id,
            "compile_220": None,
            "compile_200": None,
            "run_220": None,
            "run_200": None,
            "output_220": None,
            "output_200": None,
            "match": None,
            "failure_reason": None
        }
    
    def run(self):
        """Execute the full differential test"""
        # Write code
        self.kt_file.write_text(self.code)
        
        # Compile with 2.2.20
        compile_220_ok = self._compile(KOTLINC_2_2_20, self.jar_220, "220")
        with lock:
            if compile_220_ok:
                stats["compile_220_success"] += 1
            else:
                stats["compile_220_failed"] += 1
        
        # Compile with 2.0.0
        compile_200_ok = self._compile(KOTLINC_2_0_0, self.jar_200, "200")
        with lock:
            if compile_200_ok:
                stats["compile_200_success"] += 1
            else:
                stats["compile_200_failed"] += 1
        
        # Only run if both compiled successfully
        if compile_220_ok and compile_200_ok:
            with lock:
                stats["both_compiled"] += 1
            
            # Run with 2.2.20
            run_220_ok, output_220 = self._run(self.jar_220, KOTLIN_2_2_20, "220")
            self.result["run_220"] = run_220_ok
            self.result["output_220"] = output_220
            
            with lock:
                if run_220_ok:
                    stats["run_220_success"] += 1
                else:
                    stats["run_220_failed"] += 1
            
            # Run with 2.0.0
            run_200_ok, output_200 = self._run(self.jar_200, KOTLIN_2_0_0, "200")
            self.result["run_200"] = run_200_ok
            self.result["output_200"] = output_200
            
            with lock:
                if run_200_ok:
                    stats["run_200_success"] += 1
                else:
                    stats["run_200_failed"] += 1
            
            # Compare results
            if run_220_ok != run_200_ok:
                self.result["match"] = False
                self.result["failure_reason"] = "One version crashed, other didn't"
                return False
            elif run_220_ok and run_200_ok:
                if output_220 == output_200:
                    self.result["match"] = True
                    with lock:
                        stats["output_match"] += 1
                    # Clean up - test passed
                    self._cleanup()
                    return True
                else:
                    self.result["match"] = False
                    self.result["failure_reason"] = "Output differs"
                    with lock:
                        stats["output_differ"] += 1
                    return False
            else:
                # Both failed - consider this a match (both failed similarly)
                self.result["match"] = True
                self._cleanup()
                return True
        else:
            # Compilation failed in at least one version
            if compile_220_ok != compile_200_ok:
                self.result["match"] = False
                self.result["failure_reason"] = "Compilation difference"
                return False
            else:
                # Both failed to compile - consider match
                self.result["match"] = True
                self._cleanup()
                return True
    
    def _compile(self, kotlinc, jar_path, version):
        """Compile the Kotlin code"""
        try:
            cmd = [str(kotlinc), str(self.kt_file), "-d", str(jar_path)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=COMPILE_TIMEOUT
            )
            
            success = result.returncode == 0
            self.result[f"compile_{version}"] = {
                "success": success,
                "stderr": result.stderr[:500] if not success else None
            }
            return success
        except subprocess.TimeoutExpired:
            self.result[f"compile_{version}"] = {
                "success": False,
                "stderr": "Compilation timeout"
            }
            return False
        except Exception as e:
            self.result[f"compile_{version}"] = {
                "success": False,
                "stderr": str(e)
            }
            return False
    
    def _run(self, jar_path, kotlin_bin, version):
        """Run the compiled code"""
        try:
            cmd = [str(kotlin_bin), "-cp", str(jar_path), "TestKt"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=RUN_TIMEOUT
            )
            
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            
            return success, output
        except subprocess.TimeoutExpired:
            return False, "Execution timeout"
        except Exception as e:
            return False, str(e)
    
    def _cleanup(self):
        """Remove temporary files for passed tests"""
        try:
            shutil.rmtree(self.work_dir)
        except:
            pass
    
    def save_failure(self):
        """Save failure artifacts"""
        failure_dir = EXPERIMENTS_DIR / "failures" / f"test_{self.test_id}"
        failure_dir.mkdir(parents=True, exist_ok=True)
        
        # Save code
        shutil.copy(self.kt_file, failure_dir / "Test.kt")
        
        # Save result metadata
        with open(failure_dir / "result.json", 'w') as f:
            json.dump(self.result, f, indent=2)
        
        # Save outputs if available
        if self.result["output_220"]:
            (failure_dir / "output_220.txt").write_text(self.result["output_220"])
        if self.result["output_200"]:
            (failure_dir / "output_200.txt").write_text(self.result["output_200"])
        
        with lock:
            stats["failures_saved"] += 1


def run_test(test_id, code):
    """Run a single differential test"""
    tester = DifferentialTester(test_id, code)
    passed = tester.run()
    
    if not passed:
        tester.save_failure()
    
    return test_id, passed, tester.result


def main():
    print("="*60)
    print("Step 4: Differential Fuzzing Pipeline")
    print("="*60)
    
    # Setup
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    (EXPERIMENTS_DIR / "failures").mkdir(exist_ok=True)
    (EXPERIMENTS_DIR / "temp").mkdir(exist_ok=True)
    
    generator = ComplexCodeGenerator()
    
    print(f"\nGenerating and testing {NUM_SAMPLES} samples...")
    print(f"Using {MAX_WORKERS} worker threads\n")
    
    # Generate test cases
    test_cases = []
    for i in range(NUM_SAMPLES):
        code = generator.generate(i)
        test_cases.append((i, code))
        with lock:
            stats["generated"] += 1
    
    # Run tests in parallel
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(run_test, tid, code): tid for tid, code in test_cases}
        
        for future in as_completed(futures):
            test_id, passed, result = future.result()
            results.append(result)
            
            status = "✓ PASS" if passed else "✗ FAIL"
            if test_id % 10 == 0 or not passed:
                print(f"Test {test_id:3d}: {status}")
    
    # Clean up temp directory
    try:
        shutil.rmtree(EXPERIMENTS_DIR / "temp")
    except:
        pass
    
    # Generate report
    print(f"\n{'='*60}")
    print("DIFFERENTIAL FUZZING RESULTS")
    print(f"{'='*60}")
    print(f"Generated: {stats['generated']}")
    print(f"\nCompilation:")
    print(f"  2.2.20 Success: {stats['compile_220_success']}")
    print(f"  2.2.20 Failed:  {stats['compile_220_failed']}")
    print(f"  2.0.0 Success:  {stats['compile_200_success']}")
    print(f"  2.0.0 Failed:   {stats['compile_200_failed']}")
    print(f"  Both Compiled:  {stats['both_compiled']}")
    print(f"\nExecution:")
    print(f"  2.2.20 Success: {stats['run_220_success']}")
    print(f"  2.2.20 Failed:  {stats['run_220_failed']}")
    print(f"  2.0.0 Success:  {stats['run_200_success']}")
    print(f"  2.0.0 Failed:   {stats['run_200_failed']}")
    print(f"\nComparison:")
    print(f"  Output Match:   {stats['output_match']}")
    print(f"  Output Differ:  {stats['output_differ']}")
    print(f"  Failures Saved: {stats['failures_saved']}")
    print(f"{'='*60}")
    
    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "num_samples": NUM_SAMPLES,
        "num_workers": MAX_WORKERS,
        "statistics": stats,
        "failed_tests": [r for r in results if r["match"] == False]
    }
    
    summary_file = EXPERIMENTS_DIR / "summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✓ Summary saved to: {summary_file}")
    print(f"✓ Failed test artifacts saved to: {EXPERIMENTS_DIR / 'failures'}")
    
    if stats["failures_saved"] > 0:
        print(f"\n⚠ Found {stats['failures_saved']} differences between versions!")
    else:
        print(f"\n✓ All tests passed! No differences found.")


if __name__ == "__main__":
    main()
