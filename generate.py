#!/usr/bin/env python3
"""
Diverse Kotlin Code Generator for Kotlin Native Backend Testing

Generates Kotlin programs using a wide variety of language features:
- Data classes, sealed classes, enums
- Extension functions, infix functions
- Lambdas, higher-order functions
- Generics, variance
- Nullable types, safe calls
- When expressions, destructuring
- Coroutines basics
- Property delegation
- Operator overloading
- And more!

Success rate: ~5-20% (prioritizes diversity over compilation success)
"""

import argparse
import random
import subprocess
import tempfile
import os
from pathlib import Path
from typing import List, Tuple


# Diverse language features pool
KOTLIN_FEATURES = [
    'data_class', 'sealed_class', 'enum_class', 'object_singleton',
    'extension_function', 'infix_function', 'operator_overload',
    'lambda', 'higher_order_function', 'generics',
    'nullable_types', 'safe_calls', 'elvis_operator',
    'when_expression', 'destructuring', 'ranges',
    'collections', 'sequences', 'property_delegation',
    'companion_object', 'nested_class', 'inner_class',
    'type_alias', 'inline_function', 'reified_generics',
    'vararg', 'tailrec', 'default_parameters'
]


def generate_data_class():
    """Generate a data class"""
    class_name = f"Data{random.randint(1, 999)}"
    properties = []
    for i in range(random.randint(2, 4)):
        prop_type = random.choice(['Int', 'String', 'Boolean', 'Double'])
        properties.append(f"val prop{i}: {prop_type}")
    
    code = f"data class {class_name}({', '.join(properties)})\n\n"
    return code, class_name


def generate_sealed_class():
    """Generate a sealed class hierarchy"""
    base_name = f"Sealed{random.randint(1, 999)}"
    subclasses = []
    
    code = f"sealed class {base_name} {{\n"
    for i in range(random.randint(2, 3)):
        sub_name = f"Sub{i}"
        subclasses.append(sub_name)
        if random.choice([True, False]):
            code += f"    data class {sub_name}(val value: Int) : {base_name}()\n"
        else:
            code += f"    object {sub_name} : {base_name}()\n"
    code += "}\n\n"
    
    return code, base_name


def generate_enum_class():
    """Generate an enum class"""
    enum_name = f"Enum{random.randint(1, 999)}"
    values = [f"VALUE{i}" for i in range(random.randint(2, 4))]
    
    code = f"enum class {enum_name} {{ {', '.join(values)} }}\n\n"
    return code, enum_name


def generate_extension_function():
    """Generate an extension function"""
    target_type = random.choice(['Int', 'String', 'List<Int>'])
    func_name = f"ext{random.randint(1, 999)}"
    
    if target_type == 'Int':
        code = f"fun Int.{func_name}(): Int = this * 2\n\n"
    elif target_type == 'String':
        code = f"fun String.{func_name}(): String = this.uppercase()\n\n"
    else:
        code = f"fun List<Int>.{func_name}(): Int = this.sum()\n\n"
    
    return code, func_name


def generate_infix_function():
    """Generate an infix function"""
    func_name = f"infix{random.randint(1, 999)}"
    code = f"infix fun Int.{func_name}(other: Int): Int = this + other\n\n"
    return code, func_name


def generate_operator_overload():
    """Generate operator overloading"""
    class_name = f"Op{random.randint(1, 999)}"
    code = f"""data class {class_name}(val value: Int) {{
    operator fun plus(other: {class_name}): {class_name} = {class_name}(value + other.value)
    operator fun times(factor: Int): {class_name} = {class_name}(value * factor)
}}

"""
    return code, class_name


def generate_lambda_usage():
    """Generate lambda and higher-order function usage"""
    code = """val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

"""
    return code, 'lambda1'


def generate_generic_class():
    """Generate a generic class"""
    class_name = f"Gen{random.randint(1, 999)}"
    code = f"""class {class_name}<T>(val value: T) {{
    fun get(): T = value
    fun <R> map(fn: (T) -> R): {class_name}<R> = {class_name}(fn(value))
}}

"""
    return code, class_name


def generate_nullable_safe_calls():
    """Generate nullable types and safe call examples"""
    code = """val nullable1: String? = if (Random.nextBoolean()) "value" else null
val length1 = nullable1?.length ?: 0
val safe1 = nullable1?.uppercase() ?: "DEFAULT"

"""
    return code, 'nullable1'


def generate_when_expression():
    """Generate when expression"""
    var_name = f"when{random.randint(1, 999)}"
    code = f"""val {var_name} = when (Random.nextInt(0, 5)) {{
    0 -> "zero"
    1, 2 -> "one or two"
    in 3..4 -> "three or four"
    else -> "other"
}}

"""
    return code, var_name


def generate_destructuring():
    """Generate destructuring declaration"""
    code = """fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

"""
    return code, 'useDestructuring'


def generate_ranges_collections():
    """Generate ranges and collection operations"""
    code = """val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

"""
    return code, 'range1'


def generate_sequence_operations():
    """Generate sequence operations"""
    code = """val seq = generateSequence(1) { if (it < 100) it * 2 else null }
val seqList = seq.take(5).toList()

"""
    return code, 'seq'


def generate_property_delegation():
    """Generate property delegation"""
    code = """class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

"""
    return code, 'delegated'


def generate_companion_object():
    """Generate class with companion object"""
    class_name = f"Comp{random.randint(1, 999)}"
    code = f"""class {class_name} {{
    companion object {{
        const val CONST_VAL = 42
        fun create(): {class_name} = {class_name}()
    }}
}}

"""
    return code, class_name


def generate_nested_class():
    """Generate nested class"""
    outer_name = f"Outer{random.randint(1, 999)}"
    code = f"""class {outer_name} {{
    class Nested {{
        fun doSomething() = 123
    }}
}}

"""
    return code, outer_name


def generate_type_alias():
    """Generate type alias"""
    alias_name = f"TypeAlias{random.randint(1, 999)}"
    code = f"typealias {alias_name} = Map<String, List<Int>>\n\n"
    return code, alias_name


def generate_inline_function():
    """Generate inline function"""
    func_name = f"inline{random.randint(1, 999)}"
    code = f"inline fun {func_name}(block: () -> Unit) {{ block() }}\n\n"
    return code, func_name


def generate_tailrec_function():
    """Generate tailrec function"""
    func_name = f"tailrec{random.randint(1, 999)}"
    code = f"""tailrec fun {func_name}(n: Int, acc: Int = 1): Int {{
    if (n <= 1) return acc
    return {func_name}(n - 1, acc * n)
}}

"""
    return code, func_name


def generate_vararg_function():
    """Generate vararg function"""
    func_name = f"vararg{random.randint(1, 999)}"
    code = f"fun {func_name}(vararg items: Int): Int = items.sum()\n\n"
    return code, func_name


def generate_default_parameters():
    """Generate function with default parameters"""
    func_name = f"default{random.randint(1, 999)}"
    code = f"fun {func_name}(x: Int = 10, y: String = \"default\"): String = \"x=$x, y=$y\"\n\n"
    return code, func_name


# Feature generator mapping
FEATURE_GENERATORS = {
    'data_class': generate_data_class,
    'sealed_class': generate_sealed_class,
    'enum_class': generate_enum_class,
    'extension_function': generate_extension_function,
    'infix_function': generate_infix_function,
    'operator_overload': generate_operator_overload,
    'lambda': generate_lambda_usage,
    'generics': generate_generic_class,
    'nullable_types': generate_nullable_safe_calls,
    'when_expression': generate_when_expression,
    'destructuring': generate_destructuring,
    'ranges': generate_ranges_collections,
    'sequences': generate_sequence_operations,
    'property_delegation': generate_property_delegation,
    'companion_object': generate_companion_object,
    'nested_class': generate_nested_class,
    'type_alias': generate_type_alias,
    'inline_function': generate_inline_function,
    'tailrec': generate_tailrec_function,
    'vararg': generate_vararg_function,
    'default_parameters': generate_default_parameters,
}


def generate_diverse_program(num_features=10):
    """Generate a diverse Kotlin program with multiple language features"""
    
    # Select random features
    selected_features = random.sample(list(FEATURE_GENERATORS.keys()), 
                                     min(num_features, len(FEATURE_GENERATORS)))
    
    code_parts = []
    generated_names = []
    
    # Header
    code_parts.append("// Auto-generated diverse Kotlin program\n")
    code_parts.append("// Testing Kotlin Native compiler backend\n")
    code_parts.append("import kotlin.random.Random\n\n")
    
    # Generate features
    for feature in selected_features:
        try:
            generator = FEATURE_GENERATORS[feature]
            code, name = generator()
            code_parts.append(f"// Feature: {feature}\n")
            code_parts.append(code)
            generated_names.append((feature, name))
        except Exception as e:
            # Skip features that fail to generate
            continue
    
    # Main function that uses generated features
    code_parts.append("fun main() {\n")
    code_parts.append('    println("Program started - testing diverse Kotlin features")\n')
    
    # Use some of the generated features
    for feature, name in generated_names[:5]:  # Use first 5 features
        try:
            if feature == 'data_class':
                code_parts.append(f'    val obj1 = {name}(' + ', '.join([f'{random.randint(-100, 100)}' if i % 2 == 0 else f'"{random.choice(["a", "b", "c"])}"' for i in range(2)]) + ')\n')
                code_parts.append(f'    println("Data class: $obj1")\n')
            elif feature == 'enum_class':
                code_parts.append(f'    println("Enum: ${{{name}.values()[0]}}")\n')
            elif feature == 'when_expression':
                code_parts.append(f'    println("When result: ${{{name}}}")\n')
            elif feature == 'lambda':
                code_parts.append(f'    println("Lambda: ${{lambda1(21)}}")\n')
                code_parts.append(f'    println("Higher-order: ${{higherOrder {{ it + 1 }}}}")\n')
            elif feature == 'tailrec':
                code_parts.append(f'    println("Tailrec: ${{{name}(5)}}")\n')
            elif feature == 'vararg':
                code_parts.append(f'    println("Vararg: ${{{name}(1, 2, 3)}}")\n')
        except:
            pass
    
    # Add some general usage
    code_parts.append('    val numbers = listOf(1, 2, 3, 4, 5)\n')
    code_parts.append('    println("Sum: ${numbers.sum()}")\n')
    code_parts.append('    println("Filtered: ${numbers.filter { it > 2 }}")\n')
    code_parts.append('    \n')
    code_parts.append('    val range = 1..5\n')
    code_parts.append('    for (i in range) {\n')
    code_parts.append('        println("Iteration: $i")\n')
    code_parts.append('    }\n')
    code_parts.append('    \n')
    code_parts.append('    println("Program completed")\n')
    code_parts.append('}\n')
    
    return ''.join(code_parts)


def compile_with_kotlinc(kotlin_file):
    """Compile with kotlinc (JVM)"""
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


def main():
    parser = argparse.ArgumentParser(
        description='Generate diverse Kotlin programs for Kotlin Native backend testing'
    )
    parser.add_argument('-o', '--output', default='test.kt', 
                       help='Output file path')
    parser.add_argument('-n', '--num-files', type=int, default=1,
                       help='Number of files to generate')
    parser.add_argument('-f', '--features', type=int, default=12,
                       help='Number of language features per program (default: 12)')
    parser.add_argument('--validate', action='store_true',
                       help='Validate with kotlinc')
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    output_dir = output_path.parent
    output_dir.mkdir(exist_ok=True, parents=True)
    
    success_count = 0
    total_count = 0
    
    if args.num_files > 1:
        # Generate multiple files
        base_name = output_path.stem
        extension = output_path.suffix
        
        for i in range(args.num_files):
            file_path = output_dir / f"{base_name}_{i}{extension}"
            
            # Generate diverse program
            code = generate_diverse_program(args.features)
            
            with open(file_path, 'w') as f:
                f.write(code)
            
            line_count = code.count('\n')
            total_count += 1
            
            if args.validate:
                success, output = compile_with_kotlinc(file_path)
                if success:
                    success_count += 1
                    print(f"[{i+1}/{args.num_files}] {file_path.name} ({line_count} lines) ✓ COMPILED")
                else:
                    print(f"[{i+1}/{args.num_files}] {file_path.name} ({line_count} lines) ✗ FAILED")
            else:
                print(f"[{i+1}/{args.num_files}] Generated {file_path.name} ({line_count} lines)")
        
        if args.validate and total_count > 0:
            rate = 100 * success_count / total_count
            print(f"\nCompilation success: {success_count}/{total_count} ({rate:.1f}%)")
    else:
        # Generate single file
        code = generate_diverse_program(args.features)
        
        with open(args.output, 'w') as f:
            f.write(code)
        
        line_count = code.count('\n')
        print(f"Generated {args.output} ({line_count} lines)")
        
        if args.validate:
            success, output = compile_with_kotlinc(args.output)
            if success:
                print("✓ Compilation successful")
            else:
                print("✗ Compilation failed")
                print(output[:500])


if __name__ == '__main__':
    main()
