"""Tokens of vega language

Define Tokens lexical scanner creates from vega program code

"""
from enum import Enum
from enum import auto
from typing import Any
from typing import Union


class AutoID(Enum):
    """Create new ``Enum`` element for Token IDs"""

    @staticmethod
    # pylint: disable=unused-argument
    def _generate_next_value_(name: str, start: int, count: int,
                              last_values: Any) -> int:
        """Start numbering of Tokens at 256

        Args:
            name: not used
            start: not used
            count: counter
            last_values: not used

        Returns:
            token id
        """
        return count + 256


class Tag(AutoID):
    """Token Tag

    Represent every ``Token`` as an ID number
    """
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
    FUNCTION = auto()  # for function identifiers
    TYPE = auto()  # non basic data types (e.g. strings)
    NUM = auto()  # normal numbers
    REAL = auto()  # real numbers
    LITERAL = auto()  # literals '/"


class Token:
    """Base token class

    One character language elements like *, +, { are stored as string tokens.
    Every other language element are stored as inheritated classes with their
    respective IDs

    """

    def __init__(self, tag: Union[Tag, str]) -> None:
        """Create new token with its tag

        Args:
            tag: token tag
        """
        self.__tag = tag

    @property
    def tag(self) -> Union[Tag, str]:
        """Tag property

        Returns:
            Tag id or string
        """
        return self.__tag

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.tag!r})'

    def __str__(self) -> str:
        return f'{self.tag}'


class Num(Token):
    """Number tokens

    Represent integer numbers
    """

    def __init__(self, value: int) -> None:
        """Create number token with number id and store integer value

        Args:
            value: integer value
        """
        super().__init__(Tag.NUM)
        self.__value = value

    @property
    def value(self) -> int:
        """Value property

        Returns:
            integer value
        """
        return self.__value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value!r})'

    def __str__(self) -> str:
        return f'{self.value}'


class Word(Token):
    """Word tokens

    Words can be keywords like while, if, func or identifiers like i, var1,
    var2 or combined tokens like ==, <=, ->

    """

    def __init__(self, lexeme: str, tag: Tag) -> None:
        """Create word token

        Args:
            lexeme: keyword, variable name, combined token
            tag: keyword tag, variable tag, comined token tag
        """
        super().__init__(tag)
        self.__lexeme = lexeme

    @property
    def lexeme(self) -> str:
        """Lexeme property

        Returns:
            saved word
        """
        return self.__lexeme

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.lexeme!r})'

    def __str__(self) -> str:
        return f'{self.lexeme}'


class Real(Token):
    """Real token

    Token for real numbers
    """

    def __init__(self, value: float) -> None:
        """Create token with real tag and store real number value

        Args:
            value: real(floating) number value
        """
        super().__init__(Tag.REAL)
        self.__value = value

    @property
    def value(self) -> float:
        """Value property

        Returns:
            floating number value
        """
        return self.__value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value!r})'

    def __str__(self) -> str:
        return f'{self.value}'


class Literal(Token):
    """Literal Token

    Token for literals e.g. strings or characters, everything enclosed in
    between '' and ""

    """

    def __init__(self, content: str) -> None:
        """Create token with literal tag and literal content

        Args:
            content: literal content
        """
        super().__init__(Tag.LITERAL)
        self.__content = content

    @property
    def content(self) -> str:
        """Content property

        Returns:
            literal content
        """
        return self.__content

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.content!r})'

    def __str__(self) -> str:
        return f'{self.content}'


TokenType = Union[Token, Word, Num, Real, Literal, str]
