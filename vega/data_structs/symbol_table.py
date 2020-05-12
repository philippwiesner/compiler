from dataclasses import dataclass
from typing import Union

from vega.language.types import Type
from vega.language.token import Tag
from vega.utils.data_types.hash_table import HashTable
from vega.utils.data_types.lists import Node
from vega.utils.data_types.lists import Stack


@dataclass
class Symbol:
    name: str
    const: bool
    type: Union[Type, None]
    tag: Tag


class SymbolTable(Stack):

    def __init__(self) -> None:
        super().__init__()
        self.enter_scope()

    def enter_scope(self) -> None:
        self.push(HashTable())

    def leave_scope(self) -> None:
        if self.is_empty():
            raise IndexError("Cannot leave no scope")
        table: HashTable = self.pop()
        del table

    def lookup(self, name: str) -> bool:
        current_scope: Node = self.head
        while current_scope:
            if current_scope.data.get(name):
                return True
            current_scope = current_scope.prev
        return False

    def retrieve(self, name: str) -> Union[Symbol, None]:
        current_scope: Node = self.head
        while current_scope:
            symbol: Union[Symbol, None] = current_scope.data.get(name)
            if symbol:
                return symbol
            current_scope = current_scope.prev
        return None

    def store(self, symbol: Symbol) -> None:
        if self.is_empty():
            raise IndexError("Cannot store in no scope")
        self.head.data.put(symbol.name, symbol)
