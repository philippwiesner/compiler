from inter.expr import Expr
from symbols.types import Type
from lexer.lexer import Word


class Id(Expr):
    __offset: int = 0

    def __init__(self, id: Word, p: Type, b: int) -> None:
        super(Id, self).__init__(id, p)
        self.__offset = b

    @property
    def offset(self) -> int:
        return self.__offset
