#!/usr/bin/env python3
"""
Batch test script to generate multiple Kotlin files and report compilation statistics.
"""

import argparse
import subprocess
import tempfile
from pathlib import Path
import time


def compile_kotlin_file(kotlin_file):
    """Compile a Kotlin file and return success status."""
    kotlin_file = Path(kotlin_file).resolve()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = f'source /home/runner/.sdkman/bin/sdkman-init.sh && kotlinc "{kotlin_file}" -d "{tmpdir}" 2>&1'
        
        result = subprocess.run(
            cmd,
            shell=True,
            executable='/bin/bash',
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description='Batch test Kotlin code generation')
    parser.add_argument('-n', '--num-files', type=int, default=10, help='Number of files to generate (default: 10)')
    parser.add_argument('-d', '--max-depth', type=int, default=15, help='Maximum depth (default: 15)')
    parser.add_argument('-c', '--cooldown', type=float, default=0.9, help='Cooldown parameter (default: 0.9)')
    parser.add_argument('-o', '--output-dir', default='generated_code', help='Output directory (default: generated_code)')
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    output_pattern = str(output_dir / 'batch_test_%d.kt')
    
    print(f"Generating {args.num_files} Kotlin files...")
    print(f"Parameters: depth={args.max_depth}, cooldown={args.cooldown}")
    print()
    
    # Generate files
    cmd = [
        'python3', 'generate_kotlin.py',
        '-o', output_pattern,
        '-d', str(args.max_depth),
        '-c', str(args.cooldown),
        '-n', str(args.num_files)
    ]
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    gen_time = time.time() - start_time
    
    if result.returncode != 0:
        print(f"Error generating files: {result.stderr}")
        return
    
    print(f"Generation completed in {gen_time:.2f} seconds")
    print()
    
    # Compile and test each file
    print("Compiling generated files...")
    print("-" * 60)
    
    successful = 0
    failed = 0
    
    for i in range(args.num_files):
        kotlin_file = output_dir / f'batch_test_{i}.kt'
        
        if not kotlin_file.exists():
            continue
        
        file_size = kotlin_file.stat().st_size
        print(f"[{i+1}/{args.num_files}] {kotlin_file.name} ({file_size} bytes)... ", end='', flush=True)
        
        try:
            if compile_kotlin_file(kotlin_file):
                print("✓ SUCCESS")
                successful += 1
            else:
                print("✗ FAILED")
                failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1
    
    print("-" * 60)
    print(f"\nResults:")
    print(f"  Total files: {successful + failed}")
    print(f"  Successful:  {successful} ({100*successful/(successful+failed):.1f}%)")
    print(f"  Failed:      {failed} ({100*failed/(successful+failed):.1f}%)")
    print(f"\nGeneration time: {gen_time:.2f} seconds")
    print(f"Average per file: {gen_time/(successful+failed):.2f} seconds")


if __name__ == '__main__':
    main()
