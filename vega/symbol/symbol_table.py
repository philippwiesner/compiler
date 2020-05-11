from dataclasses import dataclass

from vega.language.types import Type
from vega.language.token import Tag
from vega.utils.data_types.hash_table import HashTable
from vega.utils.data_types.lists import Node
from vega.utils.data_types.lists import Stack


@dataclass
class Symbol:
    name: str
    const: bool
    type: Type
    id: Tag


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

    def store(self, name: str, const: bool, type: Type, id: Tag) -> None:
        if self.is_empty():
            raise IndexError("Cannot store in no scope")
        self.head.data.put(name, Symbol(name, const, type, id))
