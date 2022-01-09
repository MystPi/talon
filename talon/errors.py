class VMError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SymbolNotFound(VMError):
    pass


class SymbolExists(VMError):
    pass


class FunctionNotFound(VMError):
    pass


class FunctionExists(VMError):
    pass


class WrongParamCount(VMError):
    pass