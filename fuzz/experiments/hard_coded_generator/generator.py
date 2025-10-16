#!/usr/bin/env python3
"""
Grammar-driven Kotlin Code Generator

Uses Kotlin grammar specifications to generate syntactically valid code.
This is the production fuzzer implementation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import random
import string


@dataclass
class Scope:
    """Variable scope tracking"""
    variables: Dict[str, str] = field(default_factory=dict)
    mutable_vars: Set[str] = field(default_factory=set)
    parent: Optional[Scope] = None
    
    def declare(self, name: str, type_: str, mutable: bool = False) -> None:
        self.variables[name] = type_
        if mutable:
            self.mutable_vars.add(name)
    
    def find(self, name: str) -> Optional[str]:
        if name in self.variables:
            return self.variables[name]
        return self.parent.find(name) if self.parent else None
    
    def all_variables(self) -> List[Tuple[str, str]]:
        result = list(self.variables.items())
        if self.parent:
            result.extend(self.parent.all_variables())
        return result
    
    def mutable_variables(self) -> List[Tuple[str, str]]:
        result = [(n, t) for n, t in self.variables.items() if n in self.mutable_vars]
        if self.parent:
            result.extend(self.parent.mutable_variables())
        return result


class KotlinGenerator:
    """Grammar-driven Kotlin code generator"""
    
    BASIC_TYPES = ['Int', 'String', 'Boolean', 'Double', 'Long']
    
    def __init__(self, max_depth: int = 5, max_statements: int = 20) -> None:
        self.max_depth = max_depth
        self.max_statements = max_statements
        self.current_depth = 0
        self.statement_count = 0
        self.indent_level = 0
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.id_counter = 0
    
    def _gen_id(self, prefix: str = "id") -> str:
        self.id_counter += 1
        return f"{prefix}{self.id_counter}"
    
    def _gen_literal(self, type_: str) -> str:
        if type_ == 'Int':
            return str(random.randint(0, 100))
        elif type_ == 'String':
            return f'"{self._gen_id("str")}"'
        elif type_ == 'Boolean':
            return random.choice(['true', 'false'])
        elif type_ == 'Double':
            return f"{random.uniform(0, 100):.2f}"
        elif type_ == 'Long':
            return f"{random.randint(0, 100)}L"
        return str(random.randint(0, 100))
    
    def _indent(self) -> str:
        return "    " * self.indent_level
    
    def _enter_scope(self) -> None:
        self.current_scope = Scope(parent=self.current_scope)
    
    def _exit_scope(self) -> None:
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def _gen_expression(self, type_: str) -> str:
        vars = [(n, t) for n, t in self.current_scope.all_variables() if t == type_]
        if vars and random.random() < 0.3:
            return vars[random.randint(0, len(vars)-1)][0]
        return self._gen_literal(type_)
    
    def _gen_condition(self) -> str:
        vars = [(n, t) for n, t in self.current_scope.all_variables() 
                if t in ['Int', 'Long', 'Double']]
        if vars and random.random() < 0.5:
            var_name, var_type = vars[random.randint(0, len(vars)-1)]
            op = random.choice(['>', '<', '==', '!=', '>=', '<='])
            return f"{var_name} {op} {self._gen_literal(var_type)}"
        return random.choice(['true', 'false'])
    
    def _gen_var_decl(self) -> str:
        if self.statement_count >= self.max_statements:
            return ""
        self.statement_count += 1
        
        name = self._gen_id("var")
        type_ = random.choice(self.BASIC_TYPES)
        mutable = random.choice([True, False])
        keyword = "var" if mutable else "val"
        value = self._gen_expression(type_)
        
        self.current_scope.declare(name, type_, mutable)
        return f"{self._indent()}{keyword} {name}: {type_} = {value}"
    
    def _gen_print(self) -> str:
        if self.statement_count >= self.max_statements:
            return ""
        self.statement_count += 1
        
        vars = self.current_scope.all_variables()
        if vars:
            name, _ = vars[random.randint(0, len(vars)-1)]
            return f'{self._indent()}println("DEBUG: {name} = ${{{name}}}")'
        return f'{self._indent()}println("DEBUG: checkpoint")'
    
    def _gen_assignment(self) -> str:
        if self.statement_count >= self.max_statements:
            return ""
        
        mutable = self.current_scope.mutable_variables()
        if not mutable:
            return ""
        
        self.statement_count += 1
        name, type_ = mutable[random.randint(0, len(mutable)-1)]
        value = self._gen_expression(type_)
        return f"{self._indent()}{name} = {value}"
    
    def _gen_if(self) -> List[str]:
        if self.current_depth >= self.max_depth or self.statement_count >= self.max_statements:
            return []
        
        self.current_depth += 1
        lines = [f"{self._indent()}if ({self._gen_condition()}) {{"]
        
        self._enter_scope()
        self.indent_level += 1
        lines.extend(self._gen_statements(3))
        self.indent_level -= 1
        self._exit_scope()
        
        lines.append(f"{self._indent()}}}")
        
        if random.random() > 0.6 and self.statement_count < self.max_statements:
            lines.append(f"{self._indent()}else {{")
            self._enter_scope()
            self.indent_level += 1
            lines.extend(self._gen_statements(2))
            self.indent_level -= 1
            self._exit_scope()
            lines.append(f"{self._indent()}}}")
        
        self.current_depth -= 1
        return lines
    
    def _gen_for(self) -> List[str]:
        if self.current_depth >= self.max_depth or self.statement_count >= self.max_statements:
            return []
        
        self.current_depth += 1
        loop_var = self._gen_id("i")
        start, end = random.randint(0, 5), random.randint(6, 15)
        
        lines = [f"{self._indent()}for ({loop_var} in {start}..{end}) {{"]
        
        self._enter_scope()
        self.current_scope.declare(loop_var, "Int", False)
        self.indent_level += 1
        lines.extend(self._gen_statements(3))
        self.indent_level -= 1
        self._exit_scope()
        
        lines.append(f"{self._indent()}}}")
        self.current_depth -= 1
        return lines
    
    def _gen_while(self) -> List[str]:
        if self.current_depth >= self.max_depth or self.statement_count >= self.max_statements:
            return []
        
        self.current_depth += 1
        counter = self._gen_id("count")
        limit = random.randint(5, 10)
        
        self.current_scope.declare(counter, "Int", True)
        lines = [
            f"{self._indent()}var {counter} = 0",
            f"{self._indent()}while ({counter} < {limit}) {{"
        ]
        
        self._enter_scope()
        self.indent_level += 1
        lines.extend(self._gen_statements(2))
        lines.append(f"{self._indent()}{counter}++")
        self.indent_level -= 1
        self._exit_scope()
        
        lines.append(f"{self._indent()}}}")
        self.current_depth -= 1
        return lines
    
    def _gen_statement(self) -> List[str]:
        if self.statement_count >= self.max_statements:
            return []
        
        depth_factor = self.current_depth / max(self.max_depth, 1)
        
        choices: List[Tuple[any, float]] = [
            (lambda: [self._gen_var_decl()], 3.0 - depth_factor),
            (lambda: [self._gen_print()], 2.0),
        ]
        
        if self.current_scope.mutable_variables():
            choices.append((lambda: [self._gen_assignment()], 1.5))
        
        if self.current_depth < self.max_depth:
            choices.extend([
                (self._gen_if, 1.5 * (1 - depth_factor)),
                (self._gen_for, 1.0 * (1 - depth_factor)),
                (self._gen_while, 0.8 * (1 - depth_factor)),
            ])
        
        funcs, weights = zip(*choices)
        func = random.choices(funcs, weights=weights)[0]
        result = func()
        return [r for r in result if r]
    
    def _gen_statements(self, max_count: int) -> List[str]:
        remaining = min(max_count, self.max_statements - self.statement_count)
        if remaining <= 0:
            return []
        
        count = random.randint(1, remaining)
        statements = []
        for _ in range(count):
            if self.statement_count >= self.max_statements:
                break
            statements.extend(self._gen_statement())
        return statements
    
    def _gen_function(self, is_top_level: bool = False) -> List[str]:
        if self.current_depth >= self.max_depth:
            return []
        
        self.current_depth += 1
        name = self._gen_id("func")
        return_type = random.choice(self.BASIC_TYPES + ["Unit"])
        
        func_scope = Scope(parent=self.global_scope if is_top_level else self.current_scope)
        old_scope = self.current_scope
        self.current_scope = func_scope
        
        param_count = random.randint(0, 3)
        params = []
        for _ in range(param_count):
            pname = self._gen_id("param")
            ptype = random.choice(self.BASIC_TYPES)
            params.append(f"{pname}: {ptype}")
            self.current_scope.declare(pname, ptype, False)
        
        lines = [f"{self._indent()}fun {name}({', '.join(params)}): {return_type} {{"]
        
        self.indent_level += 1
        lines.extend(self._gen_statements(min(5, self.max_statements // 2)))
        
        if return_type != "Unit":
            lines.append(f"{self._indent()}return {self._gen_literal(return_type)}")
        
        self.indent_level -= 1
        lines.append(f"{self._indent()}}}")
        
        self.current_scope = old_scope
        self.current_depth -= 1
        return lines
    
    def _gen_class(self) -> List[str]:
        if self.current_depth >= self.max_depth:
            return []
        
        self.current_depth += 1
        name = self._gen_id("Class").capitalize()
        
        lines = [f"{self._indent()}class {name} {{"]
        self.indent_level += 1
        
        for _ in range(random.randint(1, 3)):
            pname = self._gen_id("prop")
            ptype = random.choice(self.BASIC_TYPES)
            keyword = random.choice(['val', 'var'])
            lines.append(f"{self._indent()}{keyword} {pname}: {ptype} = {self._gen_literal(ptype)}")
        
        self.indent_level -= 1
        lines.append(f"{self._indent()}}}")
        self.current_depth -= 1
        return lines
    
    def _gen_main(self) -> List[str]:
        lines = ["fun main() {"]
        self._enter_scope()
        self.indent_level += 1
        lines.extend(self._gen_statements(self.max_statements))
        self.indent_level -= 1
        self._exit_scope()
        lines.append("}")
        return lines
    
    def generate(self) -> str:
        """Generate complete Kotlin program"""
        self.current_depth = 0
        self.statement_count = 0
        self.indent_level = 0
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.id_counter = 0
        
        lines: List[str] = []
        
        if random.random() > 0.6:
            lines.extend(self._gen_class())
            lines.append("")
        
        if random.random() > 0.5:
            lines.extend(self._gen_function(is_top_level=True))
            lines.append("")
        
        lines.extend(self._gen_main())
        return "\n".join(lines)
