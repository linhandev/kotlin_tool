#!/usr/bin/env python3
"""
Analyzes .h files containing @addtogroup and extracts function prototype information using ctags.
"""

import os
import csv
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Tuple, Any

from config import ohos_sysroot_fdr, hms_sysroot_fdr


def normalize_parameter_types(param_string: str) -> str:
    """
    Extract parameter types from parameter string, ignoring parameter names.
    Example: "int foo, char* bar, const double baz" -> "int,char*,const double"
    """
    if not param_string or param_string.strip() in ["", "void"]:
        return "void"

    # Split parameters by comma, but be careful of function pointer parameters
    params = []
    current_param = ""
    paren_level = 0

    for char in param_string:
        if char == "(":
            paren_level += 1
        elif char == ")":
            paren_level -= 1
        elif char == "," and paren_level == 0:
            params.append(current_param.strip())
            current_param = ""
            continue
        current_param += char

    if current_param.strip():
        params.append(current_param.strip())

    # Extract types from each parameter
    param_types = []
    for param in params:
        param = param.strip()
        if not param:
            continue

        # Handle function pointer parameters like: void (*callback)(int)
        if "(*" in param and ")" in param:
            # For function pointers, keep the whole thing as the type
            param_types.append(param)
        else:
            # Regular parameter - extract type by removing the last identifier
            # Split by whitespace and remove the last word (which is usually the variable name)
            words = param.split()
            if len(words) >= 2:
                # Check if last word looks like a variable name (no *, no [], etc.)
                last_word = words[-1]
                if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", last_word):
                    # Remove the last word (variable name)
                    param_type = " ".join(words[:-1])
                else:
                    # Keep the whole thing (might be a complex type)
                    param_type = param
            else:
                # Single word, assume it's a type
                param_type = param
            param_types.append(param_type.strip())

    return ",".join(param_types)


def has_addtogroup(file_path: Path) -> bool:
    """Check if a file contains @addtogroup directive."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            return "@addtogroup" in content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False


def parse_function_prototypes_with_ctags(file_path: Path) -> List[Dict[str, Any]]:
    """Parse function prototypes from a header file using ctags."""
    prototypes: List[Dict[str, Any]] = []

    try:
        # Run ctags command to extract function prototypes with signature field and line numbers
        cmd = [
            "/opt/homebrew/bin/ctags",
            "--kinds-c=p",
            "--fields=+S",
            "-n",
            "-f",
            "-",
            str(file_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Parse ctags output (tab-separated format)
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue

            # ctags output format with -n flag: name<tab>file<tab>line_number<tab>kind<tab>extra_fields
            parts = line.split("\t")
            if len(parts) < 4:
                continue

            function_name = parts[0]
            file_info = parts[1]  # File path
            line_info = parts[2]  # Line number (actual number with -n flag)
            kind_info = parts[3]  # Kind with extra info like "p<tab>typeref:..."

            # Skip if not a function prototype
            if not kind_info.startswith("p"):
                continue

            # Extract line number (now directly provided by ctags -n flag)
            # Format is "line_number;" (e.g., "231;")
            try:
                if line_info.endswith(';"') and line_info[:-2].isdigit():
                    line_no = int(line_info[:-2])
                elif line_info.isdigit():
                    line_no = int(line_info)
                else:
                    line_no = -1
            except (ValueError, TypeError):
                line_no = -1

            # Look for signature and return type info
            signature = ""
            return_type = "unknown"

            for part in parts:
                if part.startswith("signature:"):
                    signature = part[10:]  # Remove 'signature:' prefix
                elif part.startswith("typeref:typename:"):
                    return_type = part[17:]  # Remove 'typeref:typename:' prefix

            # If no signature field found, try to extract from file
            if not signature:
                signature = extract_signature_from_file(
                    file_path, function_name, line_no
                )
                # Parse the signature to extract return type and parameters
                return_type, parameters = parse_signature(signature, function_name)
            else:
                # Extract parameters from the signature (everything between parentheses)
                paren_start = signature.find("(")
                paren_end = signature.rfind(")")
                if paren_start != -1 and paren_end != -1:
                    parameters = signature[paren_start + 1 : paren_end].strip()
                    if not parameters:
                        parameters = "void"
                else:
                    parameters = "unknown"

            try:
                relative_path = os.path.relpath(
                    str(file_path),
                    (
                        str(ohos_sysroot_fdr)
                        if str(ohos_sysroot_fdr) in str(file_path)
                        else str(hms_sysroot_fdr)
                    ),
                )
            except ValueError:
                # If relpath fails (e.g., different drives on Windows), use absolute path
                relative_path = str(file_path)

            # Normalize parameter types (remove parameter names)
            normalized_params = normalize_parameter_types(parameters)

            # Create full signature: return_type function_name(normalized_params)
            full_signature = f"{return_type} {function_name}({normalized_params})"

            prototypes.append(
                {
                    "file_path": relative_path,
                    "line_no": int(line_no),
                    "function_name": function_name,
                    "return_type": return_type,
                    "parameter_types": parameters,
                    "full_signature": full_signature,
                }
            )

    except subprocess.CalledProcessError as e:
        print(f"ctags failed for {file_path}: {e}")
    except Exception as e:
        print(f"Error parsing {file_path} with ctags: {e}")

    return prototypes


def extract_signature_from_file(
    file_path: Path, function_name: str, line_no: int
) -> str:
    """Extract complete function signature from file by reading around the line number."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # Start from the line where ctags found the function
        start_line = max(0, line_no - 1)  # Convert to 0-based index
        signature_lines = []

        # Look for the function declaration starting from the ctags line
        found_function = False
        paren_count = 0

        for i in range(
            start_line, min(len(lines), start_line + 20)
        ):  # Look at most 20 lines ahead
            line = lines[i].strip()

            # Skip empty lines and comments
            if not line or line.startswith("//") or line.startswith("/*"):
                continue

            # Check if this line contains our function name
            if function_name in line and not found_function:
                found_function = True
                # Start collecting from this line
                signature_lines.append(line)
                paren_count += line.count("(") - line.count(")")
            elif found_function:
                signature_lines.append(line)
                paren_count += line.count("(") - line.count(")")

            # Stop when we have balanced parentheses and hit a semicolon
            if found_function and paren_count <= 0 and (";" in line or "{" in line):
                break

        # Join the lines and clean up
        signature = " ".join(signature_lines)
        # Remove any trailing semicolon or opening brace
        signature = signature.replace(";", "").replace("{", "").strip()

        return signature

    except Exception as e:
        print(f"Error extracting signature from {file_path}: {e}")
        return "unknown"


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
        paren_start: int = signature.find("(", func_pos)
        paren_end: int = signature.rfind(")")

        if paren_start != -1 and paren_end != -1:
            parameters: str = signature[paren_start + 1 : paren_end].strip()
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


def find_header_files_with_addtogroup(
    ohos_sysroot_fdr: Path, hms_sysroot_fdr: Path
) -> List[Path]:
    """Find all .h files that contain @addtogroup and are not hidden file."""
    header_files: List[Path] = []

    for sysroot in [ohos_sysroot_fdr, hms_sysroot_fdr]:
        for root, dirs, files in os.walk(sysroot):
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                if file.endswith(".h") and not file.startswith("."):
                    file_path = Path(root) / file
                    if has_addtogroup(file_path):
                        header_files.append(file_path)

    return header_files


def main() -> None:
    """Main function."""
    print("Header File Analyzer using ctags")
    print("=" * 40)

    # Find all header files with @addtogroup
    header_files: List[Path] = find_header_files_with_addtogroup(
        ohos_sysroot_fdr, hms_sysroot_fdr
    )
    print(f"Found {len(header_files)} header files with @addtogroup")

    all_prototypes: List[Dict[str, Any]] = []

    # Process each file
    for file_path in header_files:
        print(f"Processing: {file_path}")
        prototypes: List[Dict[str, Any]] = parse_function_prototypes_with_ctags(
            file_path
        )
        all_prototypes.extend(prototypes)
        print(f"  Found {len(prototypes)} prototypes")

    # Generate CSV
    if all_prototypes:
        csv_filename: str = "header_prototypes.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames: List[str] = [
                "file_path",
                "line_no",
                "function_name",
                "return_type",
                "parameter_types",
                "full_signature",
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
            file_path_str: str = proto["file_path"]
            if file_path_str not in files_with_prototypes:
                files_with_prototypes[file_path_str] = 0
            files_with_prototypes[file_path_str] += 1

        print(f"\nSummary by file:")
        for file_path_str, count in sorted(files_with_prototypes.items()):
            print(f"  {file_path_str}: {count} prototypes")
    else:
        print("No function prototypes found.")


if __name__ == "__main__":
    main()
