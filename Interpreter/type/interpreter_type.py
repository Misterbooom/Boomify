from type.variableManager_type import VariableManager
from type.operationManager_type import OperationManager
from type.commandParser_type import Parser
from exceptions import CustomException
class InterpreterType:
    def __init__(self, debug_mode=False, code:list[str]=None):
        self.RESERVED_KEYWORDS = {"var", "explode", "ignite", "if", "else"}
        self.OPERATORS = {"=", "+=", "-=", "*=", "/=", "%=", "+", "-", "*", "/", "%"}
        self.valid_commands = ["explode", "ignite"]
        self.operators = ["=", "+=", "-=", "*=", "/=", "%="]
        self.arithmetic_operators = ["+", "-", "*", "/", "%"]
        self.debug_mode = debug_mode
        self.logs = {}
        self.var_manager = VariableManager(self)
        self.op_manager = OperationManager(self)
        self.parser = Parser(self.operators, self)
        self.line_count = 0
        self.code = code
        self.statement_line = None
        self.lines_to_skip = set()
        self.if_condition = None
        self.else_line = None  # Track the line number of 'else'
        self.command = None
        self.var_check = CheckVariables(self)
        self.nested_levels = 0
        self.restart_index = None
        self.start_index = None

    def interpret_command(self, command: str, i, ignore_skip = False,var_manager = None):

        self.line_count += 1
        self.logs.clear()
        self.tokens = command.split()
        self.log("Tokens", self.tokens)
        self.func_manager.find_function(self.tokens)
        # self.var_check.check(self.tokens)
        if self.debug_mode:
            for type, log in self.logs.items():
                print(f"{type}: {log}")

    def log(self, name, message):
        self.logs.setdefault(name, [])
        self.logs[name].append(message)

    def raise_error(
        self, error: CustomException, message, error_token=None, line=None, tokens=None
    ):
        exception = error(message, self.line_count, self.tokens, error_token)
        print(exception)
        exit()
    def get_vars(self, var_name = None):
        if var_name in self.global_var_manager.vars:
            return self.global_var_manager.vars[var_name]
        
        return self.global_var_manager.vars

class CheckVariables:
    def __init__(self, interpreter: InterpreterType):
        self.interpreter = interpreter

    def check(self, command: str):
        pass
