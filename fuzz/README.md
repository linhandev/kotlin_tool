# Kotlin Differential Fuzzer

Production-ready differential testing tool for Kotlin compilers.

## Quick Start

```bash
# Run comprehensive compilation test (30 minutes)
python3 final_product/test.py --duration 30

# Run differential fuzzing (100 tests, 4 parallel workers)
python3 final_product/fuzzer.py --tests 100 --parallel 4

# Custom complexity
python3 final_product/fuzzer.py --tests 200 --depth 8 --statements 40 --parallel 8
```

## Features

- **Grammar-driven generation**: Creates syntactically valid Kotlin code
- **Differential testing**: Compares Kotlin 2.2.20 vs 2.0.0
- **Parallel execution**: Optimized for multi-core systems
- **Type-safe**: Fully typed Python 3.10+ code
- **Comprehensive testing**: 30-minute stress tests

## Architecture

```
final_product/
├── generator.py    # Code generator with scope tracking
├── fuzzer.py       # Differential testing engine
└── test.py         # Comprehensive test suite

experiments/        # Historical experiments and comparisons
```

## Configuration

### Complexity Levels

- **Low**: depth=3, statements=10
- **Medium**: depth=5, statements=20
- **High**: depth=8, statements=40
- **Extreme**: depth=12, statements=60

### Parallelization

All stages except program execution are parallelized:
- Code generation: parallel
- Compilation: parallel
- Comparison: parallel
- Execution: sequential (to avoid resource conflicts)

## Output

Differential fuzzing saves only tests showing differences:

```
results/
└── failed_tests/
    └── test_000042/
        ├── test.kt              # Source code
        ├── compilation.json     # Compile results
        ├── exec_220.json        # Execution on 2.2.20
        ├── exec_200.json        # Execution on 2.0.0
        └── summary.json         # Difference summary
```

## Requirements

- Python 3.10+
- Kotlin 2.2.20 (system)
- Kotlin 2.0.0 (installed at /home/runner/kotlin-2.0.0/)
- Java runtime

## Implementation Details

### Code Generation

Uses hierarchical scope tracking to ensure:
- Variables declared before use
- Proper scoping (functions, blocks, loops)
- Type consistency
- Mutable/immutable distinction

### Differential Testing

Compares:
1. Compilation success/failure
2. Runtime crashes
3. Output differences
4. Exit codes

### Performance

- Generates ~100 tests/minute (with parallel=4)
- 95%+ compilation success rate
- Minimal memory footprint
