import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

from config import include_fdr, binary_fdr, library_info, group_info, additional_headers, additional_compilerOpts, out_fdr


def get_all_headers(sysroot_path: Path) -> Tuple[List[Path], List[Path], List[Path]]:
    """
    Find all .h files in include_fdr folder and categorize them into three lists:
    1. Files with @addtogroup tags
    2. Files that open normally but don't contain @addtogroup
    3. Files that can't be opened for any reason
    """
    harmony_sdk_headers: List[Path] = []
    other_headers: List[Path] = []
    failed_headers: List[Path] = []

    for file_path in sysroot_path.rglob("*.h"):
        if file_path.name.startswith("."):
            continue

        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "@addtogroup" in content:
                    harmony_sdk_headers.append(file_path)
                else:
                    other_headers.append(file_path)
        except Exception as e:
            print(f"Failed to open file {file_path}: {e}")
            failed_headers.append(file_path)

    return harmony_sdk_headers, other_headers, failed_headers


def parse_header_file_info(
    file_path: Path, sysroot_path: Path
) -> Optional[Dict[str, any]]:
    """
    Parse the required information from a header file:
    - group: @addtogroup
    - library: @library
    - includes: all #included headers
    - path: relative path from include_fdr
    """
    assert file_path.is_file(), f"{str(file_path)} is not a file"

    with file_path.open("r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    relative_path = file_path.relative_to(sysroot_path)

    # Parse @addtogroup
    if str(relative_path) in group_info:
        group = group_info[str(relative_path)]
    else:
        addtogroup_pattern = r"@addtogroup\s+(\S+)"
        addtogroup_matches = re.findall(addtogroup_pattern, content)
        assert (
            len(addtogroup_matches) <= 1
        ), f"Multiple @addtogroup matches found in {relative_path}: {addtogroup_matches}"
        group = addtogroup_matches[0] if addtogroup_matches else None

    # Parse @library
    if str(relative_path) in library_info:
        library = library_info[str(relative_path)]
    else:
        library_pattern = r"@library\s+(\S+)"
        library_matches = re.findall(library_pattern, content)
        if len(library_matches) > 1:
            unique_libraries = set(library_matches)
            assert (
                len(unique_libraries) == 1
            ), f"Multiple different @library matches found in {relative_path}: {library_matches}"
        library = library_matches[0] if library_matches else None
    
    if library == "NA":
        print(f"Warning: Library for {relative_path} is NA")
    else:
        binary_path = binary_fdr / library
        assert (
            binary_path.exists()
        ), f"Library '{library}' not found in for header {relative_path}"

    # Parse includes
    include_pattern = r'#include\s+[<"]([^>"]+)[>"]'
    includes = re.findall(include_pattern, content)

    # Resolve relative include paths to absolute paths
    resolved_includes = []
    for include in includes:
        if include.startswith("/"):
            # Already absolute path
            resolved_includes.append(include)
        elif include.startswith("../"):
            # Relative path - resolve relative to current file's directory
            current_file_dir = file_path.parent
            resolved_path = (current_file_dir / include).resolve()
            # Make it relative to sysroot_path for consistency
            resolved_relative = resolved_path.relative_to(sysroot_path)
            resolved_includes.append(str(resolved_relative))
        else:
            # System include or already properly formatted
            resolved_includes.append(include)
    assert (
        group is not None and len(group) != 0
    ), f"No @addtogroup found in {relative_path}"

    return {
        "path": relative_path,
        "group": group,
        "library": library,
        "includes": resolved_includes,
    }


def process_all_header_files() -> List[Dict[str, any]]:
    """
    Main function to process all header files and return the list of parsed information
    """
    # Find all header files
    harmony_sdk_headers, other_headers, failed_headers = get_all_headers(include_fdr)

    print(f"{len(harmony_sdk_headers)} header files with @addtogroup tags")
    print(f"{len(other_headers)} header files without @addtogroup tags")
    print(f"{len(failed_headers)} header files that couldn't be opened")

    assert (
        len(failed_headers) == 0
    ), f"Failed to open headers {' '.join(failed_headers)}"

    # Parse information from files with @addtogroup
    results: List[Dict[str, any]] = []
    for file_path in harmony_sdk_headers:
        info: Optional[Dict[str, any]] = parse_header_file_info(file_path, include_fdr)
        if info:
            results.append(info)

    return results


def generate_def_files(parsed_results: List[Dict[str, any]], out_fdr: Path = Path(".")):
    """
    Generate .def files for Kotlin Native based on grouped header information
    """
    # Group headers by group
    groups: Dict[str, List[Dict[str, any]]] = defaultdict(list)

    for header_info in parsed_results:
        groups[header_info["group"]].append(header_info)

    # Build mapping for dependency analysis
    header_to_group: Dict[str, str] = {}  # Both full path and filename to group
    
    for header in parsed_results:
        full_path = str(header["path"])
        filename = Path(header["path"]).name
        group = header["group"]
        
        header_to_group[full_path] = group
        
        if filename in header_to_group:
            if header_to_group[filename] != group:
                print(f"Warning: Filename '{filename}' exists in multiple different groups: {header_to_group[filename]} and {group}")
        else:
            header_to_group[filename] = group

    for group_name, headers in groups.items():
        # package
        def_content = f"package = platform.{group_name}\n"

        # depends
        all_includes = set()
        for header in headers:
            all_includes.update(header["includes"])
        
        # Find which groups are dependencies
        dependent_groups = set()
        for include_path in all_includes:
            if include_path in header_to_group:
                dependent_group = header_to_group[include_path]
            else:
                dependent_group = header_to_group.get(Path(include_path).name)
            
            if dependent_group and dependent_group != group_name:
                dependent_groups.add(dependent_group)
        
        if dependent_groups:
            depends_list = sorted(dependent_groups)
            def_content += f"depends = {' '.join(depends_list)}\n"

        # headers
        header_paths = [str(header["path"]) for header in headers]
        if group_name in additional_headers:
            header_paths = additional_headers[group_name] + header_paths
        def_content += f"headers = {' '.join(header_paths)}\n"
        
        # headerFilter
        folders = set()
        files_without_folders = []
        
        for header_path in header_paths:
            path_obj = Path(header_path)
            if len(path_obj.parts) > 1:  # Has folder(s)
                # Use the full directory path (excluding filename)
                folder_path = str(path_obj.parent)
                folders.add(folder_path)
            else:  # File without folder
                files_without_folders.append(path_obj.name)
        
        if folders:
            # If there are folders, use folder/** pattern
            folder_filters = [f"{folder}/**" for folder in sorted(folders)]
            def_content += f"headerFilter = {' '.join(folder_filters)}\n"
        elif files_without_folders:
            # If only files without folders, list all file names
            def_content += f"headerFilter = {' '.join(sorted(files_without_folders))}\n"

        # linkerOpts
        library = None
        for header in headers:
            if header["library"] and header["library"] != "NA":
                library = header["library"]
                break
        
        # compilerOpts
        if group_name in additional_compilerOpts:
            def_content += f"compilerOpts = {additional_compilerOpts[group_name]}\n"

        if library:
            # Strip 'lib' prefix and '.so' suffix for linkerOpts
            linker_lib = library
            if linker_lib.startswith("lib"):
                linker_lib = linker_lib[3:]
            else:
                print(f"Warning: Library '{library}' does not start with 'lib'")
            if linker_lib.endswith(".so"):
                linker_lib = linker_lib[:-3]
            else:
                print(f"Warning: Library '{library}' does not end with '.so'")
            def_content += f"linkerOpts = -l{linker_lib}\n"
        def_content += "language = C++\ncompilerOpts = -std=c++17\n"
        
        # Write .def file
        def_filename = f"{group_name}.def"
        def_filepath = out_fdr / def_filename

        try:
            with def_filepath.open("w", encoding="utf-8") as f:
                f.write(def_content)
        except Exception as e:
            print(f"Warning: Error writing {def_filename}: {e}")


if __name__ == "__main__":
    parsed_results: List[Dict[str, any]] = process_all_header_files()

    print(f"\nTotal processed files: {len(parsed_results)}")

    # Generate .def files
    out_fdr.mkdir(exist_ok=True)
    # Remove all existing files in out_fdr
    # for file_path in out_fdr.glob("*"):
    #     if file_path.is_file():
    #         file_path.unlink()
    generate_def_files(parsed_results, out_fdr)
