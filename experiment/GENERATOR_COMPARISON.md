# Generator Comparison Guide

## Quick Recommendation

**Testing Kotlin Native Compiler Backend?** → Use `generate_complex.py`

**Testing Parser/Fuzzing Kotlin Tooling?** → Use `generate_kotlin.py`

## Detailed Comparison

### generate_complex.py (Template-Based)

**Purpose**: Generate semantically valid, runnable Kotlin programs

**Compilation Rate**: 100% ✅

**Output Characteristics**:
- ~50 lines of code (configurable)
- Print statements throughout
- Valid variable declarations
- Working control flow (if/else, loops, when)
- Function definitions and calls
- List/collection operations
- Actual runnable programs

**Best For**:
- Backend compiler testing
- Correctness validation
- Behavioral testing
- Performance benchmarking
- Regression testing

**Example Command**:
```bash
python3 generate_complex.py -o test.kt -l 50 --run
```

**Example Output**:
```kotlin
fun calculate42(param: Int): Int {
    println("Function called with: $param")
    return param * 2
}

fun main() {
    println("Program started")
    val value: Int = 456
    
    if (value > 0) {
        println("Value is positive: ${value}")
    }
    
    for (i in 1..5) {
        println("Iteration: ${i}")
    }
    
    val result = calculate42(value)
    println("Result: ${result}")
    println("Program completed")
}
```

**Runtime Output**:
```
Program started
Value is positive: 456
Iteration: 1
Iteration: 2
Iteration: 3
Iteration: 4
Iteration: 5
Function called with: 456
Result: 912
Program completed
```

---

### generate_kotlin.py (Grammar-Based)

**Purpose**: Generate syntactically valid structures from grammar

**Compilation Rate**: ~0-5% ❌

**Output Characteristics**:
- Follows grammar rules exactly
- Often semantically invalid
- May have undefined references
- Random nesting of constructs
- Variable length (usually short)

**Best For**:
- Parser robustness testing
- Grammar validation
- Compiler fuzzing
- Finding edge cases in tooling

**Example Command**:
```bash
python3 generate_kotlin.py -o test.kt -d 15 -c 0.9
```

**Example Output**:
```kotlin
@file:data<*,>()
packageinternal
fun(){abstractget():(open)&suspend}
```

**Compilation**: Usually fails with semantic errors

---

## Feature Matrix

| Feature | generate_complex.py | generate_kotlin.py |
|---------|--------------------|--------------------|
| **Compilation Success** | 100% | ~0-5% |
| **Semantic Validity** | ✅ Valid | ❌ Often invalid |
| **Print Statements** | ✅ Many | ⚠️ Rare |
| **Runnable** | ✅ Yes | ❌ Rarely |
| **LOC Control** | ✅ ~50 LOC | ⚠️ Variable |
| **Generation Speed** | Fast (~1s) | Fast (~1s) |
| **Functions** | ✅ 2-3 valid | ⚠️ May be invalid |
| **Variables** | ✅ 4-7 valid | ⚠️ May be invalid |
| **Control Flow** | ✅ Working | ⚠️ May be broken |
| **Observability** | ✅ High | ❌ Low |

---

## Use Case Scenarios

### Scenario 1: Testing Backend Compiler Changes

**Situation**: You modified the Kotlin Native compiler backend and need to verify it generates correct executables.

**Use**: `generate_complex.py`

**Why**: Need programs that compile and run successfully to observe backend behavior.

```bash
# Generate 20 test programs
python3 generate_complex.py -o tests/test.kt -n 20 -l 60 --validate

# Run each to verify correct execution
python3 generate_complex.py -o tests/program.kt --run
```

---

### Scenario 2: Parser Fuzzing

**Situation**: Testing if the Kotlin parser can handle unusual grammar constructs.

**Use**: `generate_kotlin.py`

**Why**: Need syntactically valid but semantically weird code to stress-test the parser.

```bash
# Generate many random syntactic structures
python3 batch_test.py -n 100
```

---

### Scenario 3: Regression Testing

**Situation**: Need a large test suite to ensure compiler changes don't break existing functionality.

**Use**: `generate_complex.py`

**Why**: Need many valid programs that compile and run consistently.

```bash
# Generate 100 regression tests
python3 generate_complex.py -o regression/test.kt -n 100 --validate
```

---

### Scenario 4: Performance Benchmarking

**Situation**: Comparing compilation/execution speed of compiler versions.

**Use**: `generate_complex.py`

**Why**: Need valid programs that actually compile and run for meaningful benchmarks.

```bash
# Generate benchmark suite
python3 generate_complex.py -o benchmarks/bench.kt -n 50 -l 100
```

---

## Quick Start

### For Backend Testing (Most Common)

```bash
# Single program
python3 generate_complex.py -o test.kt --run

# Multiple programs
python3 generate_complex.py -o test.kt -n 10 --validate

# Custom complexity
python3 generate_complex.py -o test.kt -l 100 --run
```

### For Parser Fuzzing

```bash
# Single file
python3 generate_kotlin.py -o test.kt -d 15 -c 0.9

# Batch testing
python3 batch_test.py -n 50
```

---

## Summary

| Your Goal | Use This |
|-----------|----------|
| Test compiler backend | `generate_complex.py` |
| Test with valid programs | `generate_complex.py` |
| Need print statements | `generate_complex.py` |
| Need runnable code | `generate_complex.py` |
| Observe program behavior | `generate_complex.py` |
| Test parser robustness | `generate_kotlin.py` |
| Fuzz compiler | `generate_kotlin.py` |
| Find edge cases | `generate_kotlin.py` |

**Bottom line**: If your changes are in the compiler backend and you need programs that actually work, use `generate_complex.py`.
