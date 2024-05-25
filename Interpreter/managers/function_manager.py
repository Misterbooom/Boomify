
from built_in.builtin import built_in
from type.interpreter_type import InterpreterType
from exceptions import FunctionError,MissingParenthesisError  # noqa: F403
from built_in.base_function import BaseFunction,BaseBuiltinFunction
class FunctionManager:
    def __init__(self, interpreter: InterpreterType):
        self.interpreter = interpreter
        self.builtin = built_in
        self.functions = []
        self.translation_table = str.maketrans("", "", "()")


    def find_function(self, command: str):   
        function = self._find_builtin(command.strip())
        if function is None:
            function = self._find_function(command.strip())
        return function
    def get_function(self, command: str,not_exists_ok = False,call = True):
        function = self._find_builtin(command)
        if function is None:
            function = self._find_function(command)
        if function is None and not not_exists_ok:
            self.interpreter.raise_error(FunctionError, f"Function not found - {command}", command)  # noqa: F405
        if function is not None and call:
            if isinstance(function,BaseFunction):
                func_return = function.activate(command)
            else:
                func_return = function.activate()
            return func_return
        if function:
            return True
    def _find_builtin(self, command):
        tokens = command.split()
        for function in self.builtin:
            function:BaseBuiltinFunction
            for token in tokens:
                func_class = function(self.interpreter,command)
                if token.startswith(func_class.key_word):
                    
                    return func_class
        return None
    def _find_function(self, command):
        tokens = command.split()
        for function in self.functions:
            function: BaseFunction
            for token in tokens:
                if token.startswith(function.key_word):
                    return function
        return None

    def define_function(self, command:str,index):
        # function = BaseFunction(self.interpreter,command)
        block_start, block_end = self.interpreter.statement_manager.find_block(index)         
        self.interpreter.statement_manager.skip_to_else_or_end()
        body = self.interpreter.code[block_start + 1:block_end]
        name = command.replace('func','')
        name = name[:name.index('(')].strip()
        args = command[command.index('(')+1:command.index(')')].split(',')
        function = BaseFunction(self.interpreter,command,name,body = body,args = args,command_index = index)
        self.functions.append(function)
        # function = BaseFunction(self.interpreter,command,)