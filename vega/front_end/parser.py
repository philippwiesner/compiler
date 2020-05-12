"""Vega parser

Check syntax of Vega programm code. Return syntax errors on invalid syntax.
Create AST for further code analysis.
"""

from typing import Union
from io import TextIOWrapper

from vega.front_end.lexer import Lexer
from vega.utils.data_types.lists import TokenStream
from vega.symbol.symbol_table import SymbolTable
from vega.language import vocabulary
from vega.language.token import Tag, Token, Word, Num, Real, Literal


class Parser:

    def __init__(self, code: TextIOWrapper) -> None:
        lexer: Lexer = Lexer(code)
        self.__token_stream: Union[TokenStream] = lexer.scan()
        self.__table: SymbolTable = SymbolTable()
        self.__line: int = 0

    def parse(self):
        self.__block()

    def __get_token(self):
        token: Union[Token, Word, Num, Real, Literal]
        token, self.__line = self.__token_stream.remove()
        return token

    def __block(self):

        if self.__get_token() == Tag.FUNC:
            pass
