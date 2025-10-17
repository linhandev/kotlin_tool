#!/usr/bin/env python3
"""
Kotlin code generation script using Grammarinator.
This script generates random Kotlin code files based on the official Kotlin grammar
and validates them using the Kotlin compiler.
"""

import argparse
import sys
import os
import subprocess
import tempfile
from pathlib import Path


def generate_kotlin_file(output_file, rule='kotlinFile', max_depth=20, cooldown=0.5, num_files=1):
    """
    Generate Kotlin files using the Grammarinator generator.
    
    Args:
        output_file: Path pattern for output files (can include %d for numbering)
        rule: The starting rule for generation (default: 'kotlinFile')
        max_depth: Maximum depth of the generated tree
        cooldown: Cooldown parameter for generation (0.0-1.0)
        num_files: Number of files to generate
    """
    project_root = Path(__file__).parent.resolve()
    
    # Build the command for grammarinator-generate
    cmd = [
        'grammarinator-generate',
        'grammars.KotlinGenerator.KotlinGenerator',
        '-r', rule,
        '-d', str(max_depth),
        '-c', str(cooldown),
        '-n', str(num_files),
        '-o', output_file,
        '--sys-path', str(project_root)
    ]
    
    print(f"Generating {num_files} Kotlin file(s) with rule '{rule}', depth {max_depth}, cooldown {cooldown}")
    print(f"Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error generating code: {result.stderr}")
        return False
    
    print(f"Successfully generated Kotlin code")
    return True


def compile_kotlin_file(kotlin_file):
    """
    Attempt to compile a Kotlin file using kotlinc.
    
    Args:
        kotlin_file: Path to the Kotlin file to compile
        
    Returns:
        tuple: (success: bool, output: str)
    """
    # Source sdkman and run kotlinc
    kotlin_file = Path(kotlin_file).resolve()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = f'source /home/runner/.sdkman/bin/sdkman-init.sh && kotlinc "{kotlin_file}" -d "{tmpdir}"'
        
        result = subprocess.run(
            cmd,
            shell=True,
            executable='/bin/bash',
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.returncode == 0, result.stdout + result.stderr


def main():
    parser = argparse.ArgumentParser(description='Generate Kotlin code using Grammarinator')
    parser.add_argument('-o', '--output', required=True, help='Output file path (use %%d for multiple files)')
    parser.add_argument('-r', '--rule', default='kotlinFile', help='Starting rule (default: kotlinFile)')
    parser.add_argument('-d', '--max-depth', type=int, default=20, help='Maximum depth (default: 20)')
    parser.add_argument('-c', '--cooldown', type=float, default=0.5, help='Cooldown parameter (default: 0.5)')
    parser.add_argument('-n', '--num-files', type=int, default=1, help='Number of files to generate (default: 1)')
    parser.add_argument('--validate', action='store_true', help='Validate generated code with kotlinc')
    
    args = parser.parse_args()
    
    # Generate code
    success = generate_kotlin_file(
        args.output,
        args.rule,
        args.max_depth,
        args.cooldown,
        args.num_files
    )
    
    if not success:
        sys.exit(1)
    
    # Optionally validate generated code
    if args.validate:
        print("\n--- Validation ---")
        # Find all generated files
        if '%d' in args.output:
            output_pattern = args.output.replace('%d', '*')
            import glob
            files = sorted(glob.glob(output_pattern))
        else:
            files = [args.output]
        
        for kotlin_file in files:
            if os.path.exists(kotlin_file):
                print(f"\nValidating {kotlin_file}...")
                success, output = compile_kotlin_file(kotlin_file)
                
                if success:
                    print(f"✓ {kotlin_file} compiled successfully!")
                else:
                    print(f"✗ {kotlin_file} failed to compile:")
                    print(output[:500])  # Show first 500 chars of error


if __name__ == '__main__':
    main()
