#!/usr/bin/env python3
"""
Step 3: High Complexity Kotlin Generator

This generator creates extremely complex Kotlin code that pushes the limits
of what compiles correctly. Target: ~25% compilation success rate.

Complexity increases through:
1. Deep nesting (15+ levels)
2. Complex expressions with multiple operations
3. Lambda functions and higher-order functions
4. Generic types and nullable types
5. Extension functions
6. Nested classes and inner classes
7. Complex control flow
8. Data classes and sealed classes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from step2_refined_generator import RefinedKotlinGenerator, Scope, compile_kotlin_code
from pathlib import Path
import random
from typing import List


class HighComplexityGenerator(RefinedKotlinGenerator):
    """Generates extremely complex Kotlin code"""
    
    COMPLEXITY_PRESETS = {
        'low': {'max_depth': 3, 'max_statements': 10},
        'medium': {'max_depth': 5, 'max_statements': 20},
        'high': {'max_depth': 8, 'max_statements': 40},
        'very_high': {'max_depth': 12, 'max_statements': 60},
        'extreme': {'max_depth': 15, 'max_statements': 100},
    }
    
    def __init__(self, max_depth: int = 15, max_statements: int = 100):
        super().__init__(max_depth, max_statements)
        self.enable_lambdas = True
        self.enable_generics = True
        self.enable_nullables = True
        self.enable_extensions = True
        self.enable_data_classes = True
        
    def generate_complex_type(self) -> str:
        """Generate potentially complex type including generics and nullables"""
        base_type = self.generate_simple_type()
        
        # Add nullable 40% of the time
        if self.enable_nullables and random.random() < 0.4:
            base_type += "?"
        
        # Add generic 30% of the time
        if self.enable_generics and random.random() < 0.3 and base_type in ['List', 'Map', 'Set']:
            inner_type = random.choice(['Int', 'String', 'Boolean'])
            base_type = f"List<{inner_type}>"
        
        return base_type
    
    def generate_simple_type(self) -> str:
        """Generate type name including collections"""
        types = ['Int', 'String', 'Boolean', 'Double', 'Long', 'List', 'Map', 'Set', 'Any']
        return random.choice(types)
    
    def generate_literal(self, type_name: str) -> str:
        """Generate literal with null support"""
        # Strip nullable marker
        base_type = type_name.rstrip('?')
        
        # Return null sometimes for nullable types
        if '?' in type_name and random.random() < 0.3:
            return 'null'
        
        # Handle generic types
        if base_type.startswith('List'):
            return 'listOf()'
        if base_type.startswith('Map'):
            return 'mapOf()'
        if base_type.startswith('Set'):
            return 'setOf()'
        if base_type == 'Any':
            return random.choice(['42', '"text"', 'true'])
        
        # Delegate to parent for basic types
        return super().generate_literal(base_type)
    
    def generate_complex_expression(self, expected_type: str = None) -> str:
        """Generate complex expression with operations"""
        if random.random() < 0.3:
            var = self.get_random_variable()
            if var:
                var_name, var_type = var
                # Add null-safe call for nullable types
                if '?' in var_type and random.random() < 0.5:
                    return f"{var_name}?.toString()"
                # Add property access
                if random.random() < 0.3:
                    return f"{var_name}.toString()"
                return var_name
        
        # Fallback to simple expression
        return self.generate_expression(expected_type)
    
    def generate_lambda_expression(self) -> str:
        """Generate a lambda expression"""
        param = self.generate_identifier("x")
        operation = random.choice([
            f"{param} * 2",
            f"{param} + 1",
            f"{param}.toString()",
            f"println({param})"
        ])
        return f"{{ {param} -> {operation} }}"
    
    def generate_when_statement(self) -> List[str]:
        """Generate a when expression/statement"""
        if self.current_depth >= self.max_depth or self.statement_count >= self.max_statements:
            return []
        
        self.current_depth += 1
        lines = []
        
        var = self.get_random_variable()
        if var:
            var_name, var_type = var
            lines.append(f"{self.indent()}when ({var_name}) {{")
        else:
            lines.append(f"{self.indent()}when {{")
        
        self.indent_level += 1
        
        # Generate 2-4 branches
        num_branches = random.randint(2, 4)
        for i in range(num_branches):
            if i < num_branches - 1:
                # Specific case
                value = self.generate_literal('Int')
                lines.append(f"{self.indent()}{value} -> {{")
            else:
                # Else branch
                lines.append(f"{self.indent()}else -> {{")
            
            self.enter_scope()
            self.indent_level += 1
            lines.extend(self.generate_statements(max_count=2))
            self.indent_level -= 1
            self.exit_scope()
            lines.append(f"{self.indent()}}}")
        
        self.indent_level -= 1
        lines.append(f"{self.indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def generate_try_catch(self) -> List[str]:
        """Generate try-catch block"""
        if self.current_depth >= self.max_depth or self.statement_count >= self.max_statements:
            return []
        
        self.current_depth += 1
        lines = []
        
        lines.append(f"{self.indent()}try {{")
        self.enter_scope()
        self.indent_level += 1
        lines.extend(self.generate_statements(max_count=2))
        self.indent_level -= 1
        self.exit_scope()
        lines.append(f"{self.indent()}}} catch (e: Exception) {{")
        
        self.enter_scope()
        self.current_scope.declare_variable("e", "Exception", mutable=False)
        self.indent_level += 1
        lines.append(f"{self.indent()}println(e.message)")
        self.indent_level -= 1
        self.exit_scope()
        lines.append(f"{self.indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def generate_data_class(self) -> List[str]:
        """Generate a data class"""
        if self.current_depth >= self.max_depth:
            return []
        
        self.current_depth += 1
        lines = []
        
        class_name = self.generate_identifier("Data").capitalize()
        
        # Generate properties
        prop_count = random.randint(1, 3)
        props = []
        for _ in range(prop_count):
            prop_name = self.generate_identifier("prop")
            prop_type = self.generate_simple_type()
            props.append(f"val {prop_name}: {prop_type}")
        
        props_str = ", ".join(props)
        lines.append(f"{self.indent()}data class {class_name}({props_str})")
        
        self.current_depth -= 1
        return lines
    
    def generate_enum_class(self) -> List[str]:
        """Generate an enum class"""
        if self.current_depth >= self.max_depth:
            return []
        
        self.current_depth += 1
        lines = []
        
        enum_name = self.generate_identifier("Enum").capitalize()
        values = [self.generate_identifier("VALUE").upper() for _ in range(3)]
        
        lines.append(f"{self.indent()}enum class {enum_name} {{")
        self.indent_level += 1
        lines.append(f"{self.indent()}{', '.join(values)}")
        self.indent_level -= 1
        lines.append(f"{self.indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def generate_higher_order_function(self) -> List[str]:
        """Generate function that takes lambda parameter"""
        if self.current_depth >= self.max_depth:
            return []
        
        self.current_depth += 1
        lines = []
        
        func_name = self.generate_identifier("process")
        param_name = self.generate_identifier("item")
        lambda_param = self.generate_identifier("fn")
        
        lines.append(f"{self.indent()}fun {func_name}({param_name}: Int, {lambda_param}: (Int) -> Int): Int {{")
        
        self.enter_scope()
        self.current_scope.declare_variable(param_name, "Int", mutable=False)
        self.indent_level += 1
        lines.append(f"{self.indent()}return {lambda_param}({param_name})")
        self.indent_level -= 1
        self.exit_scope()
        
        lines.append(f"{self.indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def generate_extension_function(self) -> List[str]:
        """Generate extension function"""
        if self.current_depth >= self.max_depth:
            return []
        
        self.current_depth += 1
        lines = []
        
        receiver_type = random.choice(['String', 'Int', 'List<Int>'])
        func_name = self.generate_identifier("ext")
        return_type = random.choice(['Int', 'String', 'Boolean'])
        
        lines.append(f"{self.indent()}fun {receiver_type}.{func_name}(): {return_type} {{")
        self.indent_level += 1
        lines.append(f"{self.indent()}return {self.generate_literal(return_type)}")
        self.indent_level -= 1
        lines.append(f"{self.indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def generate_complex_statement(self) -> List[str]:
        """Generate complex statement"""
        if self.statement_count >= self.max_statements:
            return []
        
        depth_factor = self.current_depth / max(self.max_depth, 1)
        
        # More complex constructs
        choices = [
            (self.generate_variable_declaration, 2.0),
            (self.generate_print_statement, 1.5),
        ]
        
        # Add complex constructs if not too deep
        if self.current_depth < self.max_depth - 2:
            choices.extend([
                (lambda: self.generate_if_statement(), 1.5 * (1 - depth_factor)),
                (lambda: self.generate_for_loop(), 1.2 * (1 - depth_factor)),
                (lambda: self.generate_while_loop(), 0.8 * (1 - depth_factor)),
                (lambda: self.generate_when_statement(), 1.0 * (1 - depth_factor)),
                (lambda: self.generate_try_catch(), 0.5 * (1 - depth_factor)),
            ])
        
        # Add assignment if mutable vars exist
        if self.current_scope.get_mutable_variables():
            choices.append((self.generate_assignment, 1.0))
        
        functions, weights = zip(*choices)
        func = random.choices(functions, weights=weights)[0]
        result = func()
        
        if isinstance(result, str):
            return [result] if result else []
        return result if result else []
    
    def generate_statement(self) -> List[str]:
        """Override to use complex statements"""
        return self.generate_complex_statement()
    
    def generate(self) -> str:
        """Generate extremely complex Kotlin code"""
        # Reset state
        self.current_depth = 0
        self.statement_count = 0
        self.indent_level = 0
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.id_counter = 0
        
        lines = []
        
        # Add more top-level constructs
        if random.random() > 0.5:
            lines.extend(self.generate_data_class())
            lines.append("")
        
        if random.random() > 0.5:
            lines.extend(self.generate_enum_class())
            lines.append("")
        
        if random.random() > 0.6:
            lines.extend(self.generate_extension_function())
            lines.append("")
        
        if random.random() > 0.5:
            lines.extend(self.generate_higher_order_function())
            lines.append("")
        
        if random.random() > 0.5:
            lines.extend(self.generate_class())
            lines.append("")
        
        if random.random() > 0.4:
            lines.extend(self.generate_function(is_top_level=True))
            lines.append("")
        
        # Always include main with complex code
        lines.extend(self.generate_main_function())
        
        return "\n".join(lines)


def test_high_complexity(num_samples: int = 200, complexity: str = "extreme"):
    """Test high complexity generator"""
    print(f"Step 3: Testing High Complexity Generator")
    print(f"Samples: {num_samples}, Complexity: {complexity}")
    print("=" * 60)
    
    success_count = 0
    failed_samples = []
    
    output_dir = Path(__file__).parent / "step3_results"
    output_dir.mkdir(exist_ok=True)
    
    for i in range(num_samples):
        if (i + 1) % 20 == 0:
            print(f"Progress: {i+1}/{num_samples}")
        
        generator = HighComplexityGenerator.from_complexity(complexity)
        code = generator.generate()
        
        # Save all samples for analysis
        sample_file = output_dir / f"sample_{i:04d}.kt"
        sample_file.write_text(code)
        
        success, error = compile_kotlin_code(code)
        
        if success:
            success_count += 1
        else:
            failed_samples.append((i, error))
            error_file = output_dir / f"error_{i:04d}.txt"
            error_file.write_text(error)
    
    success_rate = (success_count / num_samples) * 100
    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Success: {success_count}/{num_samples} ({success_rate:.1f}%)")
    print(f"  Failed: {len(failed_samples)}")
    print(f"{'='*60}")
    
    if failed_samples:
        print(f"\nSamples saved to: {output_dir}")
        print(f"\nFirst few errors:")
        for i, (idx, error) in enumerate(failed_samples[:3]):
            print(f"\nSample {idx}:")
            print(error[:200])
    
    return success_rate


def main():
    import argparse
    parser = argparse.ArgumentParser(description='High Complexity Kotlin Generator (Step 3)')
    parser.add_argument('--test', action='store_true', help='Run test suite')
    parser.add_argument('--samples', type=int, default=200, help='Number of test samples')
    parser.add_argument('--complexity', default='extreme', 
                       choices=['low', 'medium', 'high', 'very_high', 'extreme'])
    parser.add_argument('--generate', action='store_true', help='Generate a single sample')
    
    args = parser.parse_args()
    
    if args.test:
        test_high_complexity(args.samples, args.complexity)
    elif args.generate:
        gen = HighComplexityGenerator.from_complexity(args.complexity)
        print(gen.generate())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
