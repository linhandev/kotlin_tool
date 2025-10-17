# Kotlin Code Generator for Backend Testing

Generates diverse Kotlin programs for testing Kotlin Native compiler backend.

## Quick Start

```bash
# Generate a single diverse program
python3 generate.py -o test.kt

# Generate 100 diverse programs
python3 generate.py -o test.kt -n 100

# Generate and validate
python3 generate.py -o test.kt -n 50 --validate

# More features (more diverse, lower success rate)
python3 generate.py -o test.kt -n 100 -f 20
```

## Features

The generator creates programs with diverse Kotlin language features:
- Data classes, sealed classes, enums
- Extension functions, infix functions
- Lambdas, higher-order functions
- Generics with variance
- Nullable types, safe calls, elvis operator
- When expressions, destructuring
- Ranges and collections
- Sequences and lazy evaluation
- Property delegation
- Companion objects, nested classes
- Type aliases
- Inline functions, tailrec, vararg
- Operator overloading
- And more!

## Compilation Success Rate

- With 10-12 features: ~60-80% success rate
- With 15-20 features: ~30-50% success rate
- With 25+ features: ~10-20% success rate

**Priority is diversity over compilation success** for thorough backend testing.

## Options

```
-o, --output FILE       Output file path (default: test.kt)
-n, --num-files NUM     Number of files to generate (default: 1)
-f, --features NUM      Number of features per program (default: 12)
--validate              Validate with kotlinc
```

## Example Output

Each program includes:
- 70-100 lines of code
- 10-20 different Kotlin language features
- Main function that exercises the features
- Print statements for debugging

## For Fuzzing

Generate large test suites:

```bash
# Generate 1000 diverse programs
python3 generate.py -o fuzz/test.kt -n 1000 -f 15

# Generate with high diversity (lower success rate)
python3 generate.py -o fuzz/test.kt -n 500 -f 20
```

## Previous Versions

See `experiment/` folder for previous template-based and grammar-based generators.

## Setup

```bash
pip install -r requirements.txt
```

The generator uses `kotlinc` (Kotlin JVM compiler) for validation. Kotlin Native testing should be done separately on the generated `.kt` files.
