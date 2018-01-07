from utils.base_types import HashTable
from lexer.token import Word, Tag
from symbols.types import INT, FLOAT, CHAR, BOOL

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
    TRUE,
    FALSE,
    INT,
    FLOAT,
    CHAR,
    BOOL
]


class Lexer:
    line: int = 1
    words = HashTable()

    def __init__(self):
        for keyword in reserved_keywords:
            self.reserve(keyword)

    def reserve(self, word: Word) -> None:
        self.words.put(word.lexeme, word)