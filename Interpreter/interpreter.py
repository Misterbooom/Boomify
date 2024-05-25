import argparse  # noqa: F401
from utils import (
    OperationManager,
    VariableManager,
    Parser,
    FunctionManager,
    StatementManager
)
from exceptions import ParsingError, CustomException,BoomError
import sys
from built_in.base_function import BaseFunction
from icecream import ic

sys.set_int_max_str_digits(0)

class Interpreter:
    def __init__(self, debug_mode=False, code:list=None):
        self.RESERVED_KEYWORDS = {"var", "explode", "ignite", "if", "else",'while','for','func'}
        self.OPERATORS = {"=", "+=", "-=", "*=", "/=", "%=", "+", "-", "*", "/", "%"}
        self.valid_commands = ["explode", "ignite"]
        self.operators = ['=',"+=", "-=", "*=", "/=", "%="]
        self.arithmetic_operators = ["+", "-", "*", "/", "%"]
        self.debug_mode = debug_mode
        self.logs = {}
        self.context_manager = ContextManager(self)
        self.op_manager = OperationManager(self)
        self.func_manager = FunctionManager(self)
        self.var_check = CheckVariables(self)
        self.parser = Parser(self.operators, self)
        self.statement_manager = StatementManager(self)
        self.line_count = 0
        self.code = code
        self.statement_line = None
        self.lines_to_skip = set()
        
        self.if_condition = None
        self.else_line = None  
        self.command = None
        self.skip_to = None
        self.nested_levels = 0
        self.context = "global"
    def interpret_code(self):
        i = 0
        while i < len(self.code):

            if  self.skip_to is not None:
                i = self.skip_to
                self.skip_to = None
            command = self.code[i]
            self.interpret_command(command, i) 
            i += 1

    def interpret_command(self, command: str, i, context = None):
        if context is not None :
            self.context = context

        self.line_count = i
        if command.startswith('!!'):
            return
        if self.debug_mode:                                            
            for name, log in self.logs.items():
                print(f"{name}: {log}")

        if command == "" or len(command.split()) == 0:
            return


        self.logs.clear()

        self.tokens = command.split()
        self.command = command
        self.log("Tokens", self.tokens)
        self.log("Vars", self.context_manager.get_all_vars())
        self.log('Lines To skip ', self.lines_to_skip)
        function = self.func_manager.find_function(command)
        if self.tokens[0] != 'var'  and function:
            if function is not None: 
                if isinstance(function,BaseFunction):
                    function.activate(command)
                else:
                    function.activate()

            return

        # Check for if/else statements
        elif self.tokens[0].startswith("if"):
            self.statement_manager.handle_if(command)
            return
        elif self.tokens[0].startswith("else"):
            self.statement_manager.handle_else(command)
            return
        elif self.tokens[0].startswith("while"):
            self.statement_manager.handle_while(command, i)
            return
        elif self.tokens[0].startswith("for"):
            self.statement_manager.handle_for(command, i)
            return
        elif self.tokens[0].startswith("func"):
            self.func_manager.define_function(command, i)
            return
        self.var_check.check(command) 



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
    def get_vars(self):
        self.context_manager
    def raise_error(
        self, error: CustomException, message, error_token=None, line=None, tokens=None
    ):
        exception = error(
            message,
            self.line_count if not line else line,
            self.command if not tokens else tokens,
            error_token,
        )
        
        print(exception)
        raise Exception
        exit()
class ContextManager:
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.var_manager = VariableManager(self.interpreter)
    def get_globals(self):
        return self.var_manager.global_vars
    def get_locals(self):
        
        return self.var_manager.locals_vars[self.interpreter.context]
    def set_var(self, var_name, var_value):
        self.var_manager.variable_assignment(var_name, f"{var_value}", self.interpreter.context)
    def get_vars(self):
        if self.interpreter.context != 'global':
            return self.var_manager.locals_vars.get(self.interpreter.context,None)
        else:
            return self.var_manager.global_vars
    def get_all_vars(self):
        return {'globals':self.var_manager.global_vars,'locals':self.var_manager.locals_vars}
class CheckVariables:
    def __init__(self, interpreter: Interpreter, ):
        self.interpreter = interpreter
        self.var_manager = self.interpreter.context_manager.var_manager

    def check(self, command: str):
        command = command
        tokens = command.split()
        var_name, operator, var_value = self.interpreter.parser.find_var(
            command.replace("var", "")
        )
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
                    result = self.interpreter.op_manager.arithmetic_operation(var_value,self.interpreter.context_manager.get_vars())
                    var_value = self.var_manager.variable_assignment(
                        var_name, f"{result}", self.interpreter.context
                    )
                    
                else:
                    self.var_manager.variable_assignment(
                        var_name, var_value, self.interpreter.context
                    )
        elif operator in self.interpreter.operators:
            try:
                result = self.interpreter.op_manager.perform_operation(
                    var_name, var_value, operator,self.interpreter.context_manager.get_vars()
                )
                self.var_manager.variable_assignment(var_name, f"{result}",self.interpreter.context)

                self.interpreter.log(
                    var_name, f"Updated {var_name} using {operator} to {result}"
                )
            except KeyError:
                self.interpreter.raise_error(
                    ParsingError, f"Variable - {var_name} not defined", ' ' + var_name
                )
        return var_name

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
