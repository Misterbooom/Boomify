from type.interpreter_type import InterpreterType
from built_in.base_function import BaseBuiltinFunction
class Explode(BaseBuiltinFunction):
    def __init__(self, interpreter: InterpreterType, command: str):
        super().__init__(interpreter, command, key_word="explode", func_return=None)

    def execute(self, args):
        str_args = " ".join(str(arg) for arg in args)
        print(str_args) 