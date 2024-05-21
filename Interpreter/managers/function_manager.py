
from built_in.builtin import built_in
from type.interpreter_type import InterpreterType
from exceptions import FunctionError

class FunctionManager:
    def __init__(self, interpreter: InterpreterType):
        self.interpreter = interpreter
        self.builtin = built_in

        self.translation_table = str.maketrans("", "", "()")


    def find_function(self, command: str):   
        tokens = command.split()    
        function = self._find_builtin(tokens[0])
        if function is not None: 
            function.activate()
    def get_function(self, command: str,not_exists_ok = False,call = True):
        function = self._find_builtin(command)
        if function is None and not not_exists_ok:
            self.interpreter.raise_error(FunctionError, f"Function not found - {command}", command)
        if function is not None and call:
            func_return = function.activate()
            return func_return
        if function:
            return True
    def _find_builtin(self, command):
        tokens = command.split()
        for function in self.builtin:
            for token in tokens:
                func_class = function(self.interpreter,command)
                if func_class.key_word in token:
                    
                    return func_class
        return None
    