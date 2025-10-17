#!/usr/bin/env python3
"""
Quick verification test to ensure the pipeline is set up correctly
"""

import sys
from pathlib import Path

def check_files():
    """Check all required files exist"""
    base = Path(__file__).parent
    
    required = [
        'step1_evaluate_grammars.py',
        'step2_improve_grammar.py',
        'step3_maximize_complexity.py',
        'step4_differential_fuzz.py',
        'run_pipeline.py',
        'README.md',
        'USAGE.md',
        'IMPLEMENTATION_SUMMARY.md',
        'requirements.txt',
        'VIEW_RESULTS.sh',
        'examples/example_step1_simple.kt',
        'examples/example_step2_complex.kt',
        'examples/example_step3_maxcomplexity.kt'
    ]
    
    missing = []
    for f in required:
        if not (base / f).exists():
            missing.append(f)
    
    if missing:
        print("❌ Missing required files:")
        for f in missing:
            print(f"   - {f}")
        return False
    
    print("✅ All required files present")
    return True

def check_structure():
    """Check directory structure"""
    base = Path(__file__).parent
    
    dirs = [
        'examples',
        'experiments',
        'experiments/step1_results',
        'experiments/step2_results',
        'experiments/step3_results',
        'experiments/step4_results'
    ]
    
    missing = []
    for d in dirs:
        if not (base / d).exists():
            missing.append(d)
    
    if missing:
        print("❌ Missing directories:")
        for d in missing:
            print(f"   - {d}")
        return False
    
    print("✅ Directory structure correct")
    return True

def check_results():
    """Check if pipeline has been run"""
    base = Path(__file__).parent
    
    results = [
        ('experiments/step1_results/summary.json', 'Step 1'),
        ('experiments/step2_results/results.json', 'Step 2'),
        ('experiments/step3_results/results.json', 'Step 3'),
        ('experiments/step4_results/summary.json', 'Step 4')
    ]
    
    completed = []
    pending = []
    
    for path, name in results:
        if (base / path).exists():
            completed.append(name)
        else:
            pending.append(name)
    
    if completed:
        print(f"✅ Completed: {', '.join(completed)}")
    
    if pending:
        print(f"⏳ Pending: {', '.join(pending)}")
    
    return True

def main():
    print("="*60)
    print("FUZZ TESTING PIPELINE - VERIFICATION")
    print("="*60)
    print()
    
    checks = [
        ("Files", check_files),
        ("Structure", check_structure),
        ("Results", check_results)
    ]
    
    all_passed = True
    for name, check in checks:
        print(f"Checking {name}...")
        if not check():
            all_passed = False
        print()
    
    print("="*60)
    if all_passed:
        print("✅ VERIFICATION PASSED")
        print()
        print("The pipeline is ready to use!")
        print()
        print("Quick start:")
        print("  python3 run_pipeline.py          # Run entire pipeline")
        print("  bash VIEW_RESULTS.sh             # View existing results")
        print("  python3 step4_differential_fuzz.py  # Run differential testing")
        print()
        print("See README.md and USAGE.md for detailed instructions.")
    else:
        print("⚠️  VERIFICATION FAILED")
        print("Some components are missing. Please check the output above.")
        sys.exit(1)
    print("="*60)

if __name__ == "__main__":
    main()
