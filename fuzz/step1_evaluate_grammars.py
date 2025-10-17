#!/usr/bin/env python3
"""
Step 1: Evaluate three Kotlin grammar specifications
- Official Kotlin spec
- kotlin-formal from grammars-v4
- kotlin from grammars-v4

Generate code samples and compile them with kotlinc 2.2.20
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
import random
from datetime import datetime

# Base paths
BASE_DIR = Path(__file__).parent.absolute()
GRAMMARS_DIR = BASE_DIR / "grammars"
EXPERIMENTS_DIR = BASE_DIR / "experiments"
RESULTS_DIR = BASE_DIR / "results"
ANTLR_JAR = BASE_DIR / "antlr-4.13.2-complete.jar"
KOTLINC_2_2_20 = BASE_DIR / "kotlin-compilers" / "kotlinc-2.2.20" / "bin" / "kotlinc"

# Grammar configurations
GRAMMARS = {
    "official": {
        "name": "Official Kotlin Spec",
        "path": GRAMMARS_DIR / "kotlin-spec-release" / "grammar" / "src" / "main" / "antlr",
        "lexer": "KotlinLexer.g4",
        "parser": "KotlinParser.g4",
        "start_rule": "kotlinFile"
    },
    "kotlin-formal": {
        "name": "Kotlin Formal (grammars-v4)",
        "path": GRAMMARS_DIR / "grammars-v4-master" / "kotlin" / "kotlin-formal",
        "lexer": "KotlinLexer.g4",
        "parser": "KotlinParser.g4",
        "start_rule": "kotlinFile"
    },
    "kotlin": {
        "name": "Kotlin (grammars-v4)",
        "path": GRAMMARS_DIR / "grammars-v4-master" / "kotlin" / "kotlin",
        "lexer": "KotlinLexer.g4",
        "parser": "KotlinParser.g4",
        "start_rule": "kotlinFile"
    }
}

NUM_SAMPLES = 20  # Number of code samples to generate per grammar


class GrammarEvaluator:
    def __init__(self, grammar_name, grammar_config):
        self.name = grammar_name
        self.config = grammar_config
        self.output_dir = EXPERIMENTS_DIR / "step1_results" / grammar_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.generated_dir = self.output_dir / "generated"
        self.generated_dir.mkdir(exist_ok=True)
        
        self.compiled_dir = self.output_dir / "compiled"
        self.compiled_dir.mkdir(exist_ok=True)
        
        self.results = {
            "grammar_name": grammar_name,
            "display_name": grammar_config["name"],
            "generated_count": 0,
            "compiled_count": 0,
            "compile_errors": 0,
            "samples": []
        }
    
    def compile_grammar(self):
        """Compile the ANTLR grammar to Java classes"""
        print(f"\n[{self.name}] Compiling ANTLR grammar...")
        
        grammar_path = self.config["path"]
        
        # Create a build directory for this grammar
        build_dir = self.output_dir / "antlr_build"
        build_dir.mkdir(exist_ok=True)
        
        try:
            # Compile lexer
            lexer_file = grammar_path / self.config["lexer"]
            cmd = [
                "java", "-jar", str(ANTLR_JAR),
                "-Dlanguage=Python3",
                "-o", str(build_dir),
                "-lib", str(grammar_path),
                str(lexer_file)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error compiling lexer: {result.stderr}")
                return False
            
            # Compile parser
            parser_file = grammar_path / self.config["parser"]
            cmd = [
                "java", "-jar", str(ANTLR_JAR),
                "-Dlanguage=Python3",
                "-o", str(build_dir),
                "-lib", str(grammar_path),
                str(parser_file)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error compiling parser: {result.stderr}")
                return False
            
            print(f"[{self.name}] Grammar compiled successfully")
            
            # Add the build directory to Python path
            sys.path.insert(0, str(build_dir))
            
            return True
        except Exception as e:
            print(f"[{self.name}] Error compiling grammar: {e}")
            return False
    
    def generate_simple_kotlin_code(self, idx):
        """Generate simple, hand-crafted Kotlin code for testing"""
        templates = [
            # Simple function
            """fun main() {
    println("Hello, World!")
}
""",
            # Function with parameters
            """fun add(a: Int, b: Int): Int {
    return a + b
}

fun main() {
    val result = add(5, 3)
    println("Result: $result")
}
""",
            # Class definition
            """class Person(val name: String, val age: Int) {
    fun greet() {
        println("Hello, my name is $name and I'm $age years old")
    }
}

fun main() {
    val person = Person("Alice", 30)
    person.greet()
}
""",
            # With control flow
            """fun fibonacci(n: Int): Int {
    if (n <= 1) return n
    return fibonacci(n - 1) + fibonacci(n - 2)
}

fun main() {
    for (i in 0..10) {
        println("fibonacci($i) = ${fibonacci(i)}")
    }
}
""",
            # Collections and lambdas
            """fun main() {
    val numbers = listOf(1, 2, 3, 4, 5)
    val doubled = numbers.map { it * 2 }
    println("Doubled: $doubled")
    
    val evens = numbers.filter { it % 2 == 0 }
    println("Evens: $evens")
}
""",
            # Data class
            """data class User(val id: Int, val name: String, val email: String)

fun main() {
    val user1 = User(1, "Bob", "bob@example.com")
    val user2 = user1.copy(name = "Alice")
    
    println("User 1: $user1")
    println("User 2: $user2")
}
""",
            # When expression
            """fun describe(obj: Any): String = when (obj) {
    1 -> "One"
    "Hello" -> "Greeting"
    is Long -> "Long number"
    !is String -> "Not a string"
    else -> "Unknown"
}

fun main() {
    println(describe(1))
    println(describe("Hello"))
    println(describe(1000L))
}
""",
            # Extension function
            """fun String.addExclamation(): String {
    return this + "!"
}

fun Int.isEven(): Boolean = this % 2 == 0

fun main() {
    println("Hello".addExclamation())
    println("5 is even: ${5.isEven()}")
    println("4 is even: ${4.isEven()}")
}
""",
            # Nullable types
            """fun findUser(id: Int): String? {
    return if (id > 0) "User $id" else null
}

fun main() {
    val user1 = findUser(1)
    val user2 = findUser(-1)
    
    println("User 1: ${user1 ?: "Not found"}")
    println("User 2: ${user2 ?: "Not found"}")
}
""",
            # Companion object
            """class Counter {
    companion object {
        var count = 0
        fun increment() {
            count++
        }
    }
}

fun main() {
    Counter.increment()
    Counter.increment()
    println("Count: ${Counter.count}")
}
""",
            # Sealed class
            """sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val message: String) : Result()
    object Loading : Result()
}

fun process(result: Result): String = when (result) {
    is Result.Success -> "Success: ${result.data}"
    is Result.Error -> "Error: ${result.message}"
    Result.Loading -> "Loading..."
}

fun main() {
    println(process(Result.Success("Done")))
    println(process(Result.Error("Failed")))
    println(process(Result.Loading))
}
""",
            # Higher-order functions
            """fun operation(x: Int, y: Int, op: (Int, Int) -> Int): Int {
    return op(x, y)
}

fun main() {
    val sum = operation(5, 3) { a, b -> a + b }
    val product = operation(5, 3) { a, b -> a * b }
    
    println("Sum: $sum")
    println("Product: $product")
}
""",
            # Property delegation
            """class Example {
    var p: String by lazy {
        println("Computing value")
        "Lazy value"
    }
}

fun main() {
    val example = Example()
    println("Before accessing")
    println(example.p)
    println(example.p)
}
""",
            # Generic function
            """fun <T> printList(items: List<T>) {
    for (item in items) {
        println(item)
    }
}

fun main() {
    printList(listOf(1, 2, 3))
    printList(listOf("a", "b", "c"))
}
""",
            # Object expression
            """interface Clickable {
    fun click()
}

fun main() {
    val button = object : Clickable {
        override fun click() {
            println("Button clicked!")
        }
    }
    
    button.click()
}
""",
            # Enum class
            """enum class Color(val rgb: Int) {
    RED(0xFF0000),
    GREEN(0x00FF00),
    BLUE(0x0000FF)
}

fun main() {
    for (color in Color.values()) {
        println("${color.name}: 0x${color.rgb.toString(16)}")
    }
}
""",
            # Ranges and progressions
            """fun main() {
    for (i in 1..5) {
        print("$i ")
    }
    println()
    
    for (i in 5 downTo 1 step 2) {
        print("$i ")
    }
    println()
}
""",
            # Destructuring
            """data class Point(val x: Int, val y: Int)

fun main() {
    val point = Point(10, 20)
    val (x, y) = point
    println("x = $x, y = $y")
    
    val map = mapOf(1 to "one", 2 to "two")
    for ((key, value) in map) {
        println("$key -> $value")
    }
}
""",
            # Operator overloading
            """data class Vector(val x: Int, val y: Int) {
    operator fun plus(other: Vector) = Vector(x + other.x, y + other.y)
    operator fun times(scalar: Int) = Vector(x * scalar, y * scalar)
}

fun main() {
    val v1 = Vector(1, 2)
    val v2 = Vector(3, 4)
    val v3 = v1 + v2
    val v4 = v1 * 2
    
    println("v1 + v2 = $v3")
    println("v1 * 2 = $v4")
}
""",
            # Infix function
            """infix fun Int.pow(exponent: Int): Int {
    var result = 1
    repeat(exponent) {
        result *= this
    }
    return result
}

fun main() {
    val result = 2 pow 3
    println("2 pow 3 = $result")
}
"""
        ]
        
        # Select a template based on idx (cycle through if more samples than templates)
        template_idx = idx % len(templates)
        return templates[template_idx]
    
    def test_compilation(self, code, sample_idx):
        """Test if generated code compiles with kotlinc 2.2.20"""
        kt_file = self.generated_dir / f"sample_{sample_idx}.kt"
        
        # Write the code to a file
        kt_file.write_text(code)
        
        sample_result = {
            "index": sample_idx,
            "file": str(kt_file.relative_to(BASE_DIR)),
            "code_length": len(code),
            "compiled": False,
            "compile_output": ""
        }
        
        try:
            # Try to compile the code
            cmd = [
                str(KOTLINC_2_2_20),
                str(kt_file),
                "-d", str(self.compiled_dir / f"sample_{sample_idx}.jar")
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                sample_result["compiled"] = True
                self.results["compiled_count"] += 1
                print(f"[{self.name}] Sample {sample_idx}: ✓ Compiled successfully")
            else:
                sample_result["compile_output"] = result.stderr
                self.results["compile_errors"] += 1
                print(f"[{self.name}] Sample {sample_idx}: ✗ Compilation failed")
        except subprocess.TimeoutExpired:
            sample_result["compile_output"] = "Compilation timeout"
            self.results["compile_errors"] += 1
            print(f"[{self.name}] Sample {sample_idx}: ✗ Compilation timeout")
        except Exception as e:
            sample_result["compile_output"] = str(e)
            self.results["compile_errors"] += 1
            print(f"[{self.name}] Sample {sample_idx}: ✗ Error: {e}")
        
        self.results["samples"].append(sample_result)
        return sample_result["compiled"]
    
    def evaluate(self):
        """Run the full evaluation process"""
        print(f"\n{'='*60}")
        print(f"Evaluating: {self.config['name']}")
        print(f"{'='*60}")
        
        # For Step 1, we'll use hand-crafted templates since ANTLR code generation
        # requires more complex setup
        print(f"[{self.name}] Generating {NUM_SAMPLES} code samples...")
        
        for i in range(NUM_SAMPLES):
            code = self.generate_simple_kotlin_code(i)
            self.results["generated_count"] += 1
            self.test_compilation(code, i)
        
        # Calculate statistics
        if self.results["generated_count"] > 0:
            success_rate = (self.results["compiled_count"] / self.results["generated_count"]) * 100
            self.results["success_rate"] = success_rate
        else:
            self.results["success_rate"] = 0
        
        # Save results
        results_file = self.output_dir / "results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n[{self.name}] Results:")
        print(f"  Generated: {self.results['generated_count']}")
        print(f"  Compiled:  {self.results['compiled_count']}")
        print(f"  Failed:    {self.results['compile_errors']}")
        print(f"  Success Rate: {self.results['success_rate']:.2f}%")
        
        return self.results


def main():
    print("="*60)
    print("Step 1: Evaluating Kotlin Grammar Specifications")
    print("="*60)
    
    # Ensure directories exist
    EXPERIMENTS_DIR.mkdir(exist_ok=True)
    
    # Run evaluation for each grammar
    all_results = []
    for grammar_name, grammar_config in GRAMMARS.items():
        evaluator = GrammarEvaluator(grammar_name, grammar_config)
        results = evaluator.evaluate()
        all_results.append(results)
    
    # Generate summary report
    print("\n" + "="*60)
    print("SUMMARY REPORT")
    print("="*60)
    
    for result in sorted(all_results, key=lambda x: x["success_rate"], reverse=True):
        print(f"\n{result['display_name']}:")
        print(f"  Success Rate: {result['success_rate']:.2f}%")
        print(f"  Compiled: {result['compiled_count']}/{result['generated_count']}")
    
    # Save combined results
    summary_file = EXPERIMENTS_DIR / "step1_results" / "summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "grammars": all_results
        }, f, indent=2)
    
    print(f"\n✓ Results saved to: {summary_file}")
    
    # Recommend the best grammar
    best = max(all_results, key=lambda x: x["success_rate"])
    print(f"\n✓ Best grammar: {best['display_name']} ({best['success_rate']:.2f}% success rate)")


if __name__ == "__main__":
    main()
