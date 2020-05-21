"""Vega vocabulary

Define keywords and words for lexical scanning

"""
from typing import List

from vega.language.token import Tag
from vega.language.token import Word
from vega.language.types import BOOL
from vega.language.types import CHAR
from vega.language.types import FLOAT
from vega.language.types import INT

RETURN_TYPE = Word("->", Tag.RETURN_TYPE)
EQ = Word("<=", Tag.EQ)
NE = Word("!=", Tag.NE)
LE = Word("<=", Tag.LE)
GE = Word(">=", Tag.GE)
AND = Word("&&", Tag.AND)
OR = Word("||", Tag.OR)

keywords: List = [
    INT,
    FLOAT,
    CHAR,
    BOOL,
    Word("str", Tag.TYPE),
    Word("true", Tag.TRUE),
    Word("false", Tag.FALSE),
    Word("func", Tag.FUNC),
    Word("const", Tag.CONST),
    Word("return", Tag.RETURN),
    Word("while", Tag.WHILE),
    Word("break", Tag.BREAK),
    Word("continue", Tag.CONTINUE),
    Word("if", Tag.IF),
    Word("elif", Tag.ELIF),
    Word("else", Tag.ELSE),
    Word("and", Tag.AND),
    Word("or", Tag.OR)
]
