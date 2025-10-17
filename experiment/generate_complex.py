#!/usr/bin/env python3
"""
Template-based Kotlin code generator for producing valid, complex programs.
This generates semantically correct Kotlin code that compiles and runs,
suitable for testing Kotlin Native compiler backends.
"""

import argparse
import random
import subprocess
import tempfile
from pathlib import Path


# Templates for various Kotlin constructs
VARIABLE_TYPES = ['Int', 'String', 'Boolean', 'Double', 'Long', 'Float']
VARIABLE_NAMES = ['value', 'result', 'data', 'item', 'element', 'number', 'text', 'flag', 'count', 'index']
FUNCTION_NAMES = ['calculate', 'process', 'compute', 'transform', 'evaluate', 'validate', 'generate', 'convert']


def generate_variable_declaration(var_type=None, var_name=None, use_val=True):
    """Generate a valid variable declaration with initialization."""
    if var_type is None:
        var_type = random.choice(VARIABLE_TYPES)
    if var_name is None:
        var_name = random.choice(VARIABLE_NAMES) + str(random.randint(1, 100))
    
    keyword = 'val' if use_val else 'var'
    
    if var_type == 'Int':
        value = random.randint(-1000, 1000)
    elif var_type == 'Long':
        value = f"{random.randint(-1000, 1000)}L"
    elif var_type == 'Float':
        value = f"{random.uniform(-100, 100):.2f}f"
    elif var_type == 'Double':
        value = f"{random.uniform(-100, 100):.2f}"
    elif var_type == 'Boolean':
        value = random.choice(['true', 'false'])
    elif var_type == 'String':
        strings = ['hello', 'world', 'test', 'data', 'kotlin', 'code', 'value']
        value = f'"{random.choice(strings)}"'
    else:
        value = '0'
    
    return f"    {keyword} {var_name}: {var_type} = {value}\n", var_name, var_type


def generate_print_statement(message=None, value=None):
    """Generate a println statement."""
    if message and value:
        return f'    println("{message}: ${{{value}}}")\n'
    elif value:
        return f'    println({value})\n'
    elif message:
        return f'    println("{message}")\n'
    else:
        return f'    println("Debug output: ${{{random.choice(["x", "y", "result"])}}}")\n'


def generate_if_statement(var_name, var_type):
    """Generate an if-else statement."""
    lines = []
    if var_type == 'Int' or var_type == 'Long' or var_type == 'Double' or var_type == 'Float':
        condition = f"{var_name} > 0"
        lines.append(f"    if ({condition}) {{\n")
        lines.append(generate_print_statement(f"{var_name} is positive", var_name))
        lines.append("    } else {\n")
        lines.append(generate_print_statement(f"{var_name} is non-positive", var_name))
        lines.append("    }\n")
    elif var_type == 'Boolean':
        lines.append(f"    if ({var_name}) {{\n")
        lines.append(generate_print_statement("Condition is true"))
        lines.append("    } else {\n")
        lines.append(generate_print_statement("Condition is false"))
        lines.append("    }\n")
    elif var_type == 'String':
        lines.append(f"    if ({var_name}.isNotEmpty()) {{\n")
        lines.append(generate_print_statement("String is not empty", var_name))
        lines.append("    }\n")
    
    return ''.join(lines)


def generate_for_loop(iterations=None):
    """Generate a for loop."""
    if iterations is None:
        iterations = random.randint(3, 8)
    
    loop_var = 'i'
    lines = []
    lines.append(f"    for ({loop_var} in 1..{iterations}) {{\n")
    lines.append(f'        println("Iteration: ${{{loop_var}}}")\n')
    lines.append("    }\n")
    
    return ''.join(lines)


def generate_when_statement(var_name, var_type):
    """Generate a when expression."""
    lines = []
    
    if var_type == 'Int' or var_type == 'Long':
        lines.append(f"    when {{\n")
        lines.append(f"        {var_name} > 0 -> println(\"{var_name} is positive\")\n")
        lines.append(f"        {var_name} < 0 -> println(\"{var_name} is negative\")\n")
        lines.append(f"        else -> println(\"{var_name} is zero\")\n")
        lines.append("    }\n")
    elif var_type == 'Boolean':
        lines.append(f"    when ({var_name}) {{\n")
        lines.append(f"        true -> println(\"True case\")\n")
        lines.append(f"        false -> println(\"False case\")\n")
        lines.append("    }\n")
    
    return ''.join(lines)


def generate_function(func_name=None, param_type='Int'):
    """Generate a simple function."""
    if func_name is None:
        func_name = random.choice(FUNCTION_NAMES) + str(random.randint(1, 100))
    
    lines = []
    lines.append(f"fun {func_name}(param: {param_type}): {param_type} {{\n")
    
    if param_type == 'Int' or param_type == 'Long':
        lines.append(f'    println("Function {func_name} called with: $param")\n')
        lines.append(f"    return param * 2\n")
    elif param_type == 'String':
        lines.append(f'    println("Function {func_name} called with: $param")\n')
        lines.append(f'    return param + "_processed"\n')
    elif param_type == 'Boolean':
        lines.append(f'    println("Function {func_name} called with: $param")\n')
        lines.append(f"    return !param\n")
    else:
        lines.append(f"    return param\n")
    
    lines.append("}\n\n")
    
    return ''.join(lines), func_name


def generate_complex_program(target_lines=50):
    """Generate a complex Kotlin program with approximately target_lines lines of code."""
    lines = []
    
    # Add file header
    lines.append("// Auto-generated Kotlin program for testing\n")
    lines.append("// This program is designed to test Kotlin Native compiler backend\n\n")
    
    # Generate helper functions (approximately 15-20 lines)
    functions = []
    func_types = random.sample(VARIABLE_TYPES[:4], k=2)  # Use Int, String, Boolean, Double
    for func_type in func_types:
        func_code, func_name = generate_function(param_type=func_type)
        lines.append(func_code)
        functions.append((func_name, func_type))
    
    # Start main function
    lines.append("fun main() {\n")
    lines.append(generate_print_statement("Program started"))
    lines.append("\n")
    
    # Generate variables (approximately 10 lines)
    variables = []
    num_vars = random.randint(4, 7)
    for i in range(num_vars):
        var_code, var_name, var_type = generate_variable_declaration()
        lines.append(var_code)
        variables.append((var_name, var_type))
    
    lines.append("\n")
    
    # Print initial values
    lines.append(generate_print_statement("Initial values:"))
    for var_name, var_type in variables[:3]:  # Print first 3 variables
        lines.append(generate_print_statement(var_name, var_name))
    
    lines.append("\n")
    
    # Generate control flow statements (approximately 15-20 lines)
    if len(variables) > 0:
        # Add if statement
        var_name, var_type = random.choice(variables)
        lines.append(generate_if_statement(var_name, var_type))
        lines.append("\n")
    
    # Add for loop
    lines.append(generate_for_loop(random.randint(3, 5)))
    lines.append("\n")
    
    # Add when statement
    if len(variables) > 1:
        var_name, var_type = variables[1]
        if var_type in ['Int', 'Long', 'Boolean']:
            lines.append(generate_when_statement(var_name, var_type))
            lines.append("\n")
    
    # Call helper functions
    for func_name, func_type in functions:
        if func_type in [v[1] for v in variables]:
            # Find a variable with matching type
            matching_vars = [v[0] for v in variables if v[1] == func_type]
            if matching_vars:
                var_name = matching_vars[0]
                result_var = f"result{random.randint(1, 100)}"
                lines.append(f"    val {result_var} = {func_name}({var_name})\n")
                lines.append(generate_print_statement(f"Function result", result_var))
                lines.append("\n")
    
    # Add array/list operations
    lines.append("    val numbers = listOf(1, 2, 3, 4, 5)\n")
    lines.append('    println("List: $numbers")\n')
    lines.append("    val sum = numbers.sum()\n")
    lines.append('    println("Sum: $sum")\n')
    lines.append("\n")
    
    # Add final output
    lines.append(generate_print_statement("Program completed"))
    
    # Close main function
    lines.append("}\n")
    
    return ''.join(lines)


def compile_kotlin_file(kotlin_file):
    """Compile a Kotlin file and return success status."""
    kotlin_file = Path(kotlin_file).resolve()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = ['kotlinc', str(kotlin_file), '-d', tmpdir]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.returncode == 0, result.stdout + result.stderr


def run_kotlin_program(kotlin_file):
    """Compile and run a Kotlin program, returning output."""
    kotlin_file = Path(kotlin_file).resolve()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        jar_path = Path(tmpdir) / "program.jar"
        
        # Compile
        compile_cmd = ['kotlinc', str(kotlin_file), '-include-runtime', '-d', str(jar_path)]
        
        compile_result = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if compile_result.returncode != 0:
            return False, "Compilation failed:\n" + compile_result.stdout + compile_result.stderr
        
        # Run
        run_cmd = ['java', '-jar', str(jar_path)]
        
        run_result = subprocess.run(
            run_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return True, run_result.stdout


def main():
    parser = argparse.ArgumentParser(
        description='Generate complex, valid Kotlin programs for compiler testing'
    )
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    parser.add_argument('-l', '--lines', type=int, default=50, 
                       help='Target number of lines (default: 50)')
    parser.add_argument('-n', '--num-files', type=int, default=1,
                       help='Number of files to generate (default: 1)')
    parser.add_argument('--validate', action='store_true',
                       help='Validate generated code with kotlinc')
    parser.add_argument('--run', action='store_true',
                       help='Compile and run the generated program')
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    output_dir = output_path.parent
    output_dir.mkdir(exist_ok=True)
    
    if args.num_files > 1:
        # Generate multiple files
        base_name = output_path.stem
        extension = output_path.suffix
        
        for i in range(args.num_files):
            file_path = output_dir / f"{base_name}_{i}{extension}"
            code = generate_complex_program(args.lines)
            
            with open(file_path, 'w') as f:
                f.write(code)
            
            line_count = code.count('\n')
            print(f"Generated {file_path} ({line_count} lines)")
            
            if args.validate or args.run:
                success, output = compile_kotlin_file(file_path)
                if success:
                    print(f"  ✓ Compilation successful")
                    
                    if args.run:
                        run_success, run_output = run_kotlin_program(file_path)
                        if run_success:
                            print(f"  ✓ Execution successful")
                            print(f"  Output preview:")
                            for line in run_output.split('\n')[:5]:
                                print(f"    {line}")
                        else:
                            print(f"  ✗ Execution failed")
                else:
                    print(f"  ✗ Compilation failed")
                    print(f"  {output[:200]}")
    else:
        # Generate single file
        code = generate_complex_program(args.lines)
        
        with open(args.output, 'w') as f:
            f.write(code)
        
        line_count = code.count('\n')
        print(f"Generated {args.output} ({line_count} lines)")
        
        if args.validate or args.run:
            success, output = compile_kotlin_file(args.output)
            if success:
                print(f"✓ Compilation successful")
                
                if args.run:
                    run_success, run_output = run_kotlin_program(args.output)
                    if run_success:
                        print(f"✓ Execution successful")
                        print(f"\nProgram output:")
                        print("-" * 60)
                        print(run_output)
                        print("-" * 60)
                    else:
                        print(f"✗ Execution failed")
                        print(run_output)
            else:
                print(f"✗ Compilation failed")
                print(output)


if __name__ == '__main__':
    main()
