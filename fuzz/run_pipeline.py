#!/usr/bin/env python3
"""
Master script to run the entire fuzz testing pipeline
"""

import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()

STEPS = [
    {
        "name": "Step 1: Evaluate Grammar Specifications",
        "script": "step1_evaluate_grammars.py",
        "description": "Compare three Kotlin grammar specs"
    },
    {
        "name": "Step 2: Improve Grammar for Complex Code",
        "script": "step2_improve_grammar.py",
        "description": "Generate complex Kotlin code with advanced features"
    },
    {
        "name": "Step 3: Maximize Code Complexity",
        "script": "step3_maximize_complexity.py",
        "description": "Push complexity to the maximum"
    },
    {
        "name": "Step 4: Differential Fuzzing",
        "script": "step4_differential_fuzz.py",
        "description": "Compare Kotlin 2.2.20 vs 2.0.0"
    }
]


def run_step(step):
    """Run a single step of the pipeline"""
    print("\n" + "="*70)
    print(f"{step['name']}")
    print(f"{step['description']}")
    print("="*70)
    
    script_path = BASE_DIR / step['script']
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(BASE_DIR),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ {step['name']} completed successfully")
            return True
        else:
            print(f"\n✗ {step['name']} failed with exit code {result.returncode}")
            return False
    except Exception as e:
        print(f"\n✗ Error running {step['name']}: {e}")
        return False


def main():
    print("="*70)
    print("KOTLIN NATIVE COMPILER FUZZ TESTING PIPELINE")
    print("="*70)
    print("\nThis will run all 4 steps of the pipeline:")
    for i, step in enumerate(STEPS, 1):
        print(f"  {i}. {step['name']}")
    
    response = input("\nContinue? [y/N]: ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    results = []
    for step in STEPS:
        success = run_step(step)
        results.append((step['name'], success))
        
        if not success:
            print(f"\n⚠ Step failed. Continue anyway? [y/N]: ", end='')
            response = input()
            if response.lower() != 'y':
                break
    
    # Summary
    print("\n" + "="*70)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*70)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print("\n✓ All steps completed successfully!")
        print("\nResults are available in:")
        print("  - experiments/step1_results/")
        print("  - experiments/step2_results/")
        print("  - experiments/step3_results/")
        print("  - experiments/step4_results/")
        print("\nSee fuzz/README.md for detailed documentation.")
    else:
        print("\n⚠ Some steps failed. Check the output above for details.")


if __name__ == "__main__":
    main()
