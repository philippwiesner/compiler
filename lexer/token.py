from enum import Enum, auto
from typing import Type


class AutoID(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count + 256


class Tag(AutoID):
    AND = auto()
    BASIC = auto()
    BREAK = auto()
    DO = auto()
    ELSE = auto()
    EQ = auto()
    FALSE = auto()
    GE = auto()
    ID = auto()
    IF = auto()
    INDEX = auto()
    LE = auto()
    MINUS = auto()
    NE = auto()
    NUM = auto()
    OR = auto()
    REAL = auto()
    TEMP = auto()
    TRUE = auto()
    WHILE = auto()


class Token(Type[Tag]):

    def __init__(self, tag: Tag) -> None:
        self.__tag = tag

    @property
    def tag(self) -> Tag:
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



