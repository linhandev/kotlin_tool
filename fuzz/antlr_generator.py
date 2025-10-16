#!/usr/bin/env python3
"""
ANTLR-based Kotlin Code Generator

Generates Kotlin code using grammar rules from ANTLR parser.
Uses random descent through grammar production rules.
"""

from __future__ import annotations
import sys
import random
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field

sys.path.insert(0, str(Path(__file__).parent.parent / "grammar"))

from antlr4 import InputStream, CommonTokenStream
from KotlinLexer import KotlinLexer
from KotlinParser import KotlinParser


@dataclass
class Scope:
    """Tracks variables in current scope"""
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
    
    def all_vars(self) -> List[Tuple[str, str]]:
        result = list(self.variables.items())
        if self.parent:
            result.extend(self.parent.all_vars())
        return result
    
    def mutable_vars_list(self) -> List[Tuple[str, str]]:
        result = [(n, t) for n, t in self.variables.items() if n in self.mutable_vars]
        if self.parent:
            result.extend(self.parent.mutable_vars_list())
        return result


class AntlrKotlinGenerator:
    """Generates Kotlin code using ANTLR grammar"""
    
    TYPES = ['Int', 'String', 'Boolean', 'Double', 'Long']
    
    def __init__(self, max_depth: int = 5, max_statements: int = 20) -> None:
        self.max_depth = max_depth
        self.max_statements = max_statements
        self.depth = 0
        self.stmt_count = 0
        self.indent = 0
        self.scope = Scope()
        self.id_counter = 0
    
    def _id(self, prefix: str = "id") -> str:
        self.id_counter += 1
        return f"{prefix}{self.id_counter}"
    
    def _ind(self) -> str:
        return "    " * self.indent
    
    def _type(self) -> str:
        return random.choice(self.TYPES)
    
    def _literal(self, type_: str) -> str:
        if type_ == 'Int':
            return str(random.randint(0, 100))
        elif type_ == 'String':
            return f'"{self._id("str")}"'
        elif type_ == 'Boolean':
            return random.choice(['true', 'false'])
        elif type_ == 'Double':
            return f"{random.uniform(0, 100):.2f}"
        elif type_ == 'Long':
            return f"{random.randint(0, 100)}L"
        return str(random.randint(0, 100))
    
    def _expr(self, type_: str) -> str:
        vars_of_type = [(n, t) for n, t in self.scope.all_vars() if t == type_]
        if vars_of_type and random.random() < 0.2:
            return random.choice(vars_of_type)[0]
        return self._literal(type_)
    
    def _condition(self) -> str:
        numeric_vars = [(n, t) for n, t in self.scope.all_vars() if t in ['Int', 'Long', 'Double']]
        if numeric_vars and random.random() < 0.5:
            name, type_ = random.choice(numeric_vars)
            op = random.choice(['>', '<', '==', '!=', '>=', '<='])
            return f"{name} {op} {self._literal(type_)}"
        return random.choice(['true', 'false'])
    
    def _property(self) -> str:
        """kotlinParser: property rule"""
        if self.stmt_count >= self.max_statements:
            return ""
        self.stmt_count += 1
        
        name = self._id("prop")
        type_ = self._type()
        mutable = random.choice([True, False])
        keyword = "var" if mutable else "val"
        
        self.scope.declare(name, type_, mutable)
        return f"{self._ind()}{keyword} {name}: {type_} = {self._expr(type_)}"
    
    def _variableDeclaration(self) -> str:
        """kotlinParser: variableDeclaration rule"""
        if self.stmt_count >= self.max_statements:
            return ""
        self.stmt_count += 1
        
        name = self._id("var")
        type_ = self._type()
        mutable = random.choice([True, False])
        keyword = "var" if mutable else "val"
        
        self.scope.declare(name, type_, mutable)
        return f"{self._ind()}{keyword} {name}: {type_} = {self._expr(type_)}"
    
    def _assignment(self) -> str:
        """kotlinParser: assignment rule"""
        if self.stmt_count >= self.max_statements:
            return ""
        
        mutable = self.scope.mutable_vars_list()
        if not mutable:
            return ""
        
        self.stmt_count += 1
        name, type_ = random.choice(mutable)
        return f"{self._ind()}{name} = {self._expr(type_)}"
    
    def _expression(self) -> str:
        """kotlinParser: expression rule - generates println"""
        if self.stmt_count >= self.max_statements:
            return ""
        self.stmt_count += 1
        
        vars = self.scope.all_vars()
        if vars:
            name, _ = random.choice(vars)
            return f'{self._ind()}println("DEBUG: {name} = ${{{name}}}")'
        return f'{self._ind()}println("DEBUG: checkpoint")'
    
    def _ifExpression(self) -> List[str]:
        """kotlinParser: ifExpression rule"""
        if self.depth >= self.max_depth or self.stmt_count >= self.max_statements:
            return []
        
        self.depth += 1
        lines = [f"{self._ind()}if ({self._condition()}) {{"]
        
        old_scope = self.scope
        self.scope = Scope(parent=self.scope)
        self.indent += 1
        lines.extend(self._statements(3))
        self.indent -= 1
        self.scope = old_scope
        
        lines.append(f"{self._ind()}}}")
        
        if random.random() > 0.6:
            lines.append(f"{self._ind()}else {{")
            old_scope = self.scope
            self.scope = Scope(parent=self.scope)
            self.indent += 1
            lines.extend(self._statements(2))
            self.indent -= 1
            self.scope = old_scope
            lines.append(f"{self._ind()}}}")
        
        self.depth -= 1
        return lines
    
    def _forStatement(self) -> List[str]:
        """kotlinParser: forStatement rule"""
        if self.depth >= self.max_depth or self.stmt_count >= self.max_statements:
            return []
        
        self.depth += 1
        loop_var = self._id("i")
        start, end = random.randint(0, 5), random.randint(6, 15)
        
        lines = [f"{self._ind()}for ({loop_var} in {start}..{end}) {{"]
        
        old_scope = self.scope
        self.scope = Scope(parent=self.scope)
        self.scope.declare(loop_var, "Int", False)
        self.indent += 1
        lines.extend(self._statements(3))
        self.indent -= 1
        self.scope = old_scope
        
        lines.append(f"{self._ind()}}}")
        self.depth -= 1
        return lines
    
    def _whileStatement(self) -> List[str]:
        """kotlinParser: whileStatement rule"""
        if self.depth >= self.max_depth or self.stmt_count >= self.max_statements:
            return []
        
        self.depth += 1
        counter = self._id("count")
        limit = random.randint(5, 10)
        
        self.scope.declare(counter, "Int", True)
        lines = [
            f"{self._ind()}var {counter} = 0",
            f"{self._ind()}while ({counter} < {limit}) {{"
        ]
        
        old_scope = self.scope
        self.scope = Scope(parent=self.scope)
        self.indent += 1
        lines.extend(self._statements(2))
        lines.append(f"{self._ind()}{counter}++")
        self.indent -= 1
        self.scope = old_scope
        
        lines.append(f"{self._ind()}}}")
        self.depth -= 1
        return lines
    
    def _statement(self) -> List[str]:
        """kotlinParser: statement rule"""
        if self.stmt_count >= self.max_statements:
            return []
        
        depth_factor = self.depth / max(self.max_depth, 1)
        
        choices: List[Tuple[any, float]] = [
            (lambda: [self._variableDeclaration()], 3.0 - depth_factor),
            (lambda: [self._expression()], 2.0),
        ]
        
        if self.scope.mutable_vars_list():
            choices.append((lambda: [self._assignment()], 1.5))
        
        if self.depth < self.max_depth:
            choices.extend([
                (self._ifExpression, 1.5 * (1 - depth_factor)),
                (self._forStatement, 1.0 * (1 - depth_factor)),
                (self._whileStatement, 0.8 * (1 - depth_factor)),
            ])
        
        funcs, weights = zip(*choices)
        func = random.choices(funcs, weights=weights)[0]
        result = func()
        return [r for r in result if r]
    
    def _statements(self, max_count: int) -> List[str]:
        """kotlinParser: statements rule"""
        remaining = min(max_count, self.max_statements - self.stmt_count)
        if remaining <= 0:
            return []
        
        count = random.randint(1, remaining)
        stmts = []
        for _ in range(count):
            if self.stmt_count >= self.max_statements:
                break
            stmts.extend(self._statement())
        return stmts
    
    def _functionDeclaration(self, is_top: bool = False) -> List[str]:
        """kotlinParser: functionDeclaration rule"""
        if self.depth >= self.max_depth:
            return []
        
        self.depth += 1
        name = self._id("func")
        ret_type = random.choice(self.TYPES + ["Unit"])
        
        old_scope = self.scope
        self.scope = Scope(parent=Scope() if is_top else self.scope)
        
        param_count = random.randint(0, 3)
        params = []
        for _ in range(param_count):
            pname = self._id("param")
            ptype = self._type()
            params.append(f"{pname}: {ptype}")
            self.scope.declare(pname, ptype, False)
        
        lines = [f"{self._ind()}fun {name}({', '.join(params)}): {ret_type} {{"]
        
        self.indent += 1
        lines.extend(self._statements(min(5, self.max_statements // 2)))
        
        if ret_type != "Unit":
            lines.append(f"{self._ind()}return {self._literal(ret_type)}")
        
        self.indent -= 1
        lines.append(f"{self._ind()}}}")
        
        self.scope = old_scope
        self.depth -= 1
        return lines
    
    def _classDeclaration(self) -> List[str]:
        """kotlinParser: classDeclaration rule"""
        if self.depth >= self.max_depth:
            return []
        
        self.depth += 1
        name = self._id("Class").capitalize()
        
        lines = [f"{self._ind()}class {name} {{"]
        self.indent += 1
        
        for _ in range(random.randint(1, 3)):
            lines.append(self._property())
        
        self.indent -= 1
        lines.append(f"{self._ind()}}}")
        self.depth -= 1
        return lines
    
    def _kotlinFile(self) -> List[str]:
        """kotlinParser: kotlinFile rule - top level"""
        lines: List[str] = []
        
        if random.random() > 0.6:
            lines.extend(self._classDeclaration())
            lines.append("")
        
        if random.random() > 0.5:
            lines.extend(self._functionDeclaration(is_top=True))
            lines.append("")
        
        lines.append("fun main() {")
        old_scope = self.scope
        self.scope = Scope(parent=self.scope)
        self.indent += 1
        lines.extend(self._statements(self.max_statements))
        self.indent -= 1
        self.scope = old_scope
        lines.append("}")
        
        return lines
    
    def generate(self) -> str:
        """Generate complete Kotlin program"""
        self.depth = 0
        self.stmt_count = 0
        self.indent = 0
        self.scope = Scope()
        self.id_counter = 0
        
        lines = self._kotlinFile()
        return "\n".join(lines)
