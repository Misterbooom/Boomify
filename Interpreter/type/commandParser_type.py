import ast
import operator

# Define supported operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


class SafeEval(ast.NodeVisitor):
    def __init__(self, local_vars):
        self.local_vars = local_vars

    def visit(self, node):
        try:
            if isinstance(node, ast.Expression):
                return self.visit(node.body)
            elif isinstance(node, ast.BinOp):
                left = self.visit(node.left)
                right = self.visit(node.right)
                return operators[type(node.op)](left, right)
            elif isinstance(node, ast.Constant):  # Handles all constants in Python 3.8+
                return node.value
            elif isinstance(node, ast.Name):
                if node.id in self.local_vars:
                    return self.local_vars[node.id]
                else:
                    raise ValueError(f"Variable '{node.id}' is not defined")
            elif isinstance(node, ast.Tuple):
                return tuple(self.visit(element) for element in node.elts)
            elif isinstance(node, ast.List):
                return [self.visit(element) for element in node.elts]
            else:
                raise ValueError(f"Unsupported type: {type(node).__name__}")
        except TypeError as e:
            raise ValueError(f"Type error: {e}")
        except Exception as e:
            raise ValueError(f"Error: {e}")


class Parser:
    def __init__(self, operators: list[str], interpreter= None):
        # Sort operators by length in descending order to match longest operators first
        self.operators = sorted(operators, key=len, reverse=True)
        self.interpreter = interpreter

    def find_var(self, command: str):
        ...
    def get_args(self, tokens: list[str], keyword: str):
        ...

    def safe_eval(self, expression: str, local_vars: dict):
        ...


if __name__ == "__main__":
    parser = Parser(["+=", "-=", "*=", "/=", "%="])
