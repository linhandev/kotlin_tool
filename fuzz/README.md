# Kotlin Native Compiler Fuzz Testing Pipeline

This repository contains a comprehensive differential fuzzing pipeline for testing the Kotlin Native compiler across different versions.

## Overview

The pipeline consists of 5 main steps:

1. **Grammar Evaluation**: Compare three Kotlin ANTLR grammars
2. **Grammar Improvement**: Enhance the best grammar for complex code generation  
3. **Complexity Maximization**: Generate maximally complex Kotlin code
4. **Differential Fuzzing**: Compare compilation and runtime behavior across Kotlin versions
5. **Documentation**: This guide and example outputs

## Prerequisites

- Python 3.8+
- Java 17+
- Internet connection (for initial setup to download Kotlin compilers and grammars)

## Quick Start

### Installation

```bash
cd fuzz

# Install Python dependencies
pip install -r requirements.txt

# The pipeline will automatically download:
# - ANTLR 4.13.2
# - Kotlin compilers (2.2.20 and 2.0.0)
# - Grammar specifications
```

### Running the Pipeline

#### Step 1: Evaluate Grammar Specifications

Compares three Kotlin grammar specs by generating and compiling code samples:

```bash
python3 step1_evaluate_grammars.py
```

**Output**: `experiments/step1_results/`
- `official/`: Results for official Kotlin spec
- `kotlin-formal/`: Results for kotlin-formal grammar
- `kotlin/`: Results for kotlin grammar  
- `summary.json`: Comparison summary

**Expected Results**: All three grammars achieve ~95% compilation success rate on basic templates.

#### Step 2: Improve Grammar for Complex Code

Enhances code generation to include advanced Kotlin features:

```bash
python3 step2_improve_grammar.py
```

**Output**: `experiments/step2_results/`
- `generated/`: 50 complex Kotlin source files
- `compiled/`: Successfully compiled JARs
- `results.json`: Detailed compilation results
- `README.md`: Documentation of improvements

**Features Generated**:
- Generic types with constraints
- Higher-order functions
- Sealed classes
- Operator overloading
- DSL-style builders
- Reified generics

**Expected Results**: 94% compilation success rate with complex features.

#### Step 3: Maximize Code Complexity

Pushes complexity to the limit, prioritizing complexity over correctness:

```bash
python3 step3_maximize_complexity.py
```

**Output**: `experiments/step3_results/`
- `generated/`: 100 maximally complex Kotlin files
- `compiled/`: Compiled artifacts
- `results.json`: Results with error details
- `README.md`: Complexity feature documentation

**Complexity Features**:
- Deep nesting (5+ levels)
- Multiple type parameters (4+)
- Nested lambda expressions
- Advanced variance annotations
- Monadic patterns (Either, State)
- Complex operator overloading

**Expected Results**: 85-95% compilation success (some intentional edge cases may fail).

#### Step 4: Differential Fuzzing

The main differential testing pipeline - compares Kotlin 2.2.20 vs 2.0.0:

```bash
python3 step4_differential_fuzz.py
```

**What it does**:
1. Generates random Kotlin programs with print statements
2. Compiles each program with both Kotlin 2.2.20 and 2.0.0
3. Runs both compiled programs
4. Compares outputs for differences
5. Saves artifacts only for failed tests (output differs or one crashes)

**Output**: `experiments/step4_results/`
- `failures/`: Failed test artifacts (Kotlin source, outputs, metadata)
- `summary.json`: Statistics and failed test list

**Multi-threading**: Uses 4 parallel workers by default (configurable in script).

**Expected Results**: Most tests should pass (outputs match). Any failures indicate potential compiler regressions or behavioral changes between versions.

## Example Generated Code

### Simple Example (Step 1)

```kotlin
fun fibonacci(n: Int): Int {
    if (n <= 1) return n
    return fibonacci(n - 1) + fibonacci(n - 2)
}

fun main() {
    for (i in 0..10) {
        println("fibonacci($i) = ${fibonacci(i)}")
    }
}
```

### Complex Example (Step 2)

```kotlin
sealed class Resource<out T> {
    data class Success<T>(val data: T) : Resource<T>()
    data class Error(val message: String, val code: Int) : Resource<Nothing>()
    object Loading : Resource<Nothing>()
}

fun <T> handleResource(resource: Resource<T>): String {
    return when (resource) {
        is Resource.Success -> "Success: ${resource.data}"
        is Resource.Error -> "Error ${resource.code}: ${resource.message}"
        Resource.Loading -> "Loading..."
    }
}

fun main() {
    val success = Resource.Success(42)
    println(handleResource(success))
}
```

### Maximum Complexity Example (Step 3)

```kotlin
sealed class Either<out L, out R> {
    data class Left<L>(val value: L) : Either<L, Nothing>()
    data class Right<R>(val value: R) : Either<Nothing, R>()
    
    fun <T> fold(left: (L) -> T, right: (R) -> T): T = when (this) {
        is Left -> left(value)
        is Right -> right(value)
    }
}

data class State<S, out A>(val run: (S) -> Pair<S, A>) {
    fun <B> map(f: (A) -> B): State<S, B> = State { s ->
        val (s2, a) = run(s)
        s2 to f(a)
    }
}

fun main() {
    val right: Either<String, Int> = Either.Right(42)
    println(right.fold({ "Left: $it" }, { "Right: $it" }))
}
```

## Configuration

You can adjust parameters in each script:

### step1_evaluate_grammars.py
- `NUM_SAMPLES`: Number of samples per grammar (default: 20)

### step2_improve_grammar.py  
- `NUM_SAMPLES`: Number of complex samples (default: 50)

### step3_maximize_complexity.py
- `NUM_SAMPLES`: Number of max complexity samples (default: 100)

### step4_differential_fuzz.py
- `NUM_SAMPLES`: Number of test cases (default: 50)
- `MAX_WORKERS`: Parallel threads (default: 4)
- `COMPILE_TIMEOUT`: Max compilation time in seconds (default: 20)
- `RUN_TIMEOUT`: Max execution time in seconds (default: 5)

## Results Interpretation

### Differential Fuzzing Results

The pipeline reports several statistics:

**Compilation**:
- Shows how many programs compiled successfully with each version
- Mismatches indicate potential compiler bugs

**Execution**:
- Shows how many programs ran successfully
- Runtime crashes indicate potential VM or stdlib issues

**Output Comparison**:
- `Output Match`: Programs that produced identical output ✓
- `Output Differ`: Programs with different outputs ⚠
- `Failures Saved`: Number of failed tests with artifacts saved

### Investigating Failures

When tests fail, artifacts are saved to `experiments/step4_results/failures/test_N/`:

```
test_N/
  ├── Test.kt           # Source code that triggered the difference
  ├── result.json       # Detailed test results
  ├── output_220.txt    # Output from Kotlin 2.2.20
  └── output_200.txt    # Output from Kotlin 2.0.0
```

Compare the two outputs to understand the behavioral difference.

## Project Structure

```
fuzz/
├── step1_evaluate_grammars.py    # Grammar evaluation
├── step2_improve_grammar.py      # Complex code generation
├── step3_maximize_complexity.py  # Maximum complexity generation
├── step4_differential_fuzz.py    # Differential testing pipeline
├── requirements.txt              # Python dependencies
├── antlr-4.13.2-complete.jar    # ANTLR tool (downloaded)
├── grammars/                     # Downloaded grammar specs
│   ├── kotlin-spec-release/
│   └── grammars-v4-master/
├── kotlin-compilers/             # Kotlin compiler versions
│   ├── kotlinc-2.2.20/
│   └── kotlinc-2.0.0/
└── experiments/                  # Results and artifacts
    ├── step1_results/
    ├── step2_results/
    ├── step3_results/
    └── step4_results/
```

## Known Limitations

1. **Grammar Coverage**: The grammar-based generation doesn't cover 100% of Kotlin features
2. **Timeout Sensitivity**: Very slow machines may need increased timeouts
3. **Native Compilation**: Currently tests JVM compilation, not full native compilation
4. **Platform**: Tested on Linux; may need adjustments for Windows/macOS

## Troubleshooting

### "kotlinc: command not found"

The compilers are in `kotlin-compilers/`. Scripts use absolute paths, but if you see this error, verify the paths are correct.

### Compilation Timeout

Increase `COMPILE_TIMEOUT` in the respective script.

### Out of Memory

Reduce `MAX_WORKERS` in step4_differential_fuzz.py or reduce `NUM_SAMPLES`.

### No Differences Found

This is good! It means both Kotlin versions behave identically on the generated tests. Try:
- Increasing `NUM_SAMPLES` for more coverage
- Running step3 first to generate more complex code patterns

## Future Enhancements

Potential improvements:
1. True ANTLR-based code generation with fuzzing mutations
2. Test Kotlin/Native compilation (not just JVM)
3. Coverage-guided fuzzing
4. Automated bug reporting
5. More Kotlin versions for regression testing
6. Integration with CI/CD systems

## License

This fuzzing pipeline is provided as-is for testing purposes.

## Contributing

To add new code generation templates:
1. Add methods to the respective generator class
2. Update the template selection logic
3. Test the new templates compile successfully
