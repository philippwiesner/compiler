from vega.language.token import Tag
from vega.language.token import Word


class Type(Word):

    def __init__(self, token_type: str, tag: Tag, width: int) -> None:
        super().__init__(token_type, tag)
        self.__width = width

    @property
    def width(self) -> int:
        return self.__width


INT = Type("int", Tag.BASIC, 4)
FLOAT = Type("float", Tag.BASIC, 8)
CHAR = Type("char", Tag.BASIC, 1)
BOOL = Type("bool", Tag.BASIC, 1)


class Array(Type):

    def __init__(self, size: int, token_type: Type) -> None:
        super().__init__(f'{token_type}[]', Tag.INDEX, size * token_type.width)
        self.__size = size
        self.__type = token_type

    @property
    def size(self) -> int:
        return self.__size

    @property
    def type(self) -> Type:
        return self.__type

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.type}[{self.size!r}])'

    def __str__(self) -> str:
        return f'{self.type}[{self.size}]'


class String(Array):

    def __init__(self, size: int):
        super().__init__(size, CHAR)
