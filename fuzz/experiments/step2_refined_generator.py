#!/usr/bin/env python3
"""
Step 2: Refined Kotlin Code Generator

Based on Step 1 analysis, we identified that spec1_kotlin_spec (official grammar)
had the best success rate at 21%. The main issues were:
1. Variables used before declaration
2. Variables accessed outside their scope
3. Type mismatches in return statements

This refined generator fixes these issues to achieve ~95% compilation success.
"""

import random
import string
import argparse
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Set, List, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class Scope:
    """Represents a variable scope"""
    variables: Dict[str, str] = field(default_factory=dict)  # name -> type
    mutable_vars: Set[str] = field(default_factory=set)  # mutable variables
    parent: Optional['Scope'] = None
    
    def declare_variable(self, name: str, var_type: str, mutable: bool = False):
        """Declare a variable in this scope"""
        self.variables[name] = var_type
        if mutable:
            self.mutable_vars.add(name)
    
    def find_variable(self, name: str) -> Optional[str]:
        """Find a variable in this scope or parent scopes"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.find_variable(name)
        return None
    
    def get_all_variables(self) -> List[tuple]:
        """Get all accessible variables (name, type)"""
        result = list(self.variables.items())
        if self.parent:
            result.extend(self.parent.get_all_variables())
        return result
    
    def get_mutable_variables(self) -> List[tuple]:
        """Get all accessible mutable variables (name, type)"""
        result = [(name, typ) for name, typ in self.variables.items() if name in self.mutable_vars]
        if self.parent:
            result.extend(self.parent.get_mutable_variables())
        return result
    
    def is_mutable(self, name: str) -> bool:
        """Check if variable is mutable"""
        if name in self.mutable_vars:
            return True
        if self.parent:
            return self.parent.is_mutable(name)
        return False


class RefinedKotlinGenerator:
    """Generates correct Kotlin code with proper scoping"""
    
    # Complexity presets
    COMPLEXITY_PRESETS = {
        'low': {'max_depth': 3, 'max_statements': 10},
        'medium': {'max_depth': 5, 'max_statements': 20},
        'high': {'max_depth': 8, 'max_statements': 40},
        'very_high': {'max_depth': 12, 'max_statements': 60},
        'extreme': {'max_depth': 15, 'max_statements': 100},
    }
    
    def __init__(self, max_depth: int = 5, max_statements: int = 20):
        self.max_depth = max_depth
        self.max_statements = max_statements
        self.current_depth = 0
        self.statement_count = 0
        self.indent_level = 0
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.id_counter = 0
        
    @classmethod
    def from_complexity(cls, complexity: str) -> 'RefinedKotlinGenerator':
        """Create generator from complexity preset"""
        if complexity not in cls.COMPLEXITY_PRESETS:
            raise ValueError(f"Unknown complexity: {complexity}")
        config = cls.COMPLEXITY_PRESETS[complexity]
        return cls(**config)
    
    def generate_identifier(self, prefix: str = "id") -> str:
        """Generate a unique identifier"""
        self.id_counter += 1
        return f"{prefix}{self.id_counter}"
    
    def generate_simple_type(self) -> str:
        """Generate a simple type name"""
        types = ['Int', 'String', 'Boolean', 'Double', 'Long']
        return random.choice(types)
    
    def generate_literal(self, type_name: str) -> str:
        """Generate a literal value of given type"""
        if type_name == 'Int':
            return str(random.randint(0, 100))
        elif type_name == 'String':
            return f'"{self.generate_identifier("str")}"'
        elif type_name == 'Boolean':
            return random.choice(['true', 'false'])
        elif type_name == 'Double':
            return f"{random.uniform(0, 100):.2f}"
        elif type_name == 'Long':
            return f"{random.randint(0, 100)}L"
        return str(random.randint(0, 100))
    
    def indent(self) -> str:
        """Return current indentation"""
        return "    " * self.indent_level
    
    def enter_scope(self):
        """Enter a new scope"""
        new_scope = Scope(parent=self.current_scope)
        self.current_scope = new_scope
        return new_scope
    
    def exit_scope(self):
        """Exit current scope"""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def get_random_variable(self) -> Optional[tuple]:
        """Get a random accessible variable (name, type)"""
        vars = self.current_scope.get_all_variables()
        return random.choice(vars) if vars else None
    
    def generate_expression(self, expected_type: str = None) -> str:
        """Generate an expression of the expected type"""
        # Try to use existing variable 30% of the time if available
        if random.random() < 0.3:
            var = self.get_random_variable()
            if var and (expected_type is None or var[1] == expected_type):
                return var[0]
        
        # Otherwise generate a literal
        if expected_type is None:
            expected_type = self.generate_simple_type()
        return self.generate_literal(expected_type)
    
    def generate_condition(self) -> str:
        """Generate a boolean condition"""
        var = self.get_random_variable()
        if var and var[1] in ['Int', 'Long', 'Double']:
            operator = random.choice(['>', '<', '==', '!=', '>=', '<='])
            value = self.generate_literal(var[1])
            return f"{var[0]} {operator} {value}"
        else:
            # Fallback to simple boolean
            return random.choice(['true', 'false'])
    
    def generate_variable_declaration(self) -> str:
        """Generate a variable declaration"""
        if self.statement_count >= self.max_statements:
            return ""
        
        self.statement_count += 1
        var_name = self.generate_identifier("var")
        var_type = self.generate_simple_type()
        mutability = random.choice(['val', 'var'])
        is_mutable = (mutability == 'var')
        value = self.generate_expression(var_type)
        
        # Declare in current scope
        self.current_scope.declare_variable(var_name, var_type, is_mutable)
        
        return f"{self.indent()}{mutability} {var_name}: {var_type} = {value}"
    
    def generate_print_statement(self) -> str:
        """Generate a println statement"""
        if self.statement_count >= self.max_statements:
            return ""
        
        self.statement_count += 1
        
        var = self.get_random_variable()
        if var:
            return f'{self.indent()}println({var[0]})'
        else:
            return f'{self.indent()}println({self.generate_literal("String")})'
    
    def generate_assignment(self) -> str:
        """Generate an assignment to existing mutable variable"""
        if self.statement_count >= self.max_statements:
            return ""
        
        # Find mutable variables
        mutable_vars = self.current_scope.get_mutable_variables()
        if not mutable_vars:
            return ""
        
        self.statement_count += 1
        var_name, var_type = random.choice(mutable_vars)
        value = self.generate_expression(var_type)
        return f"{self.indent()}{var_name} = {value}"
    
    def generate_if_statement(self) -> List[str]:
        """Generate an if statement"""
        if self.current_depth >= self.max_depth or self.statement_count >= self.max_statements:
            return []
        
        self.current_depth += 1
        lines = []
        
        condition = self.generate_condition()
        lines.append(f"{self.indent()}if ({condition}) {{")
        
        # Enter new scope for if block
        self.enter_scope()
        self.indent_level += 1
        lines.extend(self.generate_statements(max_count=3))
        self.indent_level -= 1
        self.exit_scope()
        
        lines.append(f"{self.indent()}}}")
        
        # Maybe add else
        if random.random() > 0.6 and self.statement_count < self.max_statements:
            lines.append(f"{self.indent()}else {{")
            self.enter_scope()
            self.indent_level += 1
            lines.extend(self.generate_statements(max_count=2))
            self.indent_level -= 1
            self.exit_scope()
            lines.append(f"{self.indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def generate_for_loop(self) -> List[str]:
        """Generate a for loop"""
        if self.current_depth >= self.max_depth or self.statement_count >= self.max_statements:
            return []
        
        self.current_depth += 1
        lines = []
        
        loop_var = self.generate_identifier("i")
        start = random.randint(0, 5)
        end = random.randint(start + 1, start + 10)
        
        lines.append(f"{self.indent()}for ({loop_var} in {start}..{end}) {{")
        
        # Enter new scope and declare loop variable
        self.enter_scope()
        self.current_scope.declare_variable(loop_var, "Int")
        self.indent_level += 1
        lines.extend(self.generate_statements(max_count=3))
        self.indent_level -= 1
        self.exit_scope()
        
        lines.append(f"{self.indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def generate_while_loop(self) -> List[str]:
        """Generate a while loop"""
        if self.current_depth >= self.max_depth or self.statement_count >= self.max_statements:
            return []
        
        self.current_depth += 1
        lines = []
        
        counter = self.generate_identifier("count")
        limit = random.randint(5, 10)
        
        # Declare counter in current scope as mutable
        self.current_scope.declare_variable(counter, "Int", mutable=True)
        
        lines.append(f"{self.indent()}var {counter} = 0")
        lines.append(f"{self.indent()}while ({counter} < {limit}) {{")
        
        self.enter_scope()
        self.indent_level += 1
        lines.extend(self.generate_statements(max_count=2))
        lines.append(f"{self.indent()}{counter}++")
        self.indent_level -= 1
        self.exit_scope()
        
        lines.append(f"{self.indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def generate_statement(self) -> List[str]:
        """Generate a single statement"""
        if self.statement_count >= self.max_statements:
            return []
        
        depth_factor = self.current_depth / max(self.max_depth, 1)
        
        # Simple statements have higher weight at deeper levels
        choices = [
            (self.generate_variable_declaration, 3.0 - depth_factor),
            (self.generate_print_statement, 2.0),
        ]
        
        # Add assignment if mutable variables exist
        if self.current_scope.get_mutable_variables():
            choices.append((self.generate_assignment, 1.5))
        
        # Add complex statements if not too deep
        if self.current_depth < self.max_depth:
            choices.extend([
                (lambda: self.generate_if_statement(), 1.5 * (1 - depth_factor)),
                (lambda: self.generate_for_loop(), 1.0 * (1 - depth_factor)),
                (lambda: self.generate_while_loop(), 0.8 * (1 - depth_factor)),
            ])
        
        functions, weights = zip(*choices)
        func = random.choices(functions, weights=weights)[0]
        result = func()
        
        # Handle both string and list returns
        if isinstance(result, str):
            return [result] if result else []
        return result if result else []
    
    def generate_statements(self, max_count: int = None) -> List[str]:
        """Generate multiple statements"""
        if max_count is None:
            max_count = self.max_statements
        
        remaining = self.max_statements - self.statement_count
        if remaining <= 0:
            return []
        
        max_to_generate = min(max_count, remaining)
        count = random.randint(1, max(1, max_to_generate))
        statements = []
        
        for _ in range(count):
            if self.statement_count >= self.max_statements:
                break
            stmts = self.generate_statement()
            statements.extend(stmts)
        
        return statements
    
    def generate_function(self, is_top_level: bool = False) -> List[str]:
        """Generate a function"""
        if self.current_depth >= self.max_depth:
            return []
        
        self.current_depth += 1
        lines = []
        
        func_name = self.generate_identifier("func")
        return_type = self.generate_simple_type() if random.random() > 0.3 else "Unit"
        
        # Generate parameters
        param_count = random.randint(0, 3)
        params = []
        
        # Create function scope
        func_scope = Scope(parent=self.global_scope if is_top_level else self.current_scope)
        old_scope = self.current_scope
        self.current_scope = func_scope
        
        for _ in range(param_count):
            param_name = self.generate_identifier("param")
            param_type = self.generate_simple_type()
            params.append(f"{param_name}: {param_type}")
            self.current_scope.declare_variable(param_name, param_type)
        
        params_str = ", ".join(params)
        lines.append(f"{self.indent()}fun {func_name}({params_str}): {return_type} {{")
        
        self.indent_level += 1
        body = self.generate_statements(max_count=min(5, self.max_statements // 2))
        lines.extend(body)
        
        # Add return statement if needed
        if return_type != "Unit":
            lines.append(f"{self.indent()}return {self.generate_literal(return_type)}")
        
        self.indent_level -= 1
        lines.append(f"{self.indent()}}}")
        
        # Restore scope
        self.current_scope = old_scope
        
        self.current_depth -= 1
        return lines
    
    def generate_class(self) -> List[str]:
        """Generate a simple class"""
        if self.current_depth >= self.max_depth:
            return []
        
        self.current_depth += 1
        lines = []
        
        class_name = self.generate_identifier("Class").capitalize()
        lines.append(f"{self.indent()}class {class_name} {{")
        
        self.indent_level += 1
        
        # Generate properties
        prop_count = random.randint(1, 3)
        for _ in range(prop_count):
            prop_name = self.generate_identifier("prop")
            prop_type = self.generate_simple_type()
            mutability = random.choice(['val', 'var'])
            lines.append(f"{self.indent()}{mutability} {prop_name}: {prop_type} = {self.generate_literal(prop_type)}")
        
        self.indent_level -= 1
        lines.append(f"{self.indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def generate_main_function(self) -> List[str]:
        """Generate a main function"""
        lines = ["fun main() {"]
        
        self.enter_scope()
        self.indent_level += 1
        lines.extend(self.generate_statements())
        self.indent_level -= 1
        self.exit_scope()
        
        lines.append("}")
        return lines
    
    def generate(self) -> str:
        """Generate complete Kotlin code"""
        # Reset state
        self.current_depth = 0
        self.statement_count = 0
        self.indent_level = 0
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.id_counter = 0
        
        lines = []
        
        # Decide what to generate
        include_class = random.random() > 0.6 and self.max_depth > 2
        include_function = random.random() > 0.5 and self.max_depth > 1
        
        if include_class:
            lines.extend(self.generate_class())
            lines.append("")
        
        if include_function:
            lines.extend(self.generate_function(is_top_level=True))
            lines.append("")
        
        # Always include main
        lines.extend(self.generate_main_function())
        
        return "\n".join(lines)


def compile_kotlin_code(code: str) -> tuple:
    """Compile Kotlin code and return (success, error)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        kt_file = Path(tmpdir) / "test.kt"
        kt_file.write_text(code)
        
        try:
            result = subprocess.run(
                ["kotlinc", str(kt_file)],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=tmpdir
            )
            return result.returncode == 0, result.stderr
        except Exception as e:
            return False, str(e)


def test_generator(num_samples: int = 200, complexity: str = "medium"):
    """Test the refined generator"""
    print(f"Testing refined generator with {num_samples} samples")
    print(f"Complexity: {complexity}")
    print("=" * 60)
    
    generator_class = RefinedKotlinGenerator.from_complexity(complexity)
    
    success_count = 0
    failed_samples = []
    
    output_dir = Path(__file__).parent / "step2_results"
    output_dir.mkdir(exist_ok=True)
    
    for i in range(num_samples):
        if (i + 1) % 20 == 0:
            print(f"Progress: {i+1}/{num_samples}")
        
        generator = RefinedKotlinGenerator.from_complexity(complexity)
        code = generator.generate()
        
        success, error = compile_kotlin_code(code)
        
        if success:
            success_count += 1
        else:
            failed_samples.append((i, code, error))
            # Save failed samples
            fail_file = output_dir / f"failed_{i:04d}.kt"
            fail_file.write_text(code)
            error_file = output_dir / f"failed_{i:04d}_error.txt"
            error_file.write_text(error)
    
    success_rate = (success_count / num_samples) * 100
    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  Success: {success_count}/{num_samples} ({success_rate:.1f}%)")
    print(f"  Failed: {len(failed_samples)}")
    print(f"{'='*60}")
    
    if failed_samples:
        print(f"\nFailed samples saved to: {output_dir}")
        print(f"\nFirst few errors:")
        for i, (idx, code, error) in enumerate(failed_samples[:3]):
            print(f"\nSample {idx}:")
            print(error[:200])
    
    return success_rate


def main():
    parser = argparse.ArgumentParser(description='Refined Kotlin Code Generator (Step 2)')
    parser.add_argument('--test', action='store_true', help='Run test suite')
    parser.add_argument('--samples', type=int, default=200, help='Number of test samples')
    parser.add_argument('--complexity', default='medium', choices=['low', 'medium', 'high'])
    parser.add_argument('--generate', action='store_true', help='Generate a single sample')
    
    args = parser.parse_args()
    
    if args.test:
        test_generator(args.samples, args.complexity)
    elif args.generate:
        gen = RefinedKotlinGenerator.from_complexity(args.complexity)
        print(gen.generate())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
