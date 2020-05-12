class Error(Exception):
    """Base class for exceptions in this module"""


class VegaSyntaxError(Error):
    """Syntax Error"""

    def __init__(self, token, line) -> None:
        self.token = token
        self.line = line
        self.message = f'Invalid Syntax at {self.token} in line {self.line}.'
        super().__init__()


class VegaAlreadyDefinedError(Error):
    """Variable definition error"""

    def __init__(self, identifier, line) -> None:
        self.identifier = identifier
        self.line = line
        self.message = f'Identifier {identifier} at line {self.line} ' \
                       f'already defined'
        super().__init__()
