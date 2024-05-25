from type.interpreter_type import InterpreterType
from exceptions import StatementError,MissingParenthesisError
from icecream import ic

class StatementManager:
    def __init__(self, interpreter: InterpreterType) -> None:
        self.interpreter = interpreter

    def handle_if(self, command: str):
        condition = self.interpreter.parser.parse_condition(command)
        self.interpreter.if_condition = self.interpreter.parser.safe_eval(
            condition, self.interpreter.get_vars()
        )
        if not self.interpreter.if_condition:
            self.skip_to_else_or_end()

    def handle_else(self, command: str):
        if self.interpreter.if_condition is None:
            self.interpreter.raise_error(
                StatementError, "Missing 'if' statement before 'else'."
            )
        if self.interpreter.if_condition:
            self.skip_to_else_or_end()

    def find_block(self, index):
        open_braces = 0
        block_start = None

        while index < len(self.interpreter.code):
            line = self.interpreter.code[index].strip()
            for char in line:
                if char == "{":
                    if open_braces == 0:
                        block_start = index
                    open_braces += 1
                elif char == "}":
                    open_braces -= 1
                    if open_braces == 0:
                        block_end = index
                        return block_start, block_end

            index += 1
        

    def handle_while(self, command, i):
        condition = self.interpreter.parser.safe_eval(
            self.interpreter.parser.parse_condition(command), self.interpreter.get_vars()
        )
        index = i
        self.interpreter.nested_levels += 1
        block_start,block_end = self.find_block(index)
    
        while condition:
            inner_index = block_start + 1
            while inner_index < block_end:
             
                inner_command = self.interpreter.code[inner_index].strip()
                self.interpreter.interpret_command(inner_command, inner_index,True)
                inner_index += 1

            condition = self.interpreter.parser.safe_eval(
                self.interpreter.parser.parse_condition(command), self.interpreter.get_vars()
            )

        for i in range(block_start, block_end + 1):
            self.interpreter.lines_to_skip.add(i)
        self.interpreter.nested_levels -= 1

    def handle_for(self, command, i):
        args = self.interpreter.parser.parse_condition(command).strip()
        var_init, condition, increment = args.split(";")
        var_name = self.interpreter.var_check.check(var_init)
        increment = self.interpreter.context_manager.var_manager.parse_value("int", increment)
        index = i

        self.interpreter.nested_levels += 1
        block_start,block_end = self.find_block(index + 1)

        if not self.interpreter.parser.safe_eval(
            condition.strip(), self.interpreter.context_manager.get_vars()
        ):
            self.skip_to_else_or_end()
        while self.interpreter.parser.safe_eval(condition, self.interpreter.context_manager.get_vars()):
            inner_index = block_start + 1
            while inner_index < block_end:
                inner_command = self.interpreter.code[inner_index].strip()
                self.interpreter.interpret_command(inner_command, inner_index)
                inner_index += 1
            vars = self.interpreter.context_manager.get_vars()
            loop_var = vars[var_name] + increment
            self.interpreter.context_manager.set_var(
                var_name,loop_var
            )

        self.skip_to_else_or_end()

    def skip_to_else_or_end(self):
        stack = []
        for i in range(self.interpreter.line_count, len(self.interpreter.code)):
            line = self.interpreter.code[i].strip()
            if line.startswith("else") and not stack:
                self.interpreter.line_count = i
                return
            for char in line:
                if char == "{":
                    stack.append("{")
                elif char == "}":
                    if stack:
                        stack.pop()
                    else:
                        self.interpreter.raise_error(
                            MissingParenthesisError,
                            "Unmatched '}' in statement",
                            line,
                            line=i + 1,
                            tokens=line,
                        )

            if not stack:
                self.interpreter.skip_to = i
                break

        if stack:
            self.interpreter.raise_error(
                MissingParenthesisError,
                "Missing '}' in statement",
                line,
                line_number=i + 1,
                tokens=line,
            )
