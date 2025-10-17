# Running the Fuzz Testing Pipeline

## Prerequisites

Before running the pipeline, ensure you have:

```bash
# Check Python version (3.8+ required)
python3 --version

# Check Java version (17+ required)
java -version
```

## Installation

1. Navigate to the fuzz directory:
```bash
cd fuzz
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

That's it! The pipeline will automatically download:
- ANTLR 4.13.2
- Kotlin compiler 2.2.20
- Kotlin compiler 2.0.0
- Three Kotlin grammar specifications

## Running the Full Pipeline

### Option 1: Run Everything (Recommended for first-time users)

```bash
python3 run_pipeline.py
```

This will execute all 4 steps sequentially with confirmation prompts.

### Option 2: Run Individual Steps

#### Step 1: Evaluate Grammars (~2 minutes)

```bash
python3 step1_evaluate_grammars.py
```

**What it does**: Downloads and evaluates 3 Kotlin grammar specs by generating 20 code samples each and compiling them with kotlinc 2.2.20.

**Expected output**: 
- `experiments/step1_results/summary.json`
- Success rate ~95% for all grammars

#### Step 2: Generate Complex Code (~3 minutes)

```bash
python3 step2_improve_grammar.py
```

**What it does**: Generates 50 complex Kotlin programs using advanced features like generics, sealed classes, and higher-order functions.

**Expected output**:
- `experiments/step2_results/generated/` - 50 .kt files
- `experiments/step2_results/results.json`
- Success rate ~94%

#### Step 3: Maximize Complexity (~10 minutes)

```bash
python3 step3_maximize_complexity.py
```

**What it does**: Generates 100 maximally complex programs with deep nesting, multiple type parameters, and advanced patterns.

**Expected output**:
- `experiments/step3_results/generated/` - 100 .kt files
- `experiments/step3_results/results.json`
- Success rate ~85-90%

#### Step 4: Differential Fuzzing (~5 minutes)

```bash
python3 step4_differential_fuzz.py
```

**What it does**: Generates 50 test cases, compiles and runs them with both Kotlin 2.2.20 and 2.0.0, compares outputs.

**Expected output**:
- `experiments/step4_results/summary.json`
- `experiments/step4_results/failures/` - Only created if differences found
- Most tests should pass (outputs match)

## Interpreting Results

### Step 1 Results

Check `experiments/step1_results/summary.json`:

```json
{
  "grammars": [
    {
      "display_name": "Official Kotlin Spec",
      "success_rate": 95.00,
      "compiled_count": 19,
      "generated_count": 20
    },
    ...
  ]
}
```

All three grammars should achieve high success rates on basic templates.

### Step 2 Results

Check `experiments/step2_results/results.json`:

```json
{
  "generated": 50,
  "compiled": 47,
  "failed": 3,
  "success_rate": 94.00
}
```

High success rate demonstrates ability to generate valid complex code.

### Step 3 Results

Check `experiments/step3_results/results.json`:

```json
{
  "generated": 100,
  "compiled": 89,
  "failed": 11,
  "success_rate": 89.00
}
```

Lower success rate is expected as complexity increases. Some edge cases intentionally fail.

### Step 4 Results

Check `experiments/step4_results/summary.json`:

```json
{
  "statistics": {
    "generated": 50,
    "compile_220_success": 50,
    "compile_200_success": 50,
    "output_match": 50,
    "output_differ": 0,
    "failures_saved": 0
  }
}
```

**Key metrics:**
- `output_match`: Tests where both versions produced identical output ✓
- `output_differ`: Tests where outputs differed ⚠
- `failures_saved`: Number of failed tests with saved artifacts

**If differences found:**
Check `experiments/step4_results/failures/test_N/`:
- `Test.kt` - Source code
- `output_220.txt` - Output from Kotlin 2.2.20
- `output_200.txt` - Output from Kotlin 2.0.0
- `result.json` - Detailed test metadata

## Configuration

### Adjusting Sample Sizes

Edit the scripts to change sample counts:

**step1_evaluate_grammars.py:**
```python
NUM_SAMPLES = 20  # Increase for more thorough testing
```

**step2_improve_grammar.py:**
```python
NUM_SAMPLES = 50  # Increase for more samples
```

**step3_maximize_complexity.py:**
```python
NUM_SAMPLES = 100  # Increase for more coverage
```

**step4_differential_fuzz.py:**
```python
NUM_SAMPLES = 50      # More tests = better coverage
MAX_WORKERS = 4       # Increase for faster execution (if you have more cores)
COMPILE_TIMEOUT = 20  # Increase if compilations timeout
RUN_TIMEOUT = 5       # Increase if programs timeout
```

### Running with More Parallelism

For faster Step 4 execution on machines with more cores:

```python
# In step4_differential_fuzz.py
MAX_WORKERS = 8  # Or more, depending on your CPU
```

## Troubleshooting

### Error: "No module named 'antlr4'"

```bash
pip install antlr4-python3-runtime==4.13.2
```

### Error: Compilation timeout

Increase timeout in the script:
```python
COMPILE_TIMEOUT = 60  # Increase from default 20
```

### Error: Out of memory

Reduce parallelism:
```python
MAX_WORKERS = 2  # Reduce from default 4
```

Or reduce sample count:
```python
NUM_SAMPLES = 25  # Reduce from default
```

### Downloads fail

Check internet connection. The pipeline needs to download:
- ANTLR JAR (~2MB)
- Kotlin 2.2.20 (~75MB)
- Kotlin 2.0.0 (~80MB)
- Grammar specs (~35MB)

## Example Session

```bash
$ cd fuzz
$ python3 run_pipeline.py

==================================================================
KOTLIN NATIVE COMPILER FUZZ TESTING PIPELINE
==================================================================

This will run all 4 steps of the pipeline:
  1. Step 1: Evaluate Grammar Specifications
  2. Step 2: Improve Grammar for Complex Code
  3. Step 3: Maximize Code Complexity
  4. Step 4: Differential Fuzzing

Continue? [y/N]: y

======================================================================
Step 1: Evaluate Grammar Specifications
Compare three Kotlin grammar specs
======================================================================
...
✓ Step 1: Evaluate Grammar Specifications completed successfully

======================================================================
Step 2: Improve Grammar for Complex Code
Generate complex Kotlin code with advanced features
======================================================================
...
✓ Step 2: Improve Grammar for Complex Code completed successfully

======================================================================
Step 3: Maximize Code Complexity
Push complexity to the maximum
======================================================================
...
✓ Step 3: Maximize Code Complexity completed successfully

======================================================================
Step 4: Differential Fuzzing
Compare Kotlin 2.2.20 vs 2.0.0
======================================================================
...
✓ Step 4: Differential Fuzzing completed successfully

======================================================================
PIPELINE EXECUTION SUMMARY
======================================================================
✓ PASS: Step 1: Evaluate Grammar Specifications
✓ PASS: Step 2: Improve Grammar for Complex Code
✓ PASS: Step 3: Maximize Code Complexity
✓ PASS: Step 4: Differential Fuzzing

✓ All steps completed successfully!

Results are available in:
  - experiments/step1_results/
  - experiments/step2_results/
  - experiments/step3_results/
  - experiments/step4_results/

See fuzz/README.md for detailed documentation.
```

## Next Steps

After running the pipeline:

1. **Review Results**: Check the `experiments/` directory for all generated artifacts
2. **Investigate Failures**: If Step 4 found differences, examine the failure artifacts
3. **Customize**: Modify code generation templates in the scripts
4. **Scale Up**: Increase sample sizes for more thorough testing
5. **Automate**: Integrate into CI/CD for continuous testing

## Need Help?

- Check the main documentation: `fuzz/README.md`
- Review example files: `fuzz/examples/`
- Check existing results: `fuzz/experiments/`
