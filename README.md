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

### Basic Code Generation

Generate a single Kotlin file:
```bash
python3 generate_kotlin.py -o generated_code/output.kt
```

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
├── generate_kotlin.py             # Main generation script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## How It Works

1. **Grammar Processing**: The ANTLR4 grammar files from the Kotlin specification are processed by Grammarinator to create a Python-based generator.

2. **Code Generation**: The generator uses the processed grammar to create random but syntactically valid Kotlin code by traversing the grammar rules.

3. **Validation**: Generated code can optionally be compiled with `kotlinc` to verify syntactic and semantic correctness.

## Limitations

- **Semantic Validity**: While the generated code is syntactically correct according to the grammar, it may not be semantically valid (e.g., undefined references, type mismatches).
- **Compilation Success Rate**: Due to semantic constraints not encoded in the grammar, many generated files may not compile successfully.
- **Grammar Actions**: Some language-specific actions from the original grammar (e.g., Java code for mode handling) have been removed for compatibility with Python.

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
