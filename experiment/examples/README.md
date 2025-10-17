# Examples

This directory contains example commands and their outputs.

## Basic Generation

```bash
# Generate a single file
python3 generate_kotlin.py -o generated_code/example1.kt -d 15 -c 0.9
```

## Batch Testing

```bash
# Generate 10 files and check compilation
python3 batch_test.py -n 10 -d 15 -c 0.9
```

Expected output:
```
Generating 10 Kotlin files...
Parameters: depth=15, cooldown=0.9

Generation completed in 0.4 seconds

Compiling generated files...
------------------------------------------------------------
[1/10] batch_test_0.kt (500 bytes)... ✗ FAILED
[2/10] batch_test_1.kt (350 bytes)... ✗ FAILED
[3/10] batch_test_2.kt (200 bytes)... ✗ FAILED
...
------------------------------------------------------------

Results:
  Total files: 10
  Successful:  0-1 (0-10%)
  Failed:      9-10 (90-100%)
```

Note: Most randomly generated code will not compile due to semantic constraints not encoded in the grammar.

## Finding Valid Code

```bash
# Try to generate code that compiles
python3 generate_valid.py -o generated_code/valid.kt -a 50
```

This script tries multiple generations until one compiles successfully.

## Different Starting Rules

You can generate from different grammar rules:

```bash
# Generate a complete file
python3 generate_kotlin.py -o generated_code/file.kt -r kotlinFile

# Generate a script
python3 generate_kotlin.py -o generated_code/script.kts -r script
```

## Parameter Effects

- **Depth (--max-depth)**: Controls complexity
  - Lower (5-10): Simpler, shorter code
  - Higher (20-30): More complex, nested structures
  
- **Cooldown (--cooldown)**: Controls variety
  - Lower (0.5-0.7): More repetitive patterns
  - Higher (0.9-1.0): More varied structures
