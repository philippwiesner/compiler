# pylint: skip-file
import pytest

from vega.data_structs.symbol_table import Symbol
from vega.data_structs.symbol_table import SymbolTable
from vega.language.types import INT
from vega.language.types import String


def describe_symbol_table():
    @pytest.fixture
    def symbol_table():
        symbol_table = SymbolTable()
        symbol_table.store(Symbol("A", True, False, INT))
        symbol_table.store(Symbol("text", False, False, String()))
        symbol_table.enter_scope('function')
        symbol_table.store(Symbol("do_something", False, True, INT))
        return symbol_table

    def describe_lookup():
        @pytest.mark.parametrize("lookup, bool", [
            pytest.param("A", True, id="variable_A"),
            pytest.param("do_something", True, id="function"),
            pytest.param("not_present", False, id="not_present")
        ])
        def global_scope(symbol_table, lookup, bool):
            assert symbol_table.lookup(lookup) is bool

        def retrieval(symbol_table):
            symbol: Symbol
            scope: str
            symbol, scope = symbol_table.retrieve("do_something")
            assert scope == 'function'
            assert symbol.name == "do_something"
            assert symbol.type == INT
            assert symbol.callable is True

        @pytest.mark.parametrize("lookup, bool", [
            pytest.param("A", True, id="variable_A"),
            pytest.param("do_something", False, id="function"),
            pytest.param("not_present", False, id="not_present")
        ])
        def after_leaving_scope(symbol_table, lookup, bool):
            symbol_table.leave_scope()

            assert symbol_table.lookup(lookup) is bool
