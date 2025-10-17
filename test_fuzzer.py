#!/usr/bin/env python3
"""
Test script for the Kotlin fuzzing pipeline

Tests the generator and validates the fuzzing pipeline structure.
"""

import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from generate import generate_diverse_program, compile_with_kotlinc


def test_generator():
    """Test the code generator"""
    print("Testing code generator...")
    
    # Test with different feature counts
    for num_features in [5, 10, 15, 20]:
        print(f"\n  Testing with {num_features} features:")
        code = generate_diverse_program(num_features)
        
        # Validate basic structure
        assert "fun main()" in code, "Missing main function"
        assert "println" in code, "Missing print statements"
        assert code.count('\n') > 50, "Code too short"
        
        print(f"    ✓ Generated {code.count('\\n')} lines")
        
        # Count features
        feature_count = code.count("// Feature:")
        print(f"    ✓ Contains {feature_count} features")
    
    print("\n✓ Generator tests passed")
    return True


def test_generator_compilation():
    """Test generator with kotlinc validation"""
    print("\nTesting compilation with kotlinc...")
    
    success_count = 0
    total_count = 10
    
    for i in range(total_count):
        code = generate_diverse_program(12)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.kt', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            success, output = compile_with_kotlinc(temp_file)
            if success:
                success_count += 1
                print(f"  [{i+1}/{total_count}] ✓ COMPILED")
            else:
                print(f"  [{i+1}/{total_count}] ✗ FAILED")
        finally:
            Path(temp_file).unlink(missing_ok=True)
    
    success_rate = 100 * success_count / total_count
    print(f"\nCompilation success rate: {success_count}/{total_count} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print(f"✓ Success rate above 90% target")
        return True
    else:
        print(f"✗ Success rate below 90% target")
        return False


def test_fuzzer_structure():
    """Test fuzzer module structure"""
    print("\nTesting fuzzer structure...")
    
    try:
        from fuzzer import KotlinNativeFuzzer, CompilerConfig, TestResult
        print("  ✓ Imports successful")
        
        # Test dataclasses
        config = CompilerConfig(version="2.0.0", path=Path("/tmp"))
        print(f"  ✓ CompilerConfig: {config.version}")
        
        result = TestResult(
            test_id="test_001",
            source_code="fun main() {}",
            baseline_compiled=True,
            sut_compiled=True
        )
        print(f"  ✓ TestResult: {result.test_id}")
        print(f"    Summary: {result.get_summary()}")
        
        print("✓ Fuzzer structure tests passed")
        return True
    except Exception as e:
        print(f"✗ Fuzzer structure test failed: {e}")
        return False


def test_feature_coverage():
    """Test that all features are covered"""
    print("\nTesting feature coverage...")
    
    from generate import KOTLIN_FEATURES, FEATURE_GENERATORS
    
    print(f"  Total features: {len(KOTLIN_FEATURES)}")
    print(f"  Total generators: {len(FEATURE_GENERATORS)}")
    
    # Check all features have generators
    missing = []
    for feature in KOTLIN_FEATURES:
        if feature not in FEATURE_GENERATORS:
            missing.append(feature)
    
    if missing:
        print(f"  ✗ Missing generators for: {missing}")
        return False
    
    print(f"  ✓ All {len(KOTLIN_FEATURES)} features have generators")
    
    # Test each generator
    print("\n  Testing individual generators:")
    for feature, generator in FEATURE_GENERATORS.items():
        try:
            code, name = generator()
            assert len(code) > 0, f"Empty code for {feature}"
            assert len(name) > 0, f"Empty name for {feature}"
            print(f"    ✓ {feature}")
        except Exception as e:
            print(f"    ✗ {feature}: {e}")
            return False
    
    print("\n✓ Feature coverage tests passed")
    return True


def main():
    """Run all tests"""
    print("="*60)
    print("Kotlin Fuzzing Pipeline Test Suite")
    print("="*60)
    
    tests = [
        ("Generator", test_generator),
        ("Feature Coverage", test_feature_coverage),
        ("Compilation", test_generator_compilation),
        ("Fuzzer Structure", test_fuzzer_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name:20s}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == '__main__':
    exit(main())
