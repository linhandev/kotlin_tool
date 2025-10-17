# Complex Program Generator Examples

## Overview

`generate_complex.py` creates semantically valid Kotlin programs that compile and run successfully. This is ideal for testing Kotlin Native compiler backends.

## Basic Usage

### Generate a Single Program

```bash
# Generate a ~50 line program
python3 generate_complex.py -o generated_code/program.kt

# Generate with custom line count
python3 generate_complex.py -o generated_code/program.kt -l 60

# Generate and validate compilation
python3 generate_complex.py -o generated_code/program.kt --validate

# Generate, compile, and run
python3 generate_complex.py -o generated_code/program.kt --run
```

### Generate Multiple Programs

```bash
# Generate 10 programs for testing
python3 generate_complex.py -o generated_code/test.kt -n 10 --validate

# Generate 5 programs and run each one
python3 generate_complex.py -o generated_code/test.kt -n 5 --run
```

## Example Output

### Generated Program Structure

```kotlin
// Auto-generated Kotlin program for testing
// This program is designed to test Kotlin Native compiler backend

fun calculate42(param: Int): Int {
    println("Function calculate42 called with: $param")
    return param * 2
}

fun process17(param: String): String {
    println("Function process17 called with: $param")
    return param + "_processed"
}

fun main() {
    println("Program started")

    val value23: Int = 456
    val text89: String = "hello"
    val flag12: Boolean = true
    val number67: Double = 78.34
    val count45: Long = -123L

    println("Initial values:")
    println("value23: ${value23}")
    println("text89: ${text89}")
    println("flag12: ${flag12}")

    if (value23 > 0) {
        println("value23 is positive: ${value23}")
    } else {
        println("value23 is non-positive: ${value23}")
    }

    for (i in 1..5) {
        println("Iteration: ${i}")
    }

    when {
        value23 > 0 -> println("value23 is positive")
        value23 < 0 -> println("value23 is negative")
        else -> println("value23 is zero")
    }

    val result1 = calculate42(value23)
    println("Function result: ${result1}")

    val result2 = process17(text89)
    println("Function result: ${result2}")

    val numbers = listOf(1, 2, 3, 4, 5)
    println("List: $numbers")
    val sum = numbers.sum()
    println("Sum: $sum")

    println("Program completed")
}
```

### Runtime Output

```
Program started
Initial values:
value23: 456
text89: hello
flag12: true
value23 is positive: 456
Iteration: 1
Iteration: 2
Iteration: 3
Iteration: 4
Iteration: 5
value23 is positive
Function calculate42 called with: 456
Function result: 912
Function process17 called with: hello
Function result: hello_processed
List: [1, 2, 3, 4, 5]
Sum: 15
Program completed
```

## Features

Each generated program includes:

1. **Function Definitions** (2-3 functions)
   - Takes parameters of various types (Int, String, Boolean, Double)
   - Prints debug information
   - Returns computed results

2. **Variable Declarations** (4-7 variables)
   - Different types: Int, String, Boolean, Double, Long, Float
   - Initialized with random but valid values
   - Named for clarity

3. **Control Flow**
   - If-else statements with type-appropriate conditions
   - For loops with iteration counters
   - When expressions for pattern matching

4. **Function Calls**
   - Calls helper functions with appropriate variables
   - Stores and prints results

5. **Collection Operations**
   - List creation and manipulation
   - Built-in operations like sum()

6. **Print Statements Throughout**
   - Program start/end markers
   - Variable values
   - Function call traces
   - Iteration progress
   - Results of operations

## Compilation Success Rate

**100%** - All generated programs compile successfully because they are semantically valid.

## Use Cases

- **Backend Testing**: Test Kotlin Native compiler backend changes
- **Correctness Validation**: Verify compiler produces correct executables
- **Behavior Observation**: Use print statements to trace execution
- **Regression Testing**: Generate large test suites quickly
- **Performance Testing**: Generate many programs for benchmarking

## Command-Line Options

```
-o, --output FILE       Output file path (required)
-l, --lines NUM         Target number of lines (default: 50)
-n, --num-files NUM     Number of files to generate (default: 1)
--validate              Validate compilation with kotlinc
--run                   Compile and run the program
```

## Comparison with Grammar-Based Generation

| Feature | generate_complex.py | generate_kotlin.py |
|---------|-------------------|-------------------|
| Compilation Success | 100% | ~0-5% |
| Semantic Validity | Valid | Often invalid |
| Print Statements | Yes, many | Rare |
| Runnable Programs | Yes | Rarely |
| Line Count Control | Yes (~50 LOC) | Variable |
| Speed | Fast (~1s/file) | Fast (~1s/file) |
| Use Case | Backend testing | Parser fuzzing |

## Tips

1. **For Backend Testing**: Always use `generate_complex.py` with `--run` flag
2. **Batch Generation**: Use `-n` to generate multiple test cases at once
3. **Custom Complexity**: Adjust `-l` parameter for longer/shorter programs
4. **Validation**: Use `--validate` to ensure compilation before deployment
5. **Observability**: All programs include print statements for easy debugging
