from utils.data_types.lists import HashTable
from lexer.token import Token
from inter.Id import Id
from typing import Union, cast


class SymbolTable(object):
    __table: HashTable = None
    __prev: 'SymbolTable' = None

    def __init__(self, prev: 'SymbolTable' = None) -> None:
        super().__init__()
        self.__table = HashTable()
        self.__prev = prev

    @property
    def prev(self) -> 'SymbolTable':
        return self.__prev

    def put(self, w: Token, i: Id) -> None:
        self.__table.put(w.__str__(), i)

    def get(self, w: Token) -> Union[Id, None]:
        scope = self
        while scope is not None:
            found = scope.__table.get(w.__str__())
            if found is not None:
                return cast(found, Id)
            scope = scope.prev
        return None
