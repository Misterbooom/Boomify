from type.interpreter_type import InterpreterType
from exceptions import ParsingError
class StatementManager:
    def __init__(self,interpreter:InterpreterType) -> None:
        self.interpreter = interpreter
    def handle_if(self, command: str):
        condition = self.interpreter.parser.parse_condition(command)
        self.if_condition = self.interpreter.parser.safe_eval(
            condition, self.interpreter.var_manager.vars
        )
        if not self.if_condition:
            self.skip_to_else_or_end()
    def handle_else(self,command: str):
        if self.if_condition is None:
            self.interpreter.raise_error(
                ParsingError, "Unexpected else without matching if"
            )
        if self.if_condition:
            self.skip_to_end_of_block(self.interpreter.code.index(command))
    def handle_while(self, command: str, i):
        print("Handle While")
        condition = self.interpreter.parser.safe_eval(self.interpreter.parser.parse_condition(command),self.interpreter.var_manager.vars)
        index = i + 1
        start_index = index
        block_lines = []
        while condition:
            if index not in block_lines:
                block_lines.append(index)
            while_command = self.interpreter.code[index]

            if while_command == "end":
                index = start_index - 1
                condition = self.interpreter.parser.parse_condition(command)  
            else:
                
                index += 1
            
            self.interpreter.interpret_command(while_command, index)

            condition = self.interpreter.parser.safe_eval(
                self.interpreter.parser.parse_condition(command),
                self.interpreter.var_manager.vars,
            )
            print(condition)
        for i in block_lines:
            self.interpreter.lines_to_skip.append(i)
    def skip_to_else_or_end(self):
        for i in range(self.interpreter.line_count, len(self.interpreter.code)):
            line = self.interpreter.code[i].strip()
            self.interpreter.lines_to_skip.append(i)
            
            if line.startswith("else"):
                self.line_count = i  # Point to 'else' for the next command
                return
            elif line == "end":
                self.line_count = i  # Point to 'end' for the next command
                return
        self.interpreter.raise_error(
            ParsingError, "Missing else or end for if statement", line
        )

    def skip_to_end_of_block(self, line_count=0):
        for i, line in enumerate(self.interpreter.code[line_count::], start=line_count):
            line = self.interpreter.code[i].strip()
            self.interpreter.lines_to_skip.append(i - 1)

            if line == "end":

                self.line_count = i  # Point to 'end' for the next command
                return
        self.interpreter.raise_error(ParsingError, "Missing end for else statement",line)