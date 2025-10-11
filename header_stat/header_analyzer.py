#!/usr/bin/env python3
"""
Header Analyzer Script using ctags
Analyzes .h files containing @addtogroup and extracts function prototype information using ctags.
"""

import os
import csv
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Any

# Global configuration
SYSROOT_INCLUDE_FOLDER = "/Users/user/Desktop/software/command-line-tools-6.0.0.858/sdk/default/openharmony/native/sysroot-ohos-aarch64-6.0.0.858/usr/include"


def has_addtogroup(file_path: Path) -> bool:
    """Check if a file contains @addtogroup directive."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            return '@addtogroup' in content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False


def parse_function_prototypes_with_ctags(file_path: Path) -> List[Dict[str, Any]]:
    """Parse function prototypes from a header file using ctags."""
    prototypes: List[Dict[str, Any]] = []
    
    try:
        # Run ctags command to extract function prototypes
        cmd = ['/opt/homebrew/bin/ctags', '--kinds-c=p', '-x', str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Parse ctags output
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
                
            # ctags output format: name kind line_no file_path signature
            parts = line.split(None, 3)  # Split on whitespace, max 4 parts
            if len(parts) < 4:
                continue
                
            function_name = parts[0]
            kind = parts[1]  # Should be 'prototype'
            line_no = parts[2]
            
            # Skip if not a function prototype
            if kind != 'prototype':
                continue
            
            # The rest is file path and signature
            remaining = parts[3]
            
            # Find where the file path ends and signature begins
            # The signature starts after the file path
            file_in_output = str(file_path)
            if file_in_output in remaining:
                signature_start = remaining.find(file_in_output) + len(file_in_output)
                signature = remaining[signature_start:].strip()
            else:
                # Fallback: try to find the signature after the space
                file_basename = os.path.basename(str(file_path))
                if file_basename in remaining:
                    signature_start = remaining.find(file_basename) + len(file_basename)
                    signature = remaining[signature_start:].strip()
                else:
                    signature = remaining.split(' ', 1)[1] if ' ' in remaining else remaining
            
            # Parse the signature to extract return type and parameters
            return_type, parameters = parse_signature(signature, function_name)
            
            # Make file path relative to SYSROOT_INCLUDE_FOLDER
            try:
                relative_path = os.path.relpath(str(file_path), SYSROOT_INCLUDE_FOLDER)
            except ValueError:
                # If relpath fails (e.g., different drives on Windows), use absolute path
                relative_path = str(file_path)
            
            prototypes.append({
                'file_path': relative_path,
                'line_no': int(line_no),
                'function_name': function_name,
                'return_type': return_type,
                'parameter_types': parameters,
                'full_signature': signature
            })
            
    except subprocess.CalledProcessError as e:
        print(f"ctags failed for {file_path}: {e}")
    except Exception as e:
        print(f"Error parsing {file_path} with ctags: {e}")
    
    return prototypes


def parse_signature(signature: str, function_name: str) -> Tuple[str, str]:
    """Parse a function signature to extract return type and parameters."""
    try:
        # Remove any leading/trailing whitespace
        signature = signature.strip()
        
        # Find the function name in the signature
        func_pos: int = signature.find(function_name)
        if func_pos == -1:
            return "unknown", "unknown"
        
        # Extract return type (everything before function name)
        return_type: str = signature[:func_pos].strip()
        
        # Extract parameters (everything between parentheses)
        paren_start: int = signature.find('(', func_pos)
        paren_end: int = signature.rfind(')')
        
        if paren_start != -1 and paren_end != -1:
            parameters: str = signature[paren_start+1:paren_end].strip()
            if not parameters:
                parameters = "void"
        else:
            parameters = "unknown"
        
        # Clean up return type
        if not return_type:
            return_type = "unknown"
        
        return return_type, parameters
        
    except Exception as e:
        print(f"Error parsing signature '{signature}': {e}")
        return "unknown", "unknown"


def find_header_files_with_addtogroup(base_path: str = SYSROOT_INCLUDE_FOLDER) -> List[Path]:
    """Find all .h files that contain @addtogroup and are not hidden."""
    header_files: List[Path] = []
    
    for root, dirs, files in os.walk(base_path):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.h') and not file.startswith('.'):
                file_path = Path(root) / file
                if has_addtogroup(file_path):
                    header_files.append(file_path)
                    
    return header_files


def main() -> None:
    """Main function."""
    print("Header File Analyzer using ctags")
    print("=" * 40)
    
    # Find all header files with @addtogroup
    header_files: List[Path] = find_header_files_with_addtogroup()
    print(f"Found {len(header_files)} header files with @addtogroup")
    
    all_prototypes: List[Dict[str, Any]] = []
    
    # Process each file
    for file_path in header_files:
        print(f"Processing: {file_path}")
        prototypes: List[Dict[str, Any]] = parse_function_prototypes_with_ctags(file_path)
        all_prototypes.extend(prototypes)
        print(f"  Found {len(prototypes)} prototypes")
    
    # Generate CSV
    if all_prototypes:
        csv_filename: str = 'header_prototypes.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames: List[str] = [
                'file_path', 'line_no', 'function_name', 
                'return_type', 'parameter_types', 'full_signature'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for prototype in all_prototypes:
                writer.writerow(prototype)
        
        print(f"\nCSV generated: {csv_filename}")
        print(f"Total prototypes extracted: {len(all_prototypes)}")
        
        # Show summary by file
        files_with_prototypes: Dict[str, int] = {}
        for proto in all_prototypes:
            file_path_str: str = proto['file_path']
            if file_path_str not in files_with_prototypes:
                files_with_prototypes[file_path_str] = 0
            files_with_prototypes[file_path_str] += 1
        
        print(f"\nSummary by file:")
        for file_path_str, count in sorted(files_with_prototypes.items()):
            # file_path_str is already relative to SYSROOT_INCLUDE_FOLDER from above
            print(f"  {file_path_str}: {count} prototypes")
    else:
        print("No function prototypes found.")


if __name__ == '__main__':
    main()