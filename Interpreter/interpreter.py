import argparse  # noqa: F401
from utils import (
    OperationManager,
    VariableManager,
    Parser,
    FunctionManager,
    StatementManager
)
from exceptions import ParsingError, CustomException,BoomError
import traceback

class Interpreter:
    def __init__(self, debug_mode=False, code:list=None):
        self.RESERVED_KEYWORDS = {"var", "explode", "ignite", "if", "else",'while'}
        self.OPERATORS = {"=", "+=", "-=", "*=", "/=", "%=", "+", "-", "*", "/", "%"}
        self.valid_commands = ["explode", "ignite"]
        self.operators = ['=',"+=", "-=", "*=", "/=", "%="]
        self.arithmetic_operators = ["+", "-", "*", "/", "%"]
        self.debug_mode = debug_mode
        self.logs = {}
        self.var_manager = VariableManager(self)
        self.op_manager = OperationManager(self)
        self.func_manager = FunctionManager(self)
        self.var_check = CheckVariables(self)
        self.parser = Parser(self.operators, self)
        self.statement_manager = StatementManager(self)
        self.line_count = 0
        self.code = code
        self.statement_line = None
        self.lines_to_skip = []
        self.if_condition = None
        self.else_line = None  # Track the line number of 'else'
        self.command = None
        self.restart_index = None
        self.start_index = None
        
    def interpret_code(self):
        i = 0
        while i < len(self.code):

            command = self.code[i]
            if i == self.restart_index:
                i = self.start_index if self.start_index is not None else 0
            i += 1

            self.interpret_command(command, i)
            

            

    def interpret_command(self, command: str, i):
        self.line_count = i
        if self.line_count  in self.lines_to_skip:
            return
        if command == "" or len(command.split()) == 0:
            return


        self.logs.clear()

        self.tokens = command.split()
        self.command = command
        self.log("Tokens", self.tokens)
        self.log("Vars", self.var_manager.vars) 
        # Check if the command is a function
        if self.tokens[0] != 'var'  and self.func_manager.find_function(command):
            return

        # Check for if/else statements
        elif self.tokens[0] == "if":
            self.statement_manager.handle_if(command)
        elif self.tokens[0] == "else":
            self.statement_manager.handle_else(command)
        elif self.tokens[0] == 'while':
            self.statement_manager.handle_while(command,i)
        # Check for variable assignment or operation
        
        self.var_check.check(self.tokens)   

        if self.debug_mode:                                            
            for name, log in self.logs.items():
                print(f"{name}: {log}")

    def check_syntax(self, tokens, var_name, operator, var_value):
        if var_name in self.RESERVED_KEYWORDS:
            self.raise_error(
                BoomError, f"Invalid variable name '{var_name}'", var_name
            )


        if operator and operator not in self.OPERATORS:
            self.raise_error(
                BoomError, f"Invalid operator '{operator}'", operator
            )

   
    def log(self, name, message):
        self.logs.setdefault(name, [])
        self.logs[name].append(message)

    def raise_error(
        self, error: CustomException, message, error_token=None, line=None, tokens=None
    ):
        exception = error(
            message,
            self.line_count if not line else line,
            self.command if not tokens else tokens,
            error_token,
        )
        if self.debug_mode:
            traceback.print_exc()
        print(exception)
        exit()


class CheckVariables:
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter

    def check(self, tokens: list[str]):
        command = " ".join(tokens).replace('var','')
        var_name, operator, var_value = self.interpreter.parser.find_var(command)
        if not var_name or not operator or not var_value:
            return
        if tokens[0] == 'var':

            if not var_name or not operator or not var_value or self.interpreter.check_syntax(tokens, var_name, operator, var_value):
                return

            self.interpreter.log(
                "Parsed_Tokens",
                {"operator": operator, "var_name": var_name, "var_value": var_value},
            )
            check_operators = any(op in var_value for op in self.interpreter.arithmetic_operators)
            if operator == "=":
                if check_operators:
                    result = self.interpreter.op_manager.arithmetic_operation(var_value)
                    self.interpreter.var_manager.variable_assignment(var_name, f"{result}")
                    
                else:
                    self.interpreter.var_manager.variable_assignment(var_name, var_value)
        elif operator in self.interpreter.operators:
            try:
                result = self.interpreter.op_manager.perform_operation(
                    var_name, var_value, operator
                )
                self.interpreter.var_manager.vars[var_name] = result
                self.interpreter.log(
                    var_name, f"Updated {var_name} using {operator} to {result}"
                )
            except KeyError:
                self.interpreter.raise_error(
                    ParsingError, f"Variable - {var_name} not defined", ' ' + var_name
                )


def run_interpreter():
    while True:
        statement = input(">>> ")
        if statement == "exit":
            break
        if statement != "":
            interpreter.interpret_command(statement)


if __name__ == "__main__":
    with open("Interpreter/calculator.bify", "r") as f:
        content = f.readlines()
        interpreter = Interpreter(False, content)
        interpreter.interpret_code()
