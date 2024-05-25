
from exceptions import OperationError
from type.interpreter_type import InterpreterType


class OperationManager:
    def __init__(self, interpreter: InterpreterType):
        self.interpreter = interpreter

    def arithmetic_operation(self, expression, vars):
        try:
            result = self.interpreter.parser.safe_eval(expression, vars)
        except SyntaxError as e:
            error_location = str(expression[e.offset - 1])
            self.interpreter.raise_error(OperationError, f"Error in expression at {error_location}.",error_location)

        return result

    def perform_operation(self, var_name, var_value, operator, vars):
        current_value = vars[var_name]
        operation_value = self.arithmetic_operation(var_value,vars)
        if operator == "+=":
            result = current_value + operation_value
        elif operator == "-=":
            result = current_value - operation_value
        elif operator == "*=":
            result = current_value * operation_value
        elif operator == "/=":
            result = current_value / operation_value
        elif operator == "%=":
            result = current_value % operation_value
        else:
            self.interpreter.raise_error(OperationError, "Invalid operator", operator)
        self.interpreter.log(
            "Arithmetic Operation",
            f"{operator} operation: {var_name} updated to {result}",
        )
        return result
