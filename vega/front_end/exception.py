"""Vega compiler exceptions"""


class BaseError(Exception):
    """Base class for exceptions in this module"""

    def __init__(self, line, message) -> None:
        self.line: int = line
        self.message: str = message
        super().__init__()


class VegaSyntaxError(BaseError):
    """Syntax Error"""

    def __init__(self, token, next_token, line) -> None:
        super().__init__(line, message=f'Invalid Syntax between {token} and '
                                       f'{next_token} in line {line}.')


class VegaIdentifierBaseError(BaseError):
    """Variable definiton base error"""

    def __init__(self, line, message, identifier) -> None:
        self.identifier = identifier
        super().__init__(line, message)


class VegaAlreadyDefinedError(VegaIdentifierBaseError):
    """Variable definition error"""

    def __init__(self, identifier, line) -> None:
        message = f'Identifier {identifier} at line {line} already defined'
        super().__init__(line, message, identifier)


class VegaNotYetDefinedError(VegaIdentifierBaseError):
    """Variable definition error"""

    def __init__(self, identifier, line) -> None:
        message = f'Identifier {identifier} at line {line} not defined'
        super().__init__(line, message, identifier)


class VegaNoCallableError(VegaIdentifierBaseError):
    """Identifier no callable"""

    def __init__(self, identifier, line) -> None:
        message = f'Identifier {identifier} at line {line} can not be called'
        super().__init__(line, message, identifier)


class VegaNotAssignError(VegaIdentifierBaseError):
    """Identifier cannot be used for assignment"""

    def __init__(self, identifier, line) -> None:
        message = f'Identifier {identifier} at line {line} cannot used for ' \
                  f'assignment'
        super().__init__(line, message, identifier)
