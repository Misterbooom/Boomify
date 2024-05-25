from type.interpreter_type import InterpreterType
from built_in.base_function import BaseBuiltinFunction


class Ignite(BaseBuiltinFunction):
    def __init__(self, interpreter: InterpreterType, command: str):
        super().__init__(interpreter, command, key_word="ignite", func_return=None,num_args=1)

    def execute(self, args):
        user_input = input(f"{args[0]}")
        self.func_return = f"'{user_input}'"
        
