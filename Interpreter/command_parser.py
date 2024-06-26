from exceptions import ParsingError, VariableError,BoomError,MissingParenthesisError
from type.interpreter_type import InterpreterType
import ast
import operator
from icecream import ic  # noqa: F401
# Define supported operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.And: operator.and_,
    ast.Or: operator.or_,
    ast.Gt: operator.gt,
    ast.Lt: operator.lt,
    ast.GtE: operator.ge,
    ast.LtE: operator.le,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.USub: operator.neg,  # Unary subtraction (negation)
    ast.UAdd: operator.pos,  # Unary addition (positive sign)
    ast.Pow: operator.pow
}

class SafeEval(ast.NodeVisitor):
    def __init__(self, local_vars):
        self.local_vars = local_vars

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            return operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            return operators[type(node.op)](operand)
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            if node.id in self.local_vars:
                return self.local_vars[node.id]
            else:
                raise ValueError(f"Variable '{node.id}' is not defined")
        elif isinstance(node, ast.IfExp):
            test = self.visit(node.test)
            body = self.visit(node.body)
            orelse = self.visit(node.orelse)
            return body if test else orelse
        elif isinstance(node, ast.Compare):
            left = self.visit(node.left)
            right = self.visit(node.comparators[0])
            op = node.ops[0]
            return operators[type(op)](left, right)
        elif isinstance(node, ast.BoolOp):
            op_type = type(node.op)
            if op_type == ast.And:
                return all(self.visit(val) for val in node.values)
            elif op_type == ast.Or:
                return any(self.visit(val) for val in node.values)
            else:
                raise ValueError(f"Unsupported boolean operator: {op_type}")
        elif isinstance(node, ast.Assign):
            target = node.targets[0].id
            value = self.visit(node.value)
            self.local_vars[target] = value
            return value
        elif isinstance(node, ast.Pow):
            return operators[type(node.op)](self.visit(node.left), self.visit(node.right))
        elif isinstance(node, ast.Tuple):
            return tuple(self.visit(element) for element in node.elts)
        elif isinstance(node, ast.List):
            return [self.visit(element) for element in node.elts]
        else:
            raise ValueError(f"Unsupported type: {type(node).__name__}")



class Parser:
    def __init__(self, operators: list[str], interpreter: InterpreterType = None):
        # Sort operators by length in descending order to match longest operators first
        self.operators = sorted(operators, key=len, reverse=True)
        self.interpreter = interpreter
        self.var_manager = self.interpreter.context_manager.var_manager
    def find_var(self, command: str):
        for op in self.operators:
            if op in command:
                parts = command.split(op)
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    var_value = parts[1].strip()
                    if " " in var_name:
                        self.interpreter.raise_error(
                            VariableError, f"Variable names cannot contain spaces - {var_name}", var_name[-1]
                        )
                    return var_name, op, var_value
                else:
                    self.interpreter.raise_error(ParsingError, f"Invalid Operator - {op}",op)
        return None,None,None
        # self.interpreter.raise_error(ParsingError, f"Operator Not Found - '{op}' ",op)

    def get_args(self, command: str, keyword: str, normalize = True):
        tokens = command.split()
        func_index = None
        for i, token in enumerate(tokens):
            if keyword in token:
                func_index = i
                break
        if func_index is None:
            return ["None"]

        func_token = " ".join(tokens[func_index:])
        
        args_start = func_token.find("(") + 1 
        args_end = func_token.rfind(")")
        if args_start is None and args_end is None:
            return []

        if args_start == -1:
            self.interpreter.raise_error(
                MissingParenthesisError, "Missing '(' in arguments", command
            )
        elif args_end == -1:
            self.interpreter.raise_error(                     
                MissingParenthesisError, "Missing ')' in arguments", command
            )
        args_str = func_token[args_start:args_end]
        args = args_str.split(",")
        normalized_args = []
        if not normalize:
            return args
        for arg in args: 
            arg_type = self.interpreter.context_manager.var_manager.check_var_type(arg.strip())
            if arg_type == "function":
                func_return = self.interpreter.func_manager.get_function(arg.strip(),self.interpreter.line_count)
                normalized_args.append(func_return)
            else:
                if arg_type is None and arg.strip() :  # Check if the argument is not empty
                    arg_value = self.safe_eval(arg.strip(), self.interpreter.context_manager.get_vars())
                else:
                    arg_value = self.interpreter.context_manager.var_manager.parse_value(arg_type,arg.strip())
                normalized_args.append(arg_value)
        return normalized_args

    def parse_condition(self,command:str):
        condition_start = command.find("(")
        condition_end = command.find(")", condition_start)

        if condition_start == -1:
            self.interpreter.raise_error(
                MissingParenthesisError, "Missing '(' in condition", command
            )
        elif condition_end == -1:
            self.interpreter.raise_error(
                MissingParenthesisError, "Missing ')' in condition",command
            )

        condition = command[condition_start + 1 : condition_end]
        return condition

    def safe_eval(self, expression: str, local_vars: dict):
        
        try:
            tree = ast.parse(expression.strip(), mode="eval")
            return SafeEval(local_vars).visit(tree.body)
        except SyntaxError as e:

            self.interpreter.raise_error(
                BoomError,
                f"Error in expression at '{str(expression[e.offset - 1])}'.",	
                str(expression[e.offset - 1]) if e.offset is not None else expression,
            )
        except TypeError as e:
            self.interpreter.raise_error(
                ParsingError,
                str(e),
                expression,
            )
        except Exception as e:
            self.interpreter.raise_error(
                BoomError,
                str(e).replace('Error:',''),	
                expression,
            )


if __name__ == "__main__":
    
    parser = Parser(["+=", "-=", "*=", "/=", "%="])

