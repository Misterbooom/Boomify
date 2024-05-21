class CustomException:
    def __init__(
        self,
        message: str,
        line_count=None,
        command: list[str] = None,
        error_token: str = None,
    ):
        self.message = message
        self.line_count = line_count
        self.error_token = error_token
        self.command = command

    def find_error_token_index(self):
        if self.error_token is None or self.command is None:
            return None
        error_index = self.command.find(self.error_token)
        return error_index

    def highlight_error_token(self):
        error_index = self.find_error_token_index()
        if error_index != -1:
            token_pos = error_index
            highlighted_token = (
                self.command[:token_pos]
                + f"\033[91m{self.error_token}\033[0m"
                + self.command[token_pos + len(self.error_token) :]
            )
            caret_line = " " * token_pos + "^" * len(self.error_token)
            return highlighted_token + "\n" + caret_line
        return self.command

    def __str__(self):
        if self.error_token:
            highlighted_command = self.highlight_error_token()
        else:
            highlighted_command = self.command
        line_info = f" (Line: {self.line_count})" if self.line_count else ""
        return (
            f"{type(self).__name__}: {self.message}{line_info}\n{highlighted_command}"
        )


class ParsingError(CustomException):
    def __init__(self, message, line_count=None, tokens=None, error_token=None):
        super().__init__(message, line_count, tokens, error_token)

    def __str__(self):
        return super().__str__()


class VariableError(CustomException):
    def __init__(self, message, line_count=None, tokens=None, error_token=None):
        super().__init__(message, line_count, tokens, error_token)

    def __str__(self):
        return super().__str__()


class OperationError(CustomException):
    def __init__(self, message, line_count=None, tokens=None, error_token=None):
        super().__init__(message, line_count, tokens, error_token)

    def __str__(self):
        return super().__str__()
class BoomError(CustomException):
    def __init__(self, message, line_count=None, tokens=None, error_token=None):
        super().__init__(message, line_count, tokens, error_token)

    def __str__(self):
        return super().__str__()
class FunctionError(CustomException):
    def __init__(self, message, line_count=None, tokens=None, error_token=None):
        super().__init__(message, line_count, tokens, error_token)

    def __str__(self):
        return super().__str__()
class TypeError(CustomException):
    def __init__(self, message, line_count=None, tokens=None, error_token=None):
        super().__init__(message, line_count, tokens, error_token)

    def __str__(self):
        return super().__str__()


# Example usage
if __name__ == "__main__":
    print(
        VariableError(
            "Invalid variable name",
            line_count=1,
            tokens=["explode(", "1", "+", "2)"],
            error_token="te",
        )
    )
