from type.interpreter_type import InterpreterType
from built_in.base_function import BaseBuiltinFunction


class Parse(BaseBuiltinFunction):
    def __init__(self, interpreter: InterpreterType, command: str):
        super().__init__(
            interpreter, command, key_word="parse", func_return=None, num_args=3
        )

    def execute(self, args):
        value = self.interpreter.parser.safe_eval(args[0].strip(),self.interpreter.get_vars())
        type = args[1]
        
        self.func_return = self.interpreter.var_manager.parse_value(type, value.strip())
