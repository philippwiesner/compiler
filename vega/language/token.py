from enum import Enum
from enum import auto
from typing import Union


class AutoID(Enum):

    @staticmethod
    # pylint: disable=unused-argument
    def _generate_next_value_(name, start, count, last_values):
        return count + 256


class Tag(AutoID):
    EQ = auto()
    LE = auto()
    GE = auto()
    NE = auto()
    CONST = auto()
    FUNC = auto()
    WHILE = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    RETURN_TYPE = auto()
    RETURN = auto()
    PASS = auto()
    CONTINUE = auto()
    BREAK = auto()
    TRUE = auto()
    FALSE = auto()
    NOT = auto()
    AND = auto()
    OR = auto()
    INDEX = auto()
    ID = auto()  # identifier
    BASIC = auto()  # basic data type
    FUNCTION = auto() # for function identifiers
    TYPE = auto()  # non basic data types (e.g. strings)
    NUM = auto()  # normal numbers
    REAL = auto()  # real numbers
    LITERAL = auto()  # literals '/"


class Token:

    def __init__(self, tag: Union[Tag, str]) -> None:
        self.__tag = tag

    @property
    def tag(self) -> Union[Tag, str]:
        return self.__tag

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.tag!r})'

    def __str__(self) -> str:
        return f'{self.tag}'


class Num(Token):

    def __init__(self, value: int) -> None:
        super().__init__(Tag.NUM)
        self.__value = value

    @property
    def value(self) -> int:
        return self.__value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value!r})'

    def __str__(self) -> str:
        return f'{self.value}'


class Word(Token):

    def __init__(self, lexeme: str, tag: Tag) -> None:
        super().__init__(tag)
        self.__lexeme = lexeme

    @property
    def lexeme(self) -> str:
        return self.__lexeme

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.lexeme!r})'

    def __str__(self) -> str:
        return f'{self.lexeme}'


class Real(Token):

    def __init__(self, value: float) -> None:
        super().__init__(Tag.REAL)
        self.__value = value

    @property
    def value(self) -> float:
        return self.__value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value!r})'

    def __str__(self) -> str:
        return f'{self.value}'


class Literal(Token):

    def __init__(self, content: str) -> None:
        super().__init__(Tag.LITERAL)
        self.__content = content

    @property
    def content(self) -> str:
        return self.__content

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.content!r})'

    def __str__(self) -> str:
        return f'{self.content}'
