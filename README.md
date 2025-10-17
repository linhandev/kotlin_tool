# Kotlin Native Compiler Fuzzing Pipeline

Differential fuzzing system for testing Kotlin Native compiler backend. Generates diverse Kotlin programs and compares behavior between compiler versions to find bugs and regressions.

## Quick Start

### 1. Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Kotlin Native compilers (2.0.0 and 2.2.20)
./install_compilers.sh
```

### 2. Run Fuzzing

```bash
# Run 100 tests with 8 workers (default)
python3 fuzzer.py -n 100

# Run 1000 tests with custom settings
python3 fuzzer.py -n 1000 -f 15 -w 16

# Long-running fuzzing campaign
python3 fuzzer.py -n 10000 -f 20 -o fuzz_results_campaign1
```

## Features

### Code Generator

Generates diverse Kotlin programs with 40+ language features:
- **Classes**: Data classes, sealed classes, enums, value classes, interfaces, abstract classes
- **Functions**: Extension functions, infix functions, inline functions, tailrec, vararg
- **Advanced**: Lambdas, generics, nullable types, smart casts, contracts
- **Modern**: Coroutines basics, delegation, property delegation, scope functions
- **Collections**: Ranges, sequences, transformations, operations
- **And more**: Annotations, lazy properties, lateinit, operator overloading

### Differential Fuzzing

### Differential Fuzzing

Compares two Kotlin Native compiler versions:
- **Baseline**: Kotlin Native 2.0.0 (reference version)
- **SUT**: Kotlin Native 2.2.20 (system under test)

For each generated program:
1. Compile with both compilers
2. Compare compilation results (success/failure)
3. If both succeed, run and compare outputs
4. Save cases showing differences

**Interesting test cases** (saved to `fuzz_results/failed_tests/`):
- Baseline compiles but SUT fails (regression)
- SUT compiles but baseline fails (new feature or fix)
- Both compile but produce different output (behavior change)

### Multiprocessing

Uses Python's multiprocessing for parallel execution:
- Default: Uses all CPU cores
- Scales linearly with number of workers
- Independent test execution
- Thread-safe result collection

## Compilation Success Rate

Target: **5%+ compilation success** with diverse features

### Multiprocessing

Uses Python's multiprocessing for parallel execution:
- Default: Uses all CPU cores
- Scales linearly with number of workers
- Independent test execution
- Thread-safe result collection

## Compilation Success Rate

Target: **5%+ compilation success** with diverse features

Actual rates (with kotlinc JVM validation):
- With 10-12 features: ~40-60% success rate
- With 15-20 features: ~20-40% success rate  
- With 25+ features: ~5-15% success rate

**Priority is diversity over compilation success** for thorough backend testing.

## Generator Options

```
-o, --output FILE       Output file path (default: test.kt)
-n, --num-files NUM     Number of files to generate (default: 1)
-f, --features NUM      Number of features per program (default: 12)
--validate              Validate with kotlinc
```

## Fuzzer Options

```
--baseline PATH         Path to baseline compiler (default: /usr/local/kotlinc-2.0.0)
--sut PATH              Path to SUT compiler (default: /usr/local/kotlinc-2.2.20)
-n, --num-tests NUM     Number of tests (default: 100)
-f, --features NUM      Features per program (default: 15)
-w, --workers NUM       Worker processes (default: CPU count)
-o, --output DIR        Output directory (default: fuzz_results)
--timeout SEC           Timeout per test (default: 30)
```

## Example Workflow

```bash
# 1. Install compilers (one-time setup)
./install_compilers.sh

# 2. Quick test (10 tests)
python3 fuzzer.py -n 10 -f 12

# 3. Medium campaign (1000 tests)
python3 fuzzer.py -n 1000 -f 15 -w 8

# 4. Long-running fuzzing (for days)
python3 fuzzer.py -n 100000 -f 20 -w 16 -o fuzz_results_long

# 5. Examine interesting cases
ls fuzz_results/failed_tests/
cat fuzz_results/failed_tests/test_000042/summary.txt
```

## Output Structure

```
fuzz_results/
├── failed_tests/           # Interesting test cases
│   ├── test_000001/
│   │   ├── test.kt        # Source code
│   │   └── summary.txt    # Comparison results
│   ├── test_000042/
│   └── ...
└── stats.txt              # Overall statistics
```

## For Long-Running Fuzzing

The fuzzer is designed to run for extended periods (days/weeks):
- Generates maximally diverse code (40+ features)
- Each test is independent
- Results saved incrementally
- Graceful handling of timeouts and errors
- Can be interrupted (Ctrl+C) and restarted

## Architecture

### Code Generator (`generate.py`)
- Template-based approach for reliability
- 40+ feature generators
- Configurable feature count
- Extensive print statements for observability

### Fuzzer (`fuzzer.py`)
- Differential testing framework
- Multiprocessing support
- Automatic result classification
- Incremental result saving

## Testing

```bash
# Test generator
python3 generate.py -o /tmp/test.kt -n 10 --validate

# Test fuzzer (requires installed compilers)
python3 fuzzer.py -n 5 -w 1
```
