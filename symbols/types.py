from lexer.token import Word, Tag


class Type(Word):
    __width = 0

    def __init__(self, s: str, tag: Tag, w: int) -> None:
        super(Type, self).__init__(s, tag)
        self.__width = w

    @property
    def width(self) -> int:
        return self.__width


INT = Type("int", Tag.BASIC, 4)
FLOAT = Type("float", Tag.BASIC, 8)
CHAR = Type("char", Tag.BASIC, 1)
BOOL = Type("bool", Tag.BASIC, 1)
