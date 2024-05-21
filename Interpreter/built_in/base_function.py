from type.interpreter_type import InterpreterType
from exceptions import ParsingError

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
                f"Invalid number of arguments - {len(args)} expected - {self.num_args}",
                args,
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
        arg_required: bool = True,
    ):
        self.interpreter = interpreter
        self.key_word = key_word
        self.num_args = num_args
        self.arg_required = arg_required
        self.command = command

    def activate(self):
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
                f"Invalid number of arguments - {len(args)} expected - {self.num_args}",
                args,
            )
        self.execute(args)

    def execute(self, args):
        raise NotImplementedError("Subclasses must implement this method")
    
    def func_return(self, args):
        return args