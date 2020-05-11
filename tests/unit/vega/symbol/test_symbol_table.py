import pytest

from vega.symbol.symbol_table import SymbolTable
from vega.language.types import INT, CHAR
from vega.language.vocabulary import Tag


def describe_symbol_table():
    @pytest.fixture
    def symbol_table() -> SymbolTable:
        table = SymbolTable()
        table.store("A", True, INT, Tag.BASIC)
        table.store("text", False, CHAR, Tag.INDEX)
        return table

    def describe_lookup():
        @pytest.mark.parametrize(
            "name",
            [
                pytest.param("A", id="const_integer"),
                pytest.param("text", id="string"),
            ]
        )
        def describe_global_scope(symbol_table, name):
            assert symbol_table.lookup(name) is True
