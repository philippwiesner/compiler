from inter.node import Node
from lexer.token import Token
from symbols.types import Type


class Expr(Node):
    __op: Token = None
    __type: Type = None

    def __init__(self, tok: Token, p: Type) -> None:
        super(Expr, self).__init__()
        self.__op = tok
        self.__type = p

    @property
    def op(self) -> Token:
        return self.__op

    @property
    def type(self) -> Type:
        return self.__type

    def gen(self) -> 'Expr':
        return self

    def reduce(self) -> 'Expr':
        return self

    def emitjumps(self, test: str, t: int, f: int) -> None:
        if t != 0 and f != 0:
            self.emit(f'if {test} goto L{t}')
            self.emit(f'goto L{f}')
        elif t != 0:
            self.emit(f'if {test} goto L{t}')
        elif f != 0:
            self.emit(f'iffalse {test} goto L{f}')

    def jumping(self, i: int, f: int) -> None:
        self.emitjumps(self.__str__(), i, f)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.op})'

    def __str__(self) -> str:
        return f'{self.op}'
