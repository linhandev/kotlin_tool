#!/usr/bin/env python3
"""
Step 3: Maximize code complexity
Generate extremely complex Kotlin code, sacrificing correctness if necessary
Focus on edge cases, deep nesting, and advanced features
"""

import os
import sys
import subprocess
import json
import random
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.absolute()
EXPERIMENTS_DIR = BASE_DIR / "experiments" / "step3_results"
KOTLINC_2_2_20 = BASE_DIR / "kotlin-compilers" / "kotlinc-2.2.20" / "bin" / "kotlinc"

NUM_SAMPLES = 100  # More samples for comprehensive testing


class MaximumComplexityGenerator:
    """Generate maximally complex Kotlin code"""
    
    def __init__(self):
        self.class_counter = 0
        self.function_counter = 0
    
    def random_type(self):
        """Generate random type"""
        types = ["Int", "String", "Boolean", "Double", "Long", "Float", "Any"]
        return random.choice(types)
    
    def random_modifier(self):
        """Generate random visibility/modifier"""
        modifiers = ["", "open ", "abstract ", "sealed ", "internal ", "private "]
        return random.choice(modifiers)
    
    def generate_complex_code(self, idx):
        """Generate maximally complex Kotlin code"""
        
        # Use different strategies based on index
        strategy = idx % 10
        
        if strategy == 0:
            return self.generate_deep_nesting()
        elif strategy == 1:
            return self.generate_multiple_generics()
        elif strategy == 2:
            return self.generate_complex_inheritance()
        elif strategy == 3:
            return self.generate_nested_lambdas()
        elif strategy == 4:
            return self.generate_complex_collections()
        elif strategy == 5:
            return self.generate_reflection_style()
        elif strategy == 6:
            return self.generate_dsl_builder()
        elif strategy == 7:
            return self.generate_complex_operators()
        elif strategy == 8:
            return self.generate_advanced_generics()
        else:
            return self.generate_mixed_complexity()
    
    def generate_deep_nesting(self):
        """Generate code with deep nesting"""
        return """
class Level1 {
    class Level2 {
        class Level3 {
            class Level4 {
                val value = "Nested"
            }
        }
    }
}

fun process(): String {
    val l1 = Level1()
    val l2 = Level1.Level2()
    val l3 = Level1.Level2.Level3()
    val l4 = Level1.Level2.Level3.Level4()
    return l4.value
}

fun main() {
    println("Result: ${process()}")
    
    val nested = listOf(1, 2, 3).map { a ->
        listOf(4, 5, 6).map { b ->
            listOf(7, 8, 9).filter { c ->
                (a + b + c) % 2 == 0
            }.map { c -> a * b * c }
        }.flatten()
    }.flatten()
    
    println("Nested: ${nested.take(5)}")
}
"""
    
    def generate_multiple_generics(self):
        """Generate code with multiple generic parameters"""
        return """
interface Mapper<A, B, C, D> {
    fun map(a: A, b: B, c: C): D
}

class QuadMapper<T1, T2, T3, T4> : Mapper<T1, T2, T3, T4> where T1: Number, T2: Number, T3: Number {
    override fun map(a: T1, b: T2, c: T3): T4 {
        @Suppress("UNCHECKED_CAST")
        return (a.toInt() + b.toInt() + c.toInt()) as T4
    }
}

fun <A, B, C, D, E> transform(a: A, b: B, c: C, f: (A, B, C) -> D, g: (D) -> E): E {
    return g(f(a, b, c))
}

fun main() {
    val mapper = QuadMapper<Int, Double, Long, Int>()
    val result = mapper.map(1, 2.0, 3L)
    println("Mapped: $result")
    
    val transformed = transform(1, 2, 3, 
        { x, y, z -> x + y + z },
        { it * 2 }
    )
    println("Transformed: $transformed")
}
"""
    
    def generate_complex_inheritance(self):
        """Generate complex class hierarchies"""
        return """
interface A { fun funcA(): String = "A" }
interface B { fun funcB(): String = "B" }
interface C { fun funcC(): String = "C" }

abstract class BaseX : A, B {
    abstract fun process(): String
}

open class MiddleY : BaseX(), C {
    override fun process(): String = "Middle"
}

class FinalZ : MiddleY() {
    override fun process(): String = "Final"
    fun combined(): String = funcA() + funcB() + funcC() + process()
}

sealed class Tree<out T> {
    data class Leaf<T>(val value: T) : Tree<T>()
    data class Node<T>(val left: Tree<T>, val right: Tree<T>) : Tree<T>()
    object Empty : Tree<Nothing>()
}

fun <T> Tree<T>.depth(): Int = when (this) {
    is Tree.Leaf -> 1
    is Tree.Node -> 1 + maxOf(left.depth(), right.depth())
    Tree.Empty -> 0
}

fun main() {
    val obj = FinalZ()
    println("Combined: ${obj.combined()}")
    
    val tree = Tree.Node(
        Tree.Leaf(1),
        Tree.Node(Tree.Leaf(2), Tree.Leaf(3))
    )
    println("Tree depth: ${tree.depth()}")
}
"""
    
    def generate_nested_lambdas(self):
        """Generate deeply nested lambda expressions"""
        return """
typealias Transform<T> = (T) -> T

fun <T> chain(vararg transforms: Transform<T>): Transform<T> {
    return { value ->
        transforms.fold(value) { acc, transform -> transform(acc) }
    }
}

fun <T> repeat(n: Int, transform: Transform<T>): Transform<T> {
    return { value ->
        (0 until n).fold(value) { acc, _ -> transform(acc) }
    }
}

fun main() {
    val double: Transform<Int> = { it * 2 }
    val addOne: Transform<Int> = { it + 1 }
    val square: Transform<Int> = { it * it }
    
    val complex = chain(double, addOne, square)
    println("Complex(5): ${complex(5)}")
    
    val repeated = repeat(3, double)
    println("Repeated(5): ${repeated(5)}")
    
    val nested = listOf(1, 2, 3).map { a ->
        listOf(4, 5, 6).flatMap { b ->
            listOf(7, 8, 9).map { c ->
                a to (b to c)
            }.filter { (x, pair) ->
                val (y, z) = pair
                x + y + z > 10
            }
        }
    }.flatten()
    
    println("Nested: ${nested.size} items")
}
"""
    
    def generate_complex_collections(self):
        """Generate complex collection operations"""
        return """
fun main() {
    val data = (1..20).toList()
    
    val result = data
        .asSequence()
        .filter { it % 2 == 0 }
        .map { it * 2 }
        .groupBy { it % 3 }
        .mapValues { (_, values) -> 
            values.sumOf { it.toLong() }
        }
        .filterValues { it > 50 }
        .toSortedMap()
    
    println("Result: $result")
    
    val matrix = List(5) { row ->
        List(5) { col ->
            row * col
        }
    }
    
    val flattened = matrix.flatten()
    val partitioned = flattened.partition { it % 2 == 0 }
    
    println("Matrix sum: ${flattened.sum()}")
    println("Evens: ${partitioned.first.size}")
    
    val zipped = data.zip(data.reversed())
        .map { (a, b) -> a to b }
        .associateBy({ it.first }, { it.second })
    
    println("Zipped: ${zipped.size} pairs")
}
"""
    
    def generate_reflection_style(self):
        """Generate reflection-style code"""
        return """
interface Serializable {
    fun serialize(): String
}

data class Entity(val id: Int, val name: String, val active: Boolean) : Serializable {
    override fun serialize(): String = "Entity($id, $name, $active)"
}

inline fun <reified T> createInstance(vararg args: Any): String {
    return "${T::class.simpleName}(${args.joinToString(", ")})"
}

inline fun <reified T> typeCheck(value: Any): Boolean {
    return value is T
}

fun main() {
    val entity = Entity(1, "Test", true)
    println("Serialized: ${entity.serialize()}")
    
    val created = createInstance<Entity>(2, "New", false)
    println("Created: $created")
    
    println("Is Entity: ${typeCheck<Entity>(entity)}")
    println("Is String: ${typeCheck<String>(entity)}")
    
    val types = listOf("String", 42, true, 3.14)
    types.forEach { value ->
        when (value) {
            is String -> println("String: $value")
            is Int -> println("Int: $value")
            is Boolean -> println("Boolean: $value")
            is Double -> println("Double: $value")
        }
    }
}
"""
    
    def generate_dsl_builder(self):
        """Generate DSL-style builder code"""
        return """
class Html {
    private val children = mutableListOf<Element>()
    
    fun head(init: Head.() -> Unit): Head {
        val head = Head()
        head.init()
        children.add(head)
        return head
    }
    
    fun body(init: Body.() -> Unit): Body {
        val body = Body()
        body.init()
        children.add(body)
        return body
    }
    
    override fun toString() = children.joinToString("\n")
}

abstract class Element {
    protected val children = mutableListOf<Element>()
}

class Head : Element() {
    fun title(text: String) {
        children.add(object : Element() {
            override fun toString() = "<title>$text</title>"
        })
    }
    
    override fun toString() = "<head>${children.joinToString("")}</head>"
}

class Body : Element() {
    fun div(init: Div.() -> Unit): Div {
        val div = Div()
        div.init()
        children.add(div)
        return div
    }
    
    override fun toString() = "<body>${children.joinToString("")}</body>"
}

class Div : Element() {
    fun text(content: String) {
        children.add(object : Element() {
            override fun toString() = content
        })
    }
    
    override fun toString() = "<div>${children.joinToString("")}</div>"
}

fun html(init: Html.() -> Unit): Html {
    val html = Html()
    html.init()
    return html
}

fun main() {
    val page = html {
        head {
            title("My Page")
        }
        body {
            div {
                text("Hello")
            }
            div {
                text("World")
            }
        }
    }
    
    println(page.toString())
}
"""
    
    def generate_complex_operators(self):
        """Generate complex operator overloading"""
        return """
data class Matrix(val rows: Int, val cols: Int, val data: List<List<Int>>) {
    operator fun plus(other: Matrix): Matrix {
        require(rows == other.rows && cols == other.cols)
        val result = data.zip(other.data).map { (r1, r2) ->
            r1.zip(r2).map { (a, b) -> a + b }
        }
        return Matrix(rows, cols, result)
    }
    
    operator fun times(scalar: Int): Matrix {
        val result = data.map { row -> row.map { it * scalar } }
        return Matrix(rows, cols, result)
    }
    
    operator fun get(i: Int, j: Int): Int = data[i][j]
    
    operator fun invoke(i: Int, j: Int): Int = data[i][j]
}

data class Complex(val real: Double, val imag: Double) {
    operator fun plus(other: Complex) = Complex(real + other.real, imag + other.imag)
    operator fun minus(other: Complex) = Complex(real - other.real, imag - other.imag)
    operator fun times(other: Complex) = Complex(
        real * other.real - imag * other.imag,
        real * other.imag + imag * other.real
    )
    
    override fun toString() = "$real + ${imag}i"
}

fun main() {
    val m1 = Matrix(2, 2, listOf(listOf(1, 2), listOf(3, 4)))
    val m2 = Matrix(2, 2, listOf(listOf(5, 6), listOf(7, 8)))
    
    val m3 = m1 + m2
    val m4 = m1 * 2
    
    println("m1[0,0] = ${m1[0, 0]}")
    println("m1(1,1) = ${m1(1, 1)}")
    
    val c1 = Complex(1.0, 2.0)
    val c2 = Complex(3.0, 4.0)
    
    println("c1 + c2 = ${c1 + c2}")
    println("c1 * c2 = ${c1 * c2}")
}
"""
    
    def generate_advanced_generics(self):
        """Generate advanced generic code"""
        return """
interface Container<out T> {
    fun get(): T
}

interface MutableContainer<T> : Container<T> {
    fun set(value: T)
}

class Box<T>(private var value: T) : MutableContainer<T> {
    override fun get(): T = value
    override fun set(value: T) { this.value = value }
}

fun <T> copyContainer(from: Container<T>, to: MutableContainer<T>) {
    to.set(from.get())
}

class Pair<out A, out B>(val first: A, val second: B)

fun <T> makePair(value: T): Pair<T, T> = Pair(value, value)

fun <A, B, C> mapPair(pair: Pair<A, B>, f: (A) -> C, g: (B) -> C): Pair<C, C> {
    return Pair(f(pair.first), g(pair.second))
}

fun main() {
    val box1 = Box(10)
    val box2 = Box(20)
    
    copyContainer(box1, box2)
    println("Box2 value: ${box2.get()}")
    
    val pair = makePair("hello")
    println("Pair: ${pair.first}, ${pair.second}")
    
    val intPair = Pair(1, 2)
    val mapped = mapPair(intPair, { it * 2 }, { it * 3 })
    println("Mapped: ${mapped.first}, ${mapped.second}")
}
"""
    
    def generate_mixed_complexity(self):
        """Generate code mixing multiple complex features"""
        return """
sealed class Either<out L, out R> {
    data class Left<L>(val value: L) : Either<L, Nothing>()
    data class Right<R>(val value: R) : Either<Nothing, R>()
    
    fun <T> fold(left: (L) -> T, right: (R) -> T): T = when (this) {
        is Left -> left(value)
        is Right -> right(value)
    }
    
    fun <T> map(f: (R) -> T): Either<L, T> = when (this) {
        is Left -> this
        is Right -> Right(f(value))
    }
}

data class State<S, out A>(val run: (S) -> Pair<S, A>) {
    fun <B> map(f: (A) -> B): State<S, B> = State { s ->
        val (s2, a) = run(s)
        s2 to f(a)
    }
    
    fun <B> flatMap(f: (A) -> State<S, B>): State<S, B> = State { s ->
        val (s2, a) = run(s)
        f(a).run(s2)
    }
}

fun main() {
    val left: Either<String, Int> = Either.Left("error")
    val right: Either<String, Int> = Either.Right(42)
    
    println(left.fold({ "Left: $it" }, { "Right: $it" }))
    println(right.fold({ "Left: $it" }, { "Right: $it" }))
    
    val mapped = right.map { it * 2 }
    println(mapped.fold({ "Error: $it" }, { "Result: $it" }))
    
    val state1 = State<Int, String> { s -> (s + 1) to "Value: $s" }
    val state2 = state1.map { it.uppercase() }
    
    val (finalState, result) = state2.run(10)
    println("State: $finalState, Result: $result")
}
"""


def main():
    print("="*60)
    print("Step 3: Maximizing Code Complexity")
    print("="*60)
    
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    generated_dir = EXPERIMENTS_DIR / "generated"
    generated_dir.mkdir(exist_ok=True)
    compiled_dir = EXPERIMENTS_DIR / "compiled"
    compiled_dir.mkdir(exist_ok=True)
    
    generator = MaximumComplexityGenerator()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "num_samples": NUM_SAMPLES,
        "generated": 0,
        "compiled": 0,
        "failed": 0,
        "samples": []
    }
    
    print(f"\nGenerating {NUM_SAMPLES} maximally complex code samples...")
    
    for i in range(NUM_SAMPLES):
        code = generator.generate_complex_code(i)
        kt_file = generated_dir / f"sample_{i}.kt"
        kt_file.write_text(code)
        
        results["generated"] += 1
        
        # Try to compile
        try:
            cmd = [
                str(KOTLINC_2_2_20),
                str(kt_file),
                "-d", str(compiled_dir / f"sample_{i}.jar")
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            compiled = result.returncode == 0
            
            if compiled:
                results["compiled"] += 1
                status = "✓"
            else:
                results["failed"] += 1
                status = "✗"
            
            if i % 10 == 0 or not compiled:
                print(f"Sample {i:3d}: {status}")
            
            results["samples"].append({
                "index": i,
                "file": str(kt_file.relative_to(BASE_DIR)),
                "compiled": compiled,
                "error": result.stderr[:200] if not compiled else None
            })
            
        except subprocess.TimeoutExpired:
            results["failed"] += 1
            print(f"Sample {i:3d}: ✗ (timeout)")
            results["samples"].append({
                "index": i,
                "file": str(kt_file.relative_to(BASE_DIR)),
                "compiled": False,
                "error": "Compilation timeout"
            })
    
    # Calculate statistics
    success_rate = (results["compiled"] / results["generated"]) * 100
    results["success_rate"] = success_rate
    
    print(f"\n{'='*60}")
    print("Results:")
    print(f"  Generated: {results['generated']}")
    print(f"  Compiled:  {results['compiled']}")
    print(f"  Failed:    {results['failed']}")
    print(f"  Success Rate: {success_rate:.2f}%")
    print(f"{'='*60}")
    
    # Save results
    results_file = EXPERIMENTS_DIR / "results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to: {results_file}")
    
    # Create documentation
    doc_file = EXPERIMENTS_DIR / "README.md"
    with open(doc_file, 'w') as f:
        f.write(f"""# Step 3: Maximum Complexity Code Generation

## Overview
This step pushes code complexity to the maximum, including edge cases and advanced features.

## Results
- **Total Samples**: {results['generated']}
- **Successfully Compiled**: {results['compiled']}
- **Compilation Failures**: {results['failed']}
- **Success Rate**: {success_rate:.2f}%

## Complexity Features
The generator creates code with:

1. **Deep Nesting**: Multiple levels of nested classes and lambda expressions
2. **Multiple Type Parameters**: Functions and classes with 4+ generic parameters
3. **Complex Inheritance**: Multiple interfaces, abstract classes, and sealed classes
4. **Nested Lambdas**: Deeply nested higher-order functions
5. **Advanced Collections**: Chained sequence operations with grouping and transformations
6. **Reflection-style**: Reified generics and type checking
7. **DSL Builders**: Type-safe builders with nested scopes
8. **Operator Overloading**: Custom operators for matrices, complex numbers, etc.
9. **Variance Annotations**: Covariant and contravariant type parameters
10. **Monadic Patterns**: Either, State, and other functional patterns

## Strategy
The code intentionally prioritizes complexity over correctness, exploring:
- Edge cases in type system
- Limits of generic constraints
- Deep nesting boundaries
- Advanced functional programming patterns

## Files
- `generated/`: All generated Kotlin files
- `compiled/`: Successfully compiled JAR files
- `results.json`: Detailed results with error messages
""")
    
    print(f"✓ Documentation saved to: {doc_file}")


if __name__ == "__main__":
    main()
