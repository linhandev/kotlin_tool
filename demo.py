#!/usr/bin/env python3
"""
Demo script for Kotlin Native Fuzzing Pipeline

This script demonstrates the fuzzing pipeline with mock compilers
since Kotlin Native compilers may not be installed.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from generate import generate_diverse_program


def demo_code_generation():
    """Demonstrate code generation with various feature counts"""
    print("="*60)
    print("Demo 1: Code Generation with Different Feature Counts")
    print("="*60)
    print()
    
    for num_features in [8, 12, 16, 20]:
        print(f"Generating code with {num_features} features...")
        code = generate_diverse_program(num_features)
        
        lines = code.count('\n')
        features = code.count('// Feature:')
        print_count = code.count('println')
        
        print(f"  Lines of code: {lines}")
        print(f"  Features used: {features}")
        print(f"  Print statements: {print_count}")
        print()
        
        # Save example
        output_file = f"/tmp/demo_code_{num_features}_features.kt"
        Path(output_file).write_text(code)
        print(f"  Saved to: {output_file}")
        print()


def demo_feature_showcase():
    """Showcase a few generated files with different features"""
    print("="*60)
    print("Demo 2: Feature Showcase")
    print("="*60)
    print()
    
    # Generate a sample with balanced features
    print("Generating sample Kotlin program with 12 features...")
    code = generate_diverse_program(12)
    
    output_file = "/tmp/showcase_example.kt"
    Path(output_file).write_text(code)
    
    # Show first 40 lines
    lines = code.split('\n')
    print("\nFirst 40 lines of generated code:")
    print("-" * 60)
    for i, line in enumerate(lines[:40], 1):
        print(f"{i:3d} | {line}")
    print("-" * 60)
    print(f"\nFull file saved to: {output_file}")
    print()


def demo_diversity():
    """Demonstrate code diversity by generating multiple files"""
    print("="*60)
    print("Demo 3: Code Diversity")
    print("="*60)
    print()
    
    print("Generating 5 programs with 10 features each...")
    print("Showing which features were selected for each:\n")
    
    for i in range(5):
        code = generate_diverse_program(10)
        
        # Extract feature names
        features = []
        for line in code.split('\n'):
            if '// Feature:' in line:
                feature = line.split('// Feature:')[1].strip()
                features.append(feature)
        
        print(f"Program {i+1}: {', '.join(features)}")
    
    print("\nNote: Each program has a unique combination of features!")
    print()


def demo_fuzzer_structure():
    """Demonstrate the fuzzer structure"""
    print("="*60)
    print("Demo 4: Fuzzer Structure")
    print("="*60)
    print()
    
    from fuzzer import KotlinNativeFuzzer, CompilerConfig, TestResult
    
    print("The fuzzer supports:")
    print("  - Differential testing between two compiler versions")
    print("  - Multiprocessing for parallel test execution")
    print("  - Automatic classification of test results")
    print("  - Incremental saving of interesting test cases")
    print()
    
    # Show a mock test result
    print("Example test result categories:")
    
    categories = [
        ("both_failed", "Both compilers failed to compile"),
        ("both_passed_match", "Both compiled successfully with matching output"),
        ("both_passed_differ", "Both compiled but outputs differ (BUG!)"),
        ("baseline_only", "Only baseline compiled (regression in SUT)"),
        ("sut_only", "Only SUT compiled (new feature or fix)"),
    ]
    
    for category, description in categories:
        print(f"  - {category:20s}: {description}")
    
    print()


def demo_usage_examples():
    """Show usage examples"""
    print("="*60)
    print("Demo 5: Usage Examples")
    print("="*60)
    print()
    
    print("Code Generator Usage:")
    print("-" * 60)
    print("# Generate a single program")
    print("python3 generate.py -o test.kt -f 12")
    print()
    print("# Generate 100 programs")
    print("python3 generate.py -o test.kt -n 100 -f 12")
    print()
    print("# Generate and validate with kotlinc")
    print("python3 generate.py -o test.kt -n 20 -f 10 --validate")
    print()
    print()
    
    print("Fuzzer Usage (requires Kotlin Native compilers):")
    print("-" * 60)
    print("# Install compilers (one-time setup)")
    print("./install_compilers.sh")
    print()
    print("# Run 100 tests with all CPU cores")
    print("python3 fuzzer.py -n 100 -f 12")
    print()
    print("# Long-running fuzzing campaign")
    print("python3 fuzzer.py -n 10000 -f 15 -w 16 -o fuzz_results_long")
    print()
    print()
    
    print("Expected Results:")
    print("-" * 60)
    print("fuzz_results/")
    print("├── failed_tests/")
    print("│   ├── test_000042/")
    print("│   │   ├── test.kt       # Kotlin source code")
    print("│   │   └── summary.txt   # Comparison results")
    print("│   └── ...")
    print("└── stats.txt             # Overall statistics")
    print()


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("Kotlin Native Fuzzing Pipeline - Demo")
    print("="*60)
    print()
    
    demos = [
        demo_code_generation,
        demo_feature_showcase,
        demo_diversity,
        demo_fuzzer_structure,
        demo_usage_examples,
    ]
    
    for demo in demos:
        demo()
        input("Press Enter to continue to next demo...")
        print()
    
    print("="*60)
    print("Demo Complete!")
    print("="*60)
    print()
    print("Next steps:")
    print("  1. Install Kotlin Native compilers: ./install_compilers.sh")
    print("  2. Run fuzzing: python3 fuzzer.py -n 100")
    print("  3. Check results: ls fuzz_results/failed_tests/")
    print()


if __name__ == '__main__':
    main()
