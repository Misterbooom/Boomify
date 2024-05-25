from type.interpreter_type import InterpreterType
from exceptions import ParsingError,RecursionDepthError
from utils import VariableManager
from icecream import ic
class BaseBuiltinFunction:
    def __init__(
        self,
        interpreter: InterpreterType,
        command: str,
        key_word: str,
        num_args: int = float("inf"),
        arg_required: bool = True,
        func_return: any = None,
    ):
        self.interpreter = interpreter
        self.key_word = key_word
        self.num_args = num_args
        self.arg_required = arg_required
        self.command = command
        self.func_return = func_return
        self.func_name = f"<BuiltInFunction-{self.key_word}>"
    def activate(self,exec = True):
        args = self.interpreter.parser.get_args(self.command, self.key_word)
        self.interpreter.log(self.key_word, {"args": args})
        if not args and self.arg_required:
            self.interpreter.raise_error(
                ParsingError,
                f"Invalid number of arguments - {0}",
                self.key_word,
            )
        if len(args) > self.num_args:
            self.interpreter.raise_error(
                ParsingError,
                f"Invalid number of arguments - {len(args)}, expected - {self.num_args}, Arguments - {args}",
                self.key_word,
            )
        if exec:
            self.execute(args)
        return self.func_name if not self.func_return else self.func_return

    def execute(self, args):
        raise NotImplementedError("Subclasses must implement this method")
    

class BaseFunction:
    def __init__(
        self,
        interpreter: InterpreterType,
        command: str,
        key_word: str,
        num_args: int = float("inf"),
        body: list = [],
        arg_required: bool = True,
        args:list = [],
        command_index = 0
    ):
        self.interpreter = interpreter
        self.key_word = key_word
        self.num_args = num_args
        self.arg_required = arg_required
        self.command = command
        self.command_index = command_index
        self.body = body
        self.args = args
        self.func_return = None
        self.func_name = f"<Function-{self.key_word}>"
    def activate(self,command):
        args = self.interpreter.parser.get_args(command, self.key_word)
        self.interpreter.context = self.key_word
        for i,arg in enumerate(args):
            self.interpreter.context_manager.set_var(self.args[i],arg)
        self.interpreter.log(self.key_word, {"args": args})
        if not args and self.arg_required:
            self.interpreter.raise_error(
                ParsingError,
                f"Invalid number of arguments - {0}",
                self.key_word,
            )
        if len(args) > self.num_args:
            self.interpreter.raise_error(
                ParsingError,
                f"Invalid number of arguments - {len(args)} expected - {self.num_args}",
                args,
            )
        self.execute(self.command_index)
        return self.func_name if not self.func_return else self.func_return

    def execute(self,index): 
        for i,line in enumerate(self.body,start = index):
            
            try:

                if 'return' in line:
                    args = self.interpreter.parser.get_args(line, 'return')
                    self.func_return = tuple(args) if len(args) > 0 else args[0]
                    break
                self.interpreter.interpret_command(line,i)
            except RecursionError :
                self.interpreter.raise_error(RecursionDepthError,'max recursion depth exceeded',line)
        
        self.interpreter.context = 'global'
        self.interpreter.line_count = index
        self.interpreter.statement_manager.skip_to_else_or_end()
    
