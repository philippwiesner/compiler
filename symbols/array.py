from symbols.types import Type
from lexer.token import Tag


class Array(Type):
    __type: 'Array' = None
    __size: int = 1

    def __init__(self, sz: int, p: Type) -> None:
        super(Array, self).__init__("[]", Tag.INDEX, sz * p.width)
        self.__size = sz
        self.__type = p

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

