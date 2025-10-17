# Kotlin Differential Fuzzer

ANTLR-based differential testing tool for Kotlin compilers.

## Quick Start

```bash
# Run all 4 steps
python3 fuzzing_pipeline.py --all --samples 200 --tests 100

# Run specific step
python3 fuzzing_pipeline.py --step 1 --samples 200
python3 fuzzing_pipeline.py --step 2 --samples 300
python3 fuzzing_pipeline.py --step 3 --samples 200
python3 fuzzing_pipeline.py --step 4 --tests 100 --parallel 4
```

## Implementation

### ANTLR-Based Generation

Uses ANTLR 4.13.2 to generate Kotlin code from grammar specifications:
- Downloaded from https://www.antlr.org/download/antlr-4.13.2-complete.jar
- Generates Python parsers from .g4 grammar files
- Code generation follows grammar production rules

### 4-Step Pipeline

**Step 1**: Evaluate 3 grammar specs by generating and compiling code with Kotlin 2.2.20
- kotlin-spec (official)
- kotlin-formal (antlr/grammars-v4)
- kotlin (antlr/grammars-v4, known ambiguity)

**Step 2**: Refine best spec to achieve 95%+ compilation success

**Step 3**: Increase complexity until ~25% success rate

**Step 4**: Differential fuzzing comparing Kotlin 2.2.20 vs 2.0.0
- Parallel compilation and comparison
- Sequential execution (one test at a time)
- Saves only tests showing differences

## Structure

```
fuzz/
├── fuzzing_pipeline.py       # Complete 4-step pipeline
├── antlr_generator.py         # ANTLR-based code generator
├── antlr-4.13.2-complete.jar  # ANTLR tool
├── grammar/                   # Generated ANTLR parsers
│   ├── KotlinLexer.py
│   ├── KotlinParser.py
│   └── *.g4 files
├── grammars/                  # 3 grammar source specs
│   ├── spec1_kotlin_spec/
│   ├── spec2_kotlin_formal/
│   └── spec3_kotlin/
└── experiments/               # Previous experimental work
```

## Requirements

- Python 3.10+
- Kotlin 2.2.20 (system)
- Kotlin 2.0.0 (/home/runner/kotlin-2.0.0/)
- Java runtime
- antlr4-python3-runtime==4.13.2

## Output

Results saved in `results/` directory:
- `step1/` - Grammar evaluation data
- `step2/` - Refinement results
- `step3/` - High complexity results
- `step4/failed_tests/` - Differential testing failures

