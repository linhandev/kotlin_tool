#!/usr/bin/env python3
"""
Script to generate simple valid Kotlin code examples.
This attempts to generate minimal valid Kotlin structures.
"""

import subprocess
import tempfile
import os
from pathlib import Path


def try_generate_valid_kotlin(output_file, max_attempts=50):
    """
    Try to generate a valid Kotlin file by attempting multiple generations
    and keeping the first one that compiles successfully.
    
    Args:
        output_file: Path to the output file
        max_attempts: Maximum number of attempts
        
    Returns:
        bool: True if successful, False otherwise
    """
    project_root = Path(__file__).parent.resolve()
    
    # Start with simpler/shorter code
    depths = [8, 10, 12, 15, 18, 20]
    cooldowns = [0.95, 0.9, 0.85, 0.8]
    
    for attempt in range(max_attempts):
        depth = depths[attempt % len(depths)]
        cooldown = cooldowns[attempt % len(cooldowns)]
        
        # Generate to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.kt', delete=False) as tmp:
            tmp_file = tmp.name
        
        try:
            # Generate code
            cmd = [
                'grammarinator-generate',
                'grammars.KotlinGenerator.KotlinGenerator',
                '-r', 'kotlinFile',
                '-d', str(depth),
                '-c', str(cooldown),
                '-n', '1',
                '-o', tmp_file,
                '--sys-path', str(project_root)
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            # Try to compile
            with tempfile.TemporaryDirectory() as tmpdir:
                compile_cmd = f'source /home/runner/.sdkman/bin/sdkman-init.sh && kotlinc "{tmp_file}" -d "{tmpdir}" 2>&1'
                
                result = subprocess.run(
                    compile_cmd,
                    shell=True,
                    executable='/bin/bash',
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    # Success! Copy to output
                    import shutil
                    shutil.copy(tmp_file, output_file)
                    print(f"✓ Generated valid Kotlin code after {attempt + 1} attempts")
                    print(f"  Parameters: depth={depth}, cooldown={cooldown}")
                    
                    # Show the file
                    with open(output_file, 'r') as f:
                        content = f.read()
                    print(f"\nGenerated code ({len(content)} bytes):")
                    print("-" * 60)
                    print(content)
                    print("-" * 60)
                    return True
                else:
                    if attempt % 10 == 0 and attempt > 0:
                        print(f"Attempt {attempt + 1}/{max_attempts}...")
                    
        finally:
            # Clean up temp file
            if os.path.exists(tmp_file):
                os.unlink(tmp_file)
    
    print(f"✗ Failed to generate valid code after {max_attempts} attempts")
    return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate valid Kotlin code')
    parser.add_argument('-o', '--output', default='generated_code/valid_example.kt', 
                       help='Output file path')
    parser.add_argument('-a', '--attempts', type=int, default=50,
                       help='Maximum number of attempts (default: 50)')
    
    args = parser.parse_args()
    
    output_dir = Path(args.output).parent
    output_dir.mkdir(exist_ok=True)
    
    print(f"Attempting to generate valid Kotlin code...")
    print(f"Will try up to {args.attempts} times\n")
    
    success = try_generate_valid_kotlin(args.output, args.attempts)
    
    if success:
        print(f"\n✓ Valid Kotlin code saved to: {args.output}")
        return 0
    else:
        print(f"\n✗ Could not generate valid code")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
