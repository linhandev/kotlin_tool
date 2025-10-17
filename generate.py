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

Success rate: ~90-100% (improved for valid code generation while maintaining diversity)
"""

import argparse
import random
import subprocess
import tempfile
import os
from pathlib import Path
from typing import List, Tuple, Optional


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
    'vararg', 'tailrec', 'default_parameters',
    # New advanced features
    'interface', 'abstract_class', 'annotation_class', 
    'lazy_property', 'lateinit_property', 'const_val',
    'value_class', 'array_operations', 'string_templates',
    'labeled_returns', 'smart_casts', 'contracts',
    'scope_functions', 'collection_transformations',
    'delegation_pattern', 'coroutine_basics'
]


def generate_data_class() -> Tuple[str, str]:
    """Generate a data class"""
    class_name = f"Data{random.randint(1, 999)}"
    num_props = random.randint(2, 3)
    prop_types = []
    properties = []
    for i in range(num_props):
        prop_type = random.choice(['Int', 'String', 'Boolean'])
        prop_types.append(prop_type)
        properties.append(f"val prop{i}: {prop_type}")
    
    code = f"data class {class_name}({', '.join(properties)})\n\n"
    # Return class name with type info for later use
    return code, f"{class_name}|{'|'.join(prop_types)}"


def generate_sealed_class() -> Tuple[str, str]:
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


def generate_enum_class() -> Tuple[str, str]:
    """Generate an enum class"""
    enum_name = f"Enum{random.randint(1, 999)}"
    values = [f"VALUE{i}" for i in range(random.randint(2, 4))]
    
    code = f"enum class {enum_name} {{ {', '.join(values)} }}\n\n"
    return code, enum_name


def generate_extension_function() -> Tuple[str, str]:
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


def generate_infix_function() -> Tuple[str, str]:
    """Generate an infix function"""
    func_name = f"infix{random.randint(1, 999)}"
    code = f"infix fun Int.{func_name}(other: Int): Int = this + other\n\n"
    return code, func_name


def generate_operator_overload() -> Tuple[str, str]:
    """Generate operator overloading"""
    class_name = f"Op{random.randint(1, 999)}"
    code = f"""data class {class_name}(val value: Int) {{
    operator fun plus(other: {class_name}): {class_name} = {class_name}(value + other.value)
    operator fun times(factor: Int): {class_name} = {class_name}(value * factor)
}}

"""
    return code, class_name


def generate_lambda_usage() -> Tuple[str, str]:
    """Generate lambda and higher-order function usage"""
    code = """val lambda1 = { x: Int -> x * 2 }
val lambda2: (Int, Int) -> Int = { a, b -> a + b }

fun higherOrder(fn: (Int) -> Int): Int = fn(42)

"""
    return code, 'lambda1'


def generate_generic_class() -> Tuple[str, str]:
    """Generate a generic class"""
    class_name = f"Gen{random.randint(1, 999)}"
    code = f"""class {class_name}<T>(val value: T) {{
    fun get(): T = value
    fun <R> map(fn: (T) -> R): {class_name}<R> = {class_name}(fn(value))
}}

"""
    return code, class_name


def generate_nullable_safe_calls() -> Tuple[str, str]:
    """Generate nullable types and safe call examples"""
    code = """val nullable1: String? = if (Random.nextBoolean()) "value" else null
val length1 = nullable1?.length ?: 0
val safe1 = nullable1?.uppercase() ?: "DEFAULT"

"""
    return code, 'nullable1'


def generate_when_expression() -> Tuple[str, str]:
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


def generate_destructuring() -> Tuple[str, str]:
    """Generate destructuring declaration"""
    code = """fun useDestructuring(): Pair<Int, String> {
    val (a, b, c) = Triple(1, "two", 3.0)
    val list1 = listOf(1, 2, 3, 4, 5)
    val (first, second) = list1
    return Pair(first, b)
}

"""
    return code, 'useDestructuring'


def generate_ranges_collections() -> Tuple[str, str]:
    """Generate ranges and collection operations"""
    code = """val range1 = 1..10
val range2 = 10 downTo 1 step 2
val list2 = listOf(1, 2, 3, 4, 5)
val filtered = list2.filter { it > 2 }
val mapped = list2.map { it * 2 }
val reduced = list2.fold(0) { acc, i -> acc + i }

"""
    return code, 'range1'


def generate_sequence_operations() -> Tuple[str, str]:
    """Generate sequence operations"""
    code = """val seq = generateSequence(1) { if (it < 100) it * 2 else null }
val seqList = seq.take(5).toList()

"""
    return code, 'seq'


def generate_property_delegation() -> Tuple[str, str]:
    """Generate property delegation"""
    code = """class Delegate {
    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String {
        return "delegated_${'$'}{property.name}"
    }
}

val delegated: String by Delegate()

"""
    return code, 'delegated'


def generate_companion_object() -> Tuple[str, str]:
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


def generate_nested_class() -> Tuple[str, str]:
    """Generate nested class"""
    outer_name = f"Outer{random.randint(1, 999)}"
    code = f"""class {outer_name} {{
    class Nested {{
        fun doSomething() = 123
    }}
}}

"""
    return code, outer_name


def generate_type_alias() -> Tuple[str, str]:
    """Generate type alias"""
    alias_name = f"TypeAlias{random.randint(1, 999)}"
    code = f"typealias {alias_name} = Map<String, List<Int>>\n\n"
    return code, alias_name


def generate_inline_function() -> Tuple[str, str]:
    """Generate inline function"""
    func_name = f"inline{random.randint(1, 999)}"
    code = f"inline fun {func_name}(block: () -> Unit) {{ block() }}\n\n"
    return code, func_name


def generate_tailrec_function() -> Tuple[str, str]:
    """Generate tailrec function"""
    func_name = f"tailrec{random.randint(1, 999)}"
    code = f"""tailrec fun {func_name}(n: Int, acc: Int = 1): Int {{
    if (n <= 1) return acc
    return {func_name}(n - 1, acc * n)
}}

"""
    return code, func_name


def generate_vararg_function() -> Tuple[str, str]:
    """Generate vararg function"""
    func_name = f"vararg{random.randint(1, 999)}"
    code = f"fun {func_name}(vararg items: Int): Int = items.sum()\n\n"
    return code, func_name


def generate_default_parameters() -> Tuple[str, str]:
    """Generate function with default parameters"""
    func_name = f"default{random.randint(1, 999)}"
    code = f"fun {func_name}(x: Int = 10, y: String = \"default\"): String = \"x=$x, y=$y\"\n\n"
    return code, func_name


def generate_interface() -> Tuple[str, str]:
    """Generate an interface"""
    interface_name = f"Interface{random.randint(1, 999)}"
    code = f"""interface {interface_name} {{
    fun perform(): Int
    fun describe(): String = "default implementation"
}}

class {interface_name}Impl : {interface_name} {{
    override fun perform(): Int = 42
}}

"""
    return code, interface_name


def generate_abstract_class() -> Tuple[str, str]:
    """Generate an abstract class"""
    class_name = f"Abstract{random.randint(1, 999)}"
    code = f"""abstract class {class_name} {{
    abstract fun compute(): Int
    open fun describe(): String = "abstract class"
}}

class {class_name}Concrete : {class_name}() {{
    override fun compute(): Int = 100
}}

"""
    return code, class_name


def generate_annotation_class() -> Tuple[str, str]:
    """Generate an annotation class"""
    annotation_name = f"Ann{random.randint(1, 999)}"
    code = f"""@Target(AnnotationTarget.CLASS, AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.RUNTIME)
annotation class {annotation_name}(val value: String = "default")

@{annotation_name}("test")
fun annotated{random.randint(1, 999)}() = "annotated"

"""
    return code, annotation_name


def generate_lazy_property() -> Tuple[str, str]:
    """Generate lazy property"""
    var_name = f"lazy{random.randint(1, 999)}"
    code = f"""val {var_name}: Int by lazy {{
    println("Computing lazy value")
    42
}}

"""
    return code, var_name


def generate_lateinit_property() -> Tuple[str, str]:
    """Generate lateinit property"""
    var_name = f"lateinit{random.randint(1, 999)}"
    code = f"""class LateinitHolder{random.randint(1, 999)} {{
    lateinit var {var_name}: String
    
    fun initialize() {{
        {var_name} = "initialized"
    }}
    
    fun isInitialized(): Boolean = ::{var_name}.isInitialized
}}

"""
    return code, var_name


def generate_const_val() -> Tuple[str, str]:
    """Generate const val"""
    const_name = f"CONST{random.randint(1, 999)}"
    code = f"""object Constants{random.randint(1, 999)} {{
    const val {const_name} = 42
    const val STRING_CONST = "constant"
}}

"""
    return code, const_name


def generate_value_class() -> Tuple[str, str]:
    """Generate value class (inline class)"""
    class_name = f"Value{random.randint(1, 999)}"
    code = f"""@JvmInline
value class {class_name}(val value: Int) {{
    fun doubled(): Int = value * 2
}}

"""
    return code, class_name


def generate_array_operations() -> Tuple[str, str]:
    """Generate array operations"""
    code = """val arr1 = intArrayOf(1, 2, 3, 4, 5)
val arr2 = arrayOf("a", "b", "c")
val arrSum = arr1.sum()
val arrFiltered = arr1.filter { it > 2 }

"""
    return code, 'arr1'


def generate_string_templates() -> Tuple[str, str]:
    """Generate string templates"""
    code = """val str1 = "Hello"
val str2 = "World"
val templated = "$str1 $str2"
val complex = "${str1.length} characters"
val multiline = \"\"\"
    |Line 1
    |Line 2
    |Line 3
\"\"\".trimMargin()

"""
    return code, 'templated'


def generate_labeled_returns() -> Tuple[str, str]:
    """Generate labeled returns"""
    code = """fun labeledReturn(): Int {
    listOf(1, 2, 3, 4, 5).forEach lit@{
        if (it == 3) return@lit
        println(it)
    }
    return 42
}

"""
    return code, 'labeledReturn'


def generate_smart_casts() -> Tuple[str, str]:
    """Generate smart casts"""
    code = """fun smartCast(obj: Any): String {
    return when (obj) {
        is String -> "String of length ${obj.length}"
        is Int -> "Int value: $obj"
        is List<*> -> "List of size ${obj.size}"
        else -> "Unknown type"
    }
}

"""
    return code, 'smartCast'


def generate_contracts() -> Tuple[str, str]:
    """Generate function with contracts"""
    func_name = f"contract{random.randint(1, 999)}"
    code = f"""@OptIn(ExperimentalContracts::class)
fun {func_name}(s: String?): Boolean {{
    contract {{
        returns(true) implies (s != null)
    }}
    return s != null
}}

"""
    return code, func_name


def generate_scope_functions() -> Tuple[str, str]:
    """Generate scope function usage"""
    code = """val scopeResult1 = "test".let { it.uppercase() }
val scopeResult2 = StringBuilder().apply {
    append("Hello")
    append(" ")
    append("World")
}.toString()

val scopeResult3 = listOf(1, 2, 3).run {
    filter { it > 1 }.sum()
}

"""
    return code, 'scopeResult1'


def generate_collection_transformations() -> Tuple[str, str]:
    """Generate collection transformations"""
    code = """val numbers = listOf(1, 2, 3, 4, 5)
val doubled = numbers.map { it * 2 }
val evens = numbers.filter { it % 2 == 0 }
val grouped = numbers.groupBy { it % 2 }
val flattened = listOf(listOf(1, 2), listOf(3, 4)).flatten()
val zipped = numbers.zip(listOf("a", "b", "c"))

"""
    return code, 'doubled'


def generate_delegation_pattern() -> Tuple[str, str]:
    """Generate delegation pattern"""
    class_name = f"Delegate{random.randint(1, 999)}"
    base_id = random.randint(1, 999)
    code = f"""interface Base{base_id} {{
    fun execute(): String
}}

class BaseImpl{base_id} : Base{base_id} {{
    override fun execute() = "executed"
}}

class {class_name}(b: Base{base_id}) : Base{base_id} by b

"""
    return code, class_name


def generate_coroutine_basics() -> Tuple[str, str]:
    """Generate basic coroutine usage"""
    code = """// Simulated coroutine basics (without suspend)
fun coroutineSimulation(): String {
    val result = buildString {
        append("Start")
        append(" -> ")
        append("End")
    }
    return result
}

"""
    return code, 'coroutineSimulation'


def generate_object_singleton() -> Tuple[str, str]:
    """Generate object singleton"""
    obj_name = f"Singleton{random.randint(1, 999)}"
    code = f"""object {obj_name} {{
    val value = 42
    fun doSomething(): String = "singleton action"
}}

"""
    return code, obj_name


def generate_higher_order_function() -> Tuple[str, str]:
    """Generate higher-order function"""
    func_name = f"higherOrder{random.randint(1, 999)}"
    code = f"""fun {func_name}(operation: (Int) -> Int): Int {{
    return operation(10)
}}

fun {func_name}WithReturn(x: Int, fn: (Int, Int) -> Int): Int {{
    return fn(x, x * 2)
}}

"""
    return code, func_name


def generate_safe_calls() -> Tuple[str, str]:
    """Generate safe call examples"""
    var_name = f"safeCall{random.randint(1, 999)}"
    code = f"""val {var_name}: String? = if (Random.nextBoolean()) "value" else null
val safeLength = {var_name}?.length
val safeUpper = {var_name}?.uppercase()
val chained = {var_name}?.trim()?.uppercase()

"""
    return code, var_name


def generate_elvis_operator() -> Tuple[str, str]:
    """Generate elvis operator examples"""
    var_id = random.randint(1, 999)
    var_name = f"elvis{var_id}"
    nullable_name = f"nullableVal{var_id}"
    code = f"""val {nullable_name}: Int? = if (Random.nextBoolean()) 42 else null
val {var_name} = {nullable_name} ?: 0
val elvisString{var_id} = {nullable_name}?.toString() ?: "default"

"""
    return code, var_name


def generate_collections() -> Tuple[str, str]:
    """Generate collection examples"""
    var_id = random.randint(1, 999)
    var_name = f"collection{var_id}"
    # Use lazy initialization to avoid top-level statements
    code = f"""val {var_name} by lazy {{
    mutableListOf(1, 2, 3).apply {{ add(4) }}
}}
val set{var_id} = setOf(1, 2, 3, 2, 1)
val map{var_id} = mapOf("a" to 1, "b" to 2)

"""
    return code, var_name


def generate_inner_class() -> Tuple[str, str]:
    """Generate inner class"""
    outer_name = f"OuterInner{random.randint(1, 999)}"
    code = f"""class {outer_name} {{
    private val outerValue = 42
    
    inner class Inner {{
        fun accessOuter() = outerValue
    }}
}}

"""
    return code, outer_name


def generate_reified_generics() -> Tuple[str, str]:
    """Generate reified generics"""
    func_name = f"reified{random.randint(1, 999)}"
    code = f"""inline fun <reified T> {func_name}(): String {{
    return T::class.simpleName ?: "unknown"
}}

"""
    return code, func_name


# Feature generator mapping
FEATURE_GENERATORS = {
    'data_class': generate_data_class,
    'sealed_class': generate_sealed_class,
    'enum_class': generate_enum_class,
    'object_singleton': generate_object_singleton,
    'extension_function': generate_extension_function,
    'infix_function': generate_infix_function,
    'operator_overload': generate_operator_overload,
    'lambda': generate_lambda_usage,
    'higher_order_function': generate_higher_order_function,
    'generics': generate_generic_class,
    'nullable_types': generate_nullable_safe_calls,
    'safe_calls': generate_safe_calls,
    'elvis_operator': generate_elvis_operator,
    'when_expression': generate_when_expression,
    'destructuring': generate_destructuring,
    'ranges': generate_ranges_collections,
    'collections': generate_collections,
    'sequences': generate_sequence_operations,
    'property_delegation': generate_property_delegation,
    'companion_object': generate_companion_object,
    'nested_class': generate_nested_class,
    'inner_class': generate_inner_class,
    'type_alias': generate_type_alias,
    'inline_function': generate_inline_function,
    'reified_generics': generate_reified_generics,
    'tailrec': generate_tailrec_function,
    'vararg': generate_vararg_function,
    'default_parameters': generate_default_parameters,
    # New features
    'interface': generate_interface,
    'abstract_class': generate_abstract_class,
    'annotation_class': generate_annotation_class,
    'lazy_property': generate_lazy_property,
    'lateinit_property': generate_lateinit_property,
    'const_val': generate_const_val,
    'value_class': generate_value_class,
    'array_operations': generate_array_operations,
    'string_templates': generate_string_templates,
    'labeled_returns': generate_labeled_returns,
    'smart_casts': generate_smart_casts,
    'contracts': generate_contracts,
    'scope_functions': generate_scope_functions,
    'collection_transformations': generate_collection_transformations,
    'delegation_pattern': generate_delegation_pattern,
    'coroutine_basics': generate_coroutine_basics,
}


def generate_diverse_program(num_features: int = 10) -> str:
    """Generate a diverse Kotlin program with multiple language features"""
    
    # Select random features
    selected_features = random.sample(list(FEATURE_GENERATORS.keys()), 
                                     min(num_features, len(FEATURE_GENERATORS)))
    
    code_parts = []
    generated_names = []
    
    # Header
    code_parts.append("// Auto-generated diverse Kotlin program\n")
    code_parts.append("// Testing Kotlin Native compiler backend\n")
    code_parts.append("import kotlin.random.Random\n")
    
    # Add contracts import if needed
    if 'contracts' in selected_features:
        code_parts.append("import kotlin.contracts.*\n")
    
    code_parts.append("\n")
    
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
    code_parts.append('    println("=== Program started - testing diverse Kotlin features ===")\n')
    code_parts.append('    println("Features used: {}")'.format(len(generated_names)) + '\n')
    
    # Use more of the generated features
    for idx, (feature, name) in enumerate(generated_names[:10]):  # Use first 10 features
        try:
            if feature == 'data_class':
                # Parse data class info: "ClassName|Type1|Type2|..."
                parts = name.split('|')
                class_name = parts[0]
                prop_types = parts[1:] if len(parts) > 1 else []
                
                # Generate correct arguments for each type
                args = []
                for prop_type in prop_types:
                    if prop_type == 'Int':
                        args.append(str(random.randint(-100, 100)))
                    elif prop_type == 'String':
                        args.append(f'"{random.choice(["a", "b", "c"])}"')
                    elif prop_type == 'Boolean':
                        args.append(random.choice(['true', 'false']))
                
                code_parts.append(f'    val obj{idx} = {class_name}({", ".join(args)})\n')
                code_parts.append(f'    println("Data class: $obj{idx}")\n')
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
            elif feature == 'interface':
                code_parts.append(f'    val impl{idx} = {name}Impl()\n')
                code_parts.append(f'    println("Interface: ${{impl{idx}.perform()}}")\n')
            elif feature == 'abstract_class':
                code_parts.append(f'    val concrete{idx} = {name}Concrete()\n')
                code_parts.append(f'    println("Abstract: ${{concrete{idx}.compute()}}")\n')
            elif feature == 'lazy_property':
                code_parts.append(f'    println("Lazy: ${{{name}}}")\n')
            elif feature == 'scope_functions':
                code_parts.append(f'    println("Scope: ${{scopeResult1}}")\n')
            elif feature == 'smart_casts':
                code_parts.append(f'    println("Smart cast: ${{smartCast("test")}}")\n')
                code_parts.append(f'    println("Smart cast: ${{smartCast(42)}}")\n')
            elif feature == 'object_singleton':
                code_parts.append(f'    println("Singleton: ${{{name}.doSomething()}}")\n')
            elif feature == 'higher_order_function':
                code_parts.append(f'    println("Higher-order: ${{{name} {{ it * 2 }}}}")\n')
        except:
            pass
    
    # Add some general usage with print statements
    code_parts.append('    \n')
    code_parts.append('    println("\\n=== Collection operations ===")\n')
    code_parts.append('    val testNumbers = listOf(1, 2, 3, 4, 5)\n')
    code_parts.append('    println("Numbers: $testNumbers")\n')
    code_parts.append('    println("Sum: ${testNumbers.sum()}")\n')
    code_parts.append('    println("Filtered (>2): ${testNumbers.filter { it > 2 }}")\n')
    code_parts.append('    println("Mapped (*2): ${testNumbers.map { it * 2 }}")\n')
    code_parts.append('    \n')
    code_parts.append('    println("\\n=== Range operations ===")\n')
    code_parts.append('    val testRange = 1..5\n')
    code_parts.append('    println("Range: $testRange")\n')
    code_parts.append('    for (i in testRange) {\n')
    code_parts.append('        println("  Iteration: $i")\n')
    code_parts.append('    }\n')
    code_parts.append('    \n')
    code_parts.append('    println("\\n=== String operations ===")\n')
    code_parts.append('    val testStr = "Kotlin"\n')
    code_parts.append('    println("Original: $testStr")\n')
    code_parts.append('    println("Uppercase: ${testStr.uppercase()}")\n')
    code_parts.append('    println("Length: ${testStr.length}")\n')
    code_parts.append('    \n')
    code_parts.append('    println("\\n=== Program completed successfully ===")\n')
    code_parts.append('}\n')
    
    return ''.join(code_parts)


def compile_with_kotlinc(kotlin_file: str) -> Tuple[bool, str]:
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


def main() -> None:
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
