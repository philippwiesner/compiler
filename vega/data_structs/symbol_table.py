"""Symbol table

Implements symbol table and needed data structures for storing data
inside symbol table

"""
from dataclasses import dataclass
from typing import Tuple
from typing import Union

from vega.language.types import Type
from vega.utils.data_types.hash_table import HashTable
from vega.utils.data_types.lists import Node
from vega.utils.data_types.lists import Stack


@dataclass
class Symbol:
    """Symbol data structure

    Defines a symbol to be stored in the symbol table with the following
    attributes:

    Properties:
        name: str - Name of the symbol
        const: bool - True if symbol is a constant
        callable: bool - True if symbol is a callable like a function call
        type: Type - variable type of the symbol

    """
    name: str
    const: bool
    callable: bool
    type: Union[Type, None]


@dataclass
class Scope:
    """Scope data structure

    Defines a scope in which symbols can be stored.

    Properties:
        name: str - Name of the scope
        table: HashTable - hash table for storing symbols

    """
    name: str
    table: HashTable


class SymbolTable(Stack):
    """Symbol table for storing symbols

    A symbol table is implemented like a stack, on each level of the stack
    a hash table is pushed for storing data. Symbols are first looked up on the
    top of the stack. If an element is not found, lookup one level below in the
    stack.

    """

    def __init__(self) -> None:
        """Initialize Symbol table with global scope"""
        super().__init__()
        self.enter_scope('global')

    def enter_scope(self, scope_name: str) -> None:
        """Create a new scope

        A new scope is created by pushing a new Scope on the stack

        Args:
            scope_name: name of the new scope to be created
        """
        scope = Scope(scope_name, HashTable())
        self.push(scope)

    def leave_scope(self) -> None:
        """Remove scope from top of the stack"""
        if self.is_empty():
            raise IndexError("Cannot leave no scope")
        scope: Scope = self.pop()
        del scope

    def lookup(self, name: str) -> bool:
        """Lookup symbol in symbol table

        First lookup on top of the stack, then move one level down till bottom

        Args:
            name: symbol name to look for

        Returns:
            True if symbol with name is found, False otherwise
        """
        current_scope: Node = self.head
        while current_scope:
            if current_scope.data.table.get(name):
                return True
            current_scope = current_scope.prev
        return False

    def retrieve(self, name: str) -> Tuple[Union[Symbol, None], str]:
        """Get symbol from hash table

        See ``self.lookup()`` for symbol search.

        Args:
            name: symbol name to retrieve

        Returns:
            Tuple of symbol and scope name if found, Tuple of None otherwise
        """
        current_scope: Node = self.head
        while current_scope:
            symbol: Union[Symbol, None] = current_scope.data.table.get(name)
            scope: str = current_scope.data.name
            if symbol:
                return symbol, scope
            current_scope = current_scope.prev
        return None, ''

    def store(self, symbol: Symbol) -> None:
        """Store symbol in symbol table

        Store a symbol on top scope of the stack

        Args:
            symbol: Symbol to the stored

        """
        if self.is_empty():
            raise IndexError("Cannot store in no scope")
        self.head.data.table.put(symbol.name, symbol)
