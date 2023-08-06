import ast
import sys

from py2many.analysis import get_id
from typing import List, Optional, Tuple


symbols = {
    ast.Eq: "==",
    ast.Is: "==",
    ast.NotEq: "!=",
    ast.Mult: "*",
    ast.Add: "+",
    ast.Sub: "-",
    ast.Div: "/",
    ast.FloorDiv: "/",
    ast.Mod: "%",
    ast.Lt: "<",
    ast.Gt: ">",
    ast.GtE: ">=",
    ast.LtE: "<=",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitXor: "^",
    ast.BitOr: "|",
    ast.BitAnd: "&",
    ast.Not: "!",
    ast.IsNot: "!=",
    ast.USub: "-",
    ast.And: "&&",
    ast.Or: "||",
    ast.In: "in",
}


def c_symbol(node):
    """Find the equivalent C symbol for a Python ast symbol node"""
    symbol_type = type(node)
    return symbols[symbol_type]


class CLikeTranspiler(ast.NodeVisitor):
    """Provides a base for C-like programming languages"""

    builtin_constants = frozenset(["True", "False"])
    IGNORED_MODULE_LIST = set(
        ["typing", "enum", "dataclasses", "ctypes", "math", "__future__", "asyncio"]
    )

    def __init__(self):
        self._type_map = {}
        self._headers = set([])
        self._usings = set([])
        self._features = set([])
        self._container_type_map = {}
        self._default_type = "auto"
        self._statement_separator = ";"

    def headers(self, meta=None):
        return ""

    def usings(self):
        return ""

    def features(self):
        return ""

    def comment(self, text):
        return f"/* {text} */"

    def _cast(self, name: str, to) -> str:
        return f"({to}) {name}"

    def _slice_value(self, node: ast.AST):
        # 3.9 compatibility shim
        if sys.version_info < (3, 9, 0):
            if not isinstance(node.slice, ast.Index):
                raise NotImplementedError("Advanced Slicing not supported")
            slice_value = node.slice.value
        else:
            slice_value = node.slice
        return slice_value

    def _map_type(self, typename) -> str:
        if isinstance(typename, list):
            raise NotImplementedError(f"{typename} not supported in this context")
        return self._type_map.get(typename, typename)

    def _map_types(self, typenames: List[str]) -> List[str]:
        return [self._map_type(e) for e in typenames]

    def _map_container_type(self, typename) -> str:
        return self._container_type_map.get(typename, self._default_type)

    def _combine_value_index(self, value_type, index_type) -> str:
        return f"{value_type}<{index_type}>"

    def _visit_container_type(self, typename: Tuple) -> str:
        value_type, index_type = typename
        if isinstance(index_type, List):
            index_contains_default = "Any" in index_type
            if not index_contains_default:
                if any(t is None for t in index_type):
                    raise NotImplementedError(f"{typename} not supported")
                index_type = ", ".join(index_type)
        else:
            index_contains_default = index_type == "Any"
        # Avoid types like HashMap<_, foo>. Prefer default_type instead
        if index_contains_default or value_type == self._default_type:
            return self._default_type
        return self._combine_value_index(value_type, index_type)

    def _typename_from_type_node(self, node) -> Optional[str]:
        if isinstance(node, ast.Name):
            return self._map_type(get_id(node))
        elif isinstance(node, ast.ClassDef):
            return get_id(node)
        elif isinstance(node, ast.Tuple):
            return [self._typename_from_type_node(e) for e in node.elts]
        elif isinstance(node, ast.Subscript):
            # Store a tuple like (List, int) or (Dict, (str, int)) for container types
            # in node.container_type
            # And return a target specific type
            slice_value = self._slice_value(node)
            (value_type, index_type) = tuple(
                map(self._typename_from_type_node, (node.value, slice_value))
            )
            value_type = self._map_container_type(value_type)
            node.container_type = (value_type, index_type)
            return self._combine_value_index(value_type, index_type)
        return self._default_type

    def _generic_typename_from_type_node(self, node) -> Optional[str]:
        if isinstance(node, ast.Name):
            return get_id(node)
        elif isinstance(node, ast.ClassDef):
            return get_id(node)
        elif isinstance(node, ast.Tuple):
            return [self._generic_typename_from_type_node(e) for e in node.elts]
        elif isinstance(node, ast.Subscript):
            slice_value = self._slice_value(node)
            (value_type, index_type) = tuple(
                map(self._generic_typename_from_type_node, (node.value, slice_value))
            )
            node.generic_container_type = (value_type, index_type)
            return f"{value_type}[{index_type}]"
        return self._default_type

    def _typename_from_annotation(self, node, attr="annotation") -> str:
        default_type = self._default_type
        typename = default_type
        if hasattr(node, attr):
            type_node = getattr(node, attr)
            typename = self._typename_from_type_node(type_node)
            if isinstance(type_node, ast.Subscript):
                node.container_type = type_node.container_type
                return self._visit_container_type(type_node.container_type)
            if typename is None:
                raise Exception(f"Could not infer: {type_node}")
        return typename

    def _generic_typename_from_annotation(
        self, node, attr="annotation"
    ) -> Optional[str]:
        "Unlike the one above, this doesn't do any target specific mapping"
        typename = None
        if hasattr(node, attr):
            type_node = getattr(node, attr)
            ret = self._generic_typename_from_type_node(type_node)
            if isinstance(type_node, ast.Subscript):
                node.generic_container_type = type_node.generic_container_type
            return ret
        return typename

    def visit(self, node):
        if type(node) in symbols:
            return c_symbol(node)
        else:
            return super().visit(node)

    def visit_Pass(self, node):
        return self.comment("pass")

    def visit_Module(self, node):
        docstring = getattr(node, "docstring_comment", None)
        buf = [self.comment(docstring.value)] if docstring is not None else []
        buf += [self.visit(b) for b in node.body]
        return "\n".join(buf)

    def visit_Name(self, node):
        if node.id in self.builtin_constants:
            return node.id.lower()
        return node.id

    def visit_Ellipsis(self, node):
        return self.comment("...")

    def visit_NameConstant(self, node):
        if node.value is True:
            return "true"
        elif node.value is False:
            return "false"
        elif node.value is None:
            return "NULL"
        elif node.value is Ellipsis:
            return self.visit_Ellipsis(node)
        else:
            return node.value

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            return self.visit_Str(node)
        return str(self.visit_NameConstant(node))

    def visit_Expr(self, node):
        s = self.visit(node.value)
        if isinstance(node.value, ast.Constant) and node.value.value is Ellipsis:
            return s
        if not s:
            return ""
        s = s.strip()
        if not s.endswith(self._statement_separator):
            s += self._statement_separator
        if s == self._statement_separator:
            return ""
        else:
            return s

    def visit_Str(self, node):
        return f'"{node.value}"'

    def visit_arguments(self, node):
        args = [self.visit(arg) for arg in node.args]
        if args == []:
            return [], []
        typenames, args = map(list, zip(*args))
        return typenames, args

    def visit_Return(self, node):
        if node.value:
            return "return {0};".format(self.visit(node.value))
        return "return;"

    def _make_block(self, node):
        buf = []
        buf.append("({")
        buf.extend([self.visit(child) for child in node.body])
        buf.append("})")
        return "\n".join(buf)

    def visit_If(self, node, use_parens=True):
        buf = []
        # if True: s1; s2  should be transpiled into ({s1; s2;})
        # such that the value of the expression is s2
        # This is a idiom used by rewriters to transform a single ast Node s0
        # into multiple statements s1, s2
        make_block = (
            isinstance(node.test, ast.Constant)
            and node.test.value == True
            and node.orelse == []
        )
        if make_block:
            return self._make_block(node)
        else:
            if use_parens:
                buf.append("if({0}) {{".format(self.visit(node.test)))
            else:
                buf.append("if {0} {{".format(self.visit(node.test)))
        buf.extend([self.visit(child) for child in node.body])

        orelse = [self.visit(child) for child in node.orelse]
        if orelse:
            buf.append("} else {")
            buf.extend(orelse)
            buf.append("}")
        else:
            buf.append("}")
        return "\n".join(buf)

    def visit_Continue(self, node):
        return "continue;"

    def visit_Break(self, node):
        return "break;"

    def visit_While(self, node, use_parens=True):
        buf = []
        if use_parens:
            buf.append("while ({0}) {{".format(self.visit(node.test)))
        else:
            buf.append("while {0} {{".format(self.visit(node.test)))
        buf.extend([self.visit(n) for n in node.body])
        buf.append("}")
        return "\n".join(buf)

    def visit_Compare(self, node):
        if isinstance(node.ops[0], ast.In):
            return self.visit_In(node)

        left = self.visit(node.left)
        op = self.visit(node.ops[0])
        right = self.visit(node.comparators[0])

        return "{0} {1} {2}".format(left, op, right)

    def visit_BoolOp(self, node):
        op = self.visit(node.op)
        return op.join([self.visit(v) for v in node.values])

    def visit_UnaryOp(self, node):
        return "{0}({1})".format(self.visit(node.op), self.visit(node.operand))

    def _visit_AssignOne(self, node, target) -> str:
        ...

    def visit_Assign(self, node):
        return "\n".join(
            [self._visit_AssignOne(node, target) for target in node.targets]
        )

    def visit_AugAssign(self, node):
        target = self.visit(node.target)
        op = self.visit(node.op)
        val = self.visit(node.value)
        return "{0} {1}= {2};".format(target, op, val)

    def visit_AnnAssign(self, node):
        target = self.visit(node.target)
        if (
            isinstance(node.target.annotation, ast.Subscript)
            and get_id(node.target.annotation.value) == "Callable"
        ):
            type_str = self._default_type
        else:
            type_str = self._typename_from_annotation(node)
        val = self.visit(node.value) if node.value is not None else None
        return (target, type_str, val)

    def visit_Delete(self, node):
        raise NotImplementedError("del not implemented")

    def visit_ClassDef(self, node):
        bases = [get_id(base) for base in node.bases]
        if set(bases) == {"Enum", "str"}:
            return self.visit_StrEnum(node)
        if len(bases) != 1:
            return None
        if not bases[0] in {"IntEnum", "IntFlag"}:
            return None
        if bases == ["IntEnum"]:
            return self.visit_IntEnum(node)
        if bases == ["IntFlag"]:
            return self.visit_IntFlag(node)

    def visit_StrEnum(self, node):
        raise Exception("Unimplemented")

    def visit_IntEnum(self, node):
        raise Exception("Unimplemented")

    def visit_IntFlag(self, node):
        raise Exception("Unimplemented")

    def visit_IfExp(self, node):
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        test = self.visit(node.test)
        return f"({test}? ({{ {body}; }}) : ({{ {orelse}; }}))"
