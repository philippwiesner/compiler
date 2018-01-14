from utils.base_types import HashTable
from lexer.token import Word, Tag, Token, Num, Real
from symbols.types import INT, FLOAT, CHAR, BOOL
from io import TextIOWrapper

AND = Word("&&", Tag.AND)
OR = Word("||", Tag.OR)
EQ = Word("==", Tag.EQ)
NE = Word("!=", Tag.NE)
LE = Word("<=", Tag.LE)
GE = Word(">=", Tag.GE)
MINUS = Word("minus", Tag.MINUS)
TRUE = Word("true", Tag.TRUE)
FALSE = Word("false", Tag.FALSE)
TEMP = Word("temp", Tag.TEMP)

reserved_keywords = [
    Word("if", Tag.IF),
    Word("else", Tag.ELSE),
    Word("while", Tag.WHILE),
    Word("do", Tag.DO),
    Word("break", Tag.BREAK),
    Word("function", Tag.FUNCTION),
    TRUE,
    FALSE,
    INT,
    FLOAT,
    CHAR,
    BOOL
]


class Lexer:
    __line: int = 1
    __peek: str = None
    __code: TextIOWrapper = ''
    __words: HashTable = HashTable()

    def __init__(self, code: TextIOWrapper):
        for keyword in reserved_keywords:
            self.__reserve(keyword)
        self.__code = code

    def __reserve(self, word: Word) -> None:
        self.__words.put(word.lexeme, word)

    @property
    def words(self) -> HashTable:
        return self.__words

    def __readch(self) -> bool:
        self.__peek = self.__code.read(1)
        if len(self.__peek) == 0:
            return False
        return True

    def __readcch(self, c: str) -> bool:
        self.__readch()
        if self.__peek != c:
            return False
        self.__peek = ''
        return True

    def scan(self) -> Token:
        if self.__peek is not None:
            tok: Token = Token(self.__peek)
            self.__peek = None
            return tok
        while self.__readch():
            if self.__peek == ' ' or self.__peek == '\t':
                continue
            elif self.__peek == '\n':
                self.__line += 1
            else:
                break
        if self.__peek == '&':
            if self.__readcch('&'):
                return AND
            else:
                return Token('&')
        if self.__peek == '|':
            if self.__readcch('|'):
                return OR
            else:
                return Token('|')
        if self.__peek == '=':
            if self.__readcch('='):
                return EQ
            else:
                return Token('=')
        if self.__peek == '!':
            if self.__readcch('='):
                return NE
            else:
                return Token('!')
        if self.__peek == '<':
            if self.__readcch('='):
                return LE
            else:
                return Token('<')
        if self.__peek == '>':
            if self.__readcch('='):
                return GE
            else:
                return Token('>')
        if self.__peek.isdigit():
            v: int = 0
            while self.__peek.isdigit():
                v = 10 * v + int(self.__peek)
                self.__readch()
            if self.__peek != '.':
                return Num(v)
            x: float = v
            d: float = 10
            self.__readch()
            while self.__peek.isdigit():
                x = x + int(self.__peek.isdigit()) / d
                d *= 10
                self.__readch()
            return Real(x)
        if self.__peek.isalpha():
            s: str = ''
            while self.__peek.isalnum():
                s += self.__peek
                self.__readch()
            lookup: Word = self.__words.get(s)
            if lookup is not None:
                return lookup
            w = Word(s, Tag.ID)
            self.__words.put(s, w)
            return w
        tok: Token = Token(self.__peek)
        self.__peek = None
        return tok