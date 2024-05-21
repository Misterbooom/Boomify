from built_in.builtin import built_in


class FunctionManager:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.builtin = built_in

    def find_function(self, tokens: list[str]):
        function = self._find_builtin(tokens)
        if function is not None:
            function.activate(tokens)

    def get_function(self, command: str):
        pass

    def _find_builtin(self, tokens: list[str]):
        for function in self.builtin:
            for token in tokens:
                if function.key_word == token:
                    return function
        return None
