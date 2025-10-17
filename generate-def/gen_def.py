import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

from config import include_fdr, binary_fdr, library_info, group_info, additional_headers, additional_compilerOpts, out_fdr
import subprocess


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
    elif library:
        binary_path = binary_fdr / library
        if not binary_path.exists():
            # don't raise assertion here; warn and keep going so we can collect other libs
            print(f"Warning: Library '{library}' not found for header {relative_path}")

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
            try:
                resolved_relative = resolved_path.relative_to(sysroot_path)
                resolved_includes.append(str(resolved_relative))
            except Exception:
                # If it can't be made relative to sysroot_path, keep the resolved absolute path
                resolved_includes.append(str(resolved_path))
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


def process_all_header_files() -> Dict[str, Dict[str, any]]:
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
    ), f"Failed to open headers {' '.join(map(str, failed_headers))}"

    # Parse information from files with @addtogroup
    results: Dict[str, Dict[str, any]] = {}
    for file_path in harmony_sdk_headers:
        info: Optional[Dict[str, any]] = parse_header_file_info(file_path, include_fdr)
        if info:
            results[str(file_path)] = info

    return results


def generate_def_files(header_infos: Dict[str, Dict[str, any]], out_fdr: Path = Path(".")):
    """
    Generate .def files for Kotlin Native based on grouped header information
    This updated version collects ALL libraries referenced by headers in a group
    and emits a single linkerOpts line containing all -l flags (or none if no libs).
    """
    # Group headers by group
    groups: Dict[str, List[Dict[str, any]]] = defaultdict(list)

    for header_info in header_infos.values():
        groups[header_info["group"]].append(header_info)

    # Build mapping for dependency analysis
    header_to_group: Dict[str, str] = {}  # Both full path and filename to group
    for header in header_infos.values():
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

        # headers
        if group_name in additional_headers:
            for header_path in additional_headers[group_name]:
                headers.append(header_infos.get(header_path, {"path": Path(header_path), "includes": [], "library": None}))
        header_paths = [str(header["path"]) for header in headers]
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

        """
        1. single file: headerFilter = containing_folder/filename.h, this is final
        2. folders: headerFilter = folder1/** folder2/**
        3. files without folders: headerFilter = file1.h file2.h
        """
        if len(header_paths) == 1:
            headerFilter = f"headerFilter = {header_paths[0]}"
        else:
            headerFilter = f"headerFilter ="
            if folders:
                # If there are folders, use folder/** pattern
                folder_filters = [f"{folder}/**" for folder in sorted(folders)]
                headerFilter += f" {' '.join(folder_filters)}"
            if files_without_folders:
                # If there are files without folders, list all file names
                headerFilter += f" {' '.join(sorted(files_without_folders))}"
        def_content += f"{headerFilter.strip()}\n"

        # depends
        all_includes = set()
        for header in headers:
            all_includes.update(header["includes"])

        # Find which groups are dependencies
        dependent_groups = set()
        header_files = []
        for header in headers:
            header_files.append(str(header["path"]))
            header_files.append(Path(header["path"]).name)

        for include_path in all_includes:
            if include_path in header_files:
                continue
            if include_path in header_to_group:
                dependent_group = header_to_group[include_path]
            else:
                dependent_group = header_to_group.get(Path(include_path).name)

            if dependent_group and dependent_group != group_name:
                dependent_groups.add(dependent_group)

        if dependent_groups:
            depends_list = sorted(dependent_groups)
            def_content += f"depends = {' '.join(depends_list)}\n"

        # linkerOpts: collect ALL libraries referenced by headers in this group
        libs = set()
        for header in headers:
            lib = header.get("library")
            if lib and lib != "NA":
                libs.add(lib)

        linker_flags: List[str] = []
        for library in sorted(libs):
            linker_lib = library
            # Remove lib prefix if present
            if linker_lib.startswith("lib"):
                linker_lib = linker_lib[3:]
            else:
                # not fatal; many library names may not start with 'lib'
                pass
            # Remove common suffixes
            if linker_lib.endswith(".so"):
                linker_lib = linker_lib[:-3]
            elif linker_lib.endswith(".a"):
                linker_lib = linker_lib[:-2]
            # Add -l flag
            if linker_lib:
                linker_flags.append(f"-l{linker_lib}")

        # compilerOpts
        if group_name in additional_compilerOpts:
            def_content += f"compilerOpts = {additional_compilerOpts[group_name]}\n"

        if linker_flags:
            # emit single linkerOpts line with all flags
            def_content += f"linkerOpts = {' '.join(linker_flags)}\n"

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
    parsed_results = process_all_header_files()

    print(f"\nTotal processed files: {len(parsed_results)}")

    input(f"Removing all files in {out_fdr}, Enter to continue or ctrl-c")

    try:
        subprocess.run(["git", "clean", "-dfx"], cwd=out_fdr, check=True)
        print(f"Cleaned output directory: {out_fdr}")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to clean git directory {out_fdr}: {e}")
    except FileNotFoundError:
        print("Warning: git command not found")
    generate_def_files(parsed_results, out_fdr)
