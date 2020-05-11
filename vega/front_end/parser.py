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
from vega.language import types


class Parser:

    def __init__(self, code: TextIOWrapper) -> None:
        lexer: Lexer = Lexer(code)
        self.__token_stream: Union[TokenStream] = lexer.scan()
        self.__table: SymbolTable = SymbolTable()

