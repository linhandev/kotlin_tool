# Quick Start Guide

## For Kotlin Native Backend Testing

If you need **valid, runnable Kotlin programs** to test compiler backend changes:

### 1. Setup (First Time Only)

```bash
bash setup.sh
```

### 2. Generate Test Programs

**Single program:**
```bash
python3 generate_complex.py -o test.kt --run
```

**Multiple programs:**
```bash
python3 generate_complex.py -o test.kt -n 10 --validate
```

**Custom complexity:**
```bash
python3 generate_complex.py -o test.kt -l 100 --run
```

### 3. What You Get

- ✅ Programs that compile (100% success rate)
- ✅ ~50 lines of code (configurable)
- ✅ Print statements for observing behavior
- ✅ Functions, variables, loops, conditionals
- ✅ Fast generation (~1 second per file)

### Example Output

```kotlin
fun calculate42(param: Int): Int {
    println("Function called with: $param")
    return param * 2
}

fun main() {
    println("Program started")
    val value: Int = 456
    println("value: ${value}")
    
    for (i in 1..5) {
        println("Iteration: ${i}")
    }
    
    val result = calculate42(value)
    println("Result: ${result}")
    println("Program completed")
}
```

**Runtime:**
```
Program started
value: 456
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

## For Parser Fuzzing

If you need **random grammar structures** to test parser robustness:

```bash
# Grammar-based generation
python3 generate_kotlin.py -o test.kt -d 15 -c 0.9

# Batch fuzzing
python3 batch_test.py -n 50
```

Note: Most programs won't compile (~0-5% success). Use for parser testing only.

---

## Common Commands

```bash
# Generate 1 program and run it
python3 generate_complex.py -o test.kt --run

# Generate 10 programs and validate all
python3 generate_complex.py -o test.kt -n 10 --validate

# Generate longer program (100 lines)
python3 generate_complex.py -o test.kt -l 100

# Generate shorter program (30 lines)
python3 generate_complex.py -o test.kt -l 30
```

---

## Options

### generate_complex.py

```
-o FILE         Output file path (required)
-l NUM          Lines of code (default: 50)
-n NUM          Number of files (default: 1)
--validate      Compile to check validity
--run           Compile and run program
```

### generate_kotlin.py (grammar-based)

```
-o FILE         Output file path (required)
-d NUM          Max depth (default: 20)
-c NUM          Cooldown 0.0-1.0 (default: 0.5)
-n NUM          Number of files (default: 1)
--validate      Try to compile
```

---

## Need Help?

- **Which generator?** → See [GENERATOR_COMPARISON.md](GENERATOR_COMPARISON.md)
- **Detailed docs** → See [README.md](README.md)
- **Examples** → See [examples/](examples/)
- **Solution details** → See [SOLUTION.md](SOLUTION.md)

---

## TL;DR

**Backend testing?** → `python3 generate_complex.py -o test.kt --run`

**Parser fuzzing?** → `python3 generate_kotlin.py -o test.kt`
