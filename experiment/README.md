# Previous Generator Versions

This folder contains previous versions of the Kotlin code generators.

## Contents

- **GENERATOR_COMPARISON.md** - Comparison between template and grammar-based approaches
- **QUICKSTART.md** - Quick start guide for old generators
- **SOLUTION.md** - Solution summary for backend testing
- **SUMMARY.md** - Project summary
- **examples/** - Usage examples and sample programs

## Old Generators

Previous generator scripts have been archived here. The current production generator is `../generate.py` in the root directory.

## Why Archived?

The new diverse feature-based generator (`../generate.py`) combines the best of both approaches:
- Uses 25+ Kotlin language features for maximum diversity
- Generates 70-100 line programs
- 30-70% compilation success (configurable via feature count)
- Single simple entry point
- Optimized for Kotlin Native backend fuzzing

The old generators are kept for reference and comparison.
