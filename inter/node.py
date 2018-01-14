from lexer.lexer import Lexer


class Node(object):
    __lexline: int = 0
    __labels: int = 0

    def __init__(self) -> None:
        self.__lexline = Lexer.line

    @property
    def lexline(self) -> int:
        return self.__lexline

    @property
    def labels(self) -> int:
        return self.__labels

    def newlabel(self) -> int:
        self.__labels += 1
        return self.labels

    def emitlabel(self, i: int):
        print(f'L{i}:')

    def emit(self, s: str):
        print(f'\t{s}')

