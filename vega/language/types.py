from typing import List

from vega.language.token import Tag
from vega.language.token import Word


class Type(Word):

    def __init__(self, token_type: str, tag: Tag, width: int) -> None:
        super().__init__(token_type, tag)
        self.__width: int = width

    @property
    def width(self) -> int:
        return self.__width


INT = Type("int", Tag.BASIC, 4)
FLOAT = Type("float", Tag.BASIC, 8)
CHAR = Type("char", Tag.BASIC, 1)
BOOL = Type("bool", Tag.BASIC, 1)


class Array(Type):

    def __init__(self, token_type: Type, **kwargs) -> None:
        self.__size: int = kwargs.get('size', 0)
        self.__dimensions: List = [self.__size]
        self.__type: Type = token_type
        if isinstance(token_type, Array):
            self.__dimensions = token_type.dimensions + self.__dimensions
            self.__type = token_type.type
        super().__init__('[]',
                         Tag.INDEX,
                         self.__size*token_type.width)

    @property
    def dimensions(self) -> List:
        return self.__dimensions

    @property
    def type(self) -> Type:
        return self.__type

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.type}{self.dimensions!r})'

    def __str__(self) -> str:
        return f'{self.type}{self.dimensions}'


class String(Array):

    def __init__(self, **kwargs):
        super().__init__(CHAR, **kwargs)
