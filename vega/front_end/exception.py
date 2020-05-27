"""Vega compiler exceptions"""


class BaseError(Exception):
    """Base class for exceptions in this module"""


class VegaSyntaxError(BaseError):
    """Syntax Error"""

    def __init__(self, token, line) -> None:
        self.token = token
        self.line = line
        self.message = f'Invalid Syntax at {self.token} in line {self.line}.'
        super().__init__()


class VegaIdentifierBaseError(BaseError):
    """Variable definiton base error"""

    def __init__(self, identifier, line) -> None:
        self.identifier = identifier
        self.line = line
        super().__init__()


class VegaAlreadyDefinedError(VegaIdentifierBaseError):
    """Variable definition error"""

    def __init__(self, identifier, line) -> None:
        self.message = f'Identifier {identifier} at line {self.line} ' \
                       f'already defined'
        super().__init__(identifier, line)


class VegaNotYetDefinedError(VegaIdentifierBaseError):
    """Variable definition error"""

    def __init__(self, identifier, line) -> None:
        self.message = f'Identifier {identifier} at line {self.line} ' \
                       f'not defined'
        super().__init__(identifier, line)


class VegaNoCallableError(VegaIdentifierBaseError):
    """Identifier no callable"""

    def __init__(self, identifier, line) -> None:
        self.message = f'Identifier {identifier} at line {self.line} ' \
                       f'can not be called'
        super().__init__(identifier, line)


class VegaNotAssignError(VegaIdentifierBaseError):
    """Identifier cannot be used for assignment"""

    def __init__(self, identifier, line) -> None:
        self.message = f'Identifier {identifier} at line {self.line} ' \
                       f'cannot used for assignment'
        super().__init__(identifier, line)
