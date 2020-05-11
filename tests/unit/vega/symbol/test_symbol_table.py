# pylint: skip-file
import pytest

from vega.symbol.symbol_table import SymbolTable
from vega.language.types import INT, CHAR
from vega.language.vocabulary import Tag


def describe_symbol_table():
    @pytest.fixture
    def symbol_table():
        symbol_table = SymbolTable()
        symbol_table.store("A", True, INT, Tag.BASIC)
        symbol_table.store("text", False, CHAR, Tag.INDEX)
        symbol_table.enter_scope()
        symbol_table.store("do_something", False, INT, Tag.FUNCTION)
        return symbol_table

    def describe_lookup():

        def global_scope(symbol_table):

            assert symbol_table.lookup("A") is True
            assert symbol_table.lookup("do_something") is True
            assert symbol_table.lookup("not_present") is False

        def after_leaving_scope(symbol_table):
            symbol_table.leave_scope()

            assert symbol_table.lookup("A") is True
            assert symbol_table.lookup("do_something") is False
            assert symbol_table.lookup("not_present") is False
