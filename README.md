# Kotlin Code Generator with Grammarinator

This project generates random Kotlin code using [Grammarinator](https://github.com/renatahodovan/grammarinator) based on the official [Kotlin grammar specification](https://github.com/Kotlin/kotlin-spec).

## Overview

The project uses the ANTLR4 grammar definitions from the Kotlin specification repository to generate syntactically valid (though not always semantically correct) Kotlin code. Generated code is validated using Kotlin Native compiler 2.2.20.

## Setup

### Prerequisites

- Python 3.12+
- Kotlin 2.2.20 (installed via SDKMan)

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. The Kotlin grammar has already been processed and is available in the `grammars/` directory.

## Usage

### Generate Complex Valid Programs (Recommended)

For testing compiler backends with semantically valid, compilable code:

```bash
# Generate a complex program (~50 lines) with print statements
python3 generate_complex.py -o generated_code/program.kt -l 50 --run

# Generate multiple test programs
python3 generate_complex.py -o generated_code/test.kt -n 10 -l 60 --validate

# Generate and run to see program behavior
python3 generate_complex.py -o generated_code/example.kt --run
```

This generator creates valid Kotlin programs with:
- Main function with print statements for observing behavior
- Variable declarations with different types
- Control flow (if/else, loops, when expressions)
- Function definitions and calls
- Approximately 50 lines of code (configurable)
- **100% compilation success rate**
- Actual runnable programs for backend testing

### Grammar-Based Generation (For Fuzzing)

For compiler robustness testing with random syntactic structures:
```bash
# Basic grammar-based generation
python3 generate_kotlin.py -o generated_code/output.kt
```

**Note**: Grammar-based generation produces syntactically valid but often semantically invalid code. Use `generate_complex.py` for testing compiler backends.

### Generate Multiple Files

Generate multiple Kotlin files with numbering:
```bash
python3 generate_kotlin.py -o generated_code/test_%d.kt -n 10
```

### Generate and Validate

Generate code and validate it with the Kotlin compiler:
```bash
python3 generate_kotlin.py -o generated_code/output.kt --validate
```

### Generate Valid Code

Try multiple times to generate code that compiles successfully:
```bash
python3 generate_valid.py -o generated_code/valid.kt -a 50
```

This script attempts multiple generations with varying parameters until it finds one that compiles.

### Advanced Options

```bash
python3 generate_kotlin.py \
  -o generated_code/output.kt \
  -r kotlinFile \           # Starting rule (default: kotlinFile)
  -d 20 \                   # Maximum depth (default: 20)
  -c 0.9 \                  # Cooldown factor (default: 0.5, range: 0.0-1.0)
  -n 5 \                    # Number of files to generate
  --validate                # Validate with kotlinc
```

### Parameters Explained

- **`-o, --output`**: Output file path. Use `%d` for multiple files (e.g., `test_%d.kt`)
- **`-r, --rule`**: Grammar rule to start generation from (default: `kotlinFile`)
- **`-d, --max-depth`**: Maximum depth of the syntax tree (higher = more complex code)
- **`-c, --cooldown`**: Cooldown factor affects variety in generation (0.0-1.0, higher = less repetition)
- **`-n, --num-files`**: Number of files to generate (default: 1)
- **`--validate`**: Compile generated code with kotlinc to check validity

## Project Structure

```
.
├── grammars/                      # Processed Kotlin grammar files
│   ├── KotlinGenerator.py         # Generated Grammarinator code
│   ├── KotlinLexer_clean.g4       # Cleaned ANTLR4 lexer grammar
│   └── KotlinParser.g4            # ANTLR4 parser grammar
├── generated_code/                # Output directory for generated files
├── generate_complex.py            # Template-based complex program generator (RECOMMENDED)
├── generate_kotlin.py             # Grammar-based generation script
├── generate_valid.py              # Script to generate valid (compilable) code
├── batch_test.py                  # Batch testing script with statistics
├── setup.sh                       # Setup script for environment
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## How It Works

1. **Grammar Processing**: The ANTLR4 grammar files from the Kotlin specification are processed by Grammarinator to create a Python-based generator.

2. **Code Generation**: The generator uses the processed grammar to create random but syntactically valid Kotlin code by traversing the grammar rules.

3. **Validation**: Generated code can optionally be compiled with `kotlinc` to verify syntactic and semantic correctness.

## Limitations

- **Semantic Validity**: While the generated code is syntactically correct according to the grammar, it may not be semantically valid (e.g., undefined references, type mismatches).
- **Compilation Success Rate**: Due to semantic constraints not encoded in the grammar, most generated files will not compile successfully. This is expected behavior for grammar-based fuzzing tools.
- **Code Complexity**: Valid generated code tends to be minimal (empty files, simple declarations) because complex structures are less likely to be semantically valid when randomly generated.
- **Grammar Actions**: Some language-specific actions from the original grammar (e.g., Java code for mode handling) have been removed for compatibility with Python.

## Use Cases

### Template-Based Generation (generate_complex.py)
- **Compiler Backend Testing**: Testing Kotlin Native compiler with valid, runnable programs
- **Correctness Testing**: Programs that compile and execute successfully
- **Behavioral Testing**: Programs with print statements to observe execution
- **Performance Testing**: Generate many valid programs quickly

### Grammar-Based Generation (generate_kotlin.py)
- **Compiler Robustness Testing**: Testing compiler with edge cases
- **Grammar Validation**: Verifying completeness of the Kotlin grammar specification
- **Parser Fuzzing**: Finding potential bugs in Kotlin parsing (parsers, IDEs, etc.)

**For backend compiler testing, use `generate_complex.py` which produces valid, runnable code.**

## Notes

- The grammar uses the `kotlinFile` rule as the entry point by default, which generates complete Kotlin files.
- You can also use the `script` rule to generate Kotlin script files.
- Adjust the `max-depth` and `cooldown` parameters to control the complexity and variety of generated code.
- Higher cooldown values (closer to 1.0) produce more varied code structures.

## Grammar Source

The Kotlin grammar is sourced from the official Kotlin specification repository:
- Repository: https://github.com/Kotlin/kotlin-spec
- Grammar location: `grammar/src/main/antlr/`
- Branch: `release`

## License

This project uses the official Kotlin grammar specification which is part of the Kotlin project.
