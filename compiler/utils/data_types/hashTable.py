from typing import Any, Union, List
from random import sample


class Bucket:

    def __init__(self, key: str, data: Any) -> None:
        self.__key: str = key
        self.__data: Any = data
        self.__next: Union['Bucket', None] = None

    @property
    def key(self) -> str:
        return self.__key

    @key.setter
    def key(self, key: str) -> None:
        self.__key = key

    @property
    def data(self) -> Any:
        return self.__data

    @property
    def next(self) -> Union['Bucket', None]:
        return self.__next

    @next.setter
    def next(self, b: Union['Bucket', None]) -> None:
        self.__next = b


class HashTable:

    __size: int = 256

    def __init__(self):
        self.__rand8: List[int] = sample(range(self.size), self.size)
        self.__data: List[Union['Bucket', None]] = [None] * self.__size
        self.__count: int = 0

    @property
    def size(self) -> int:
        return self.__size

    @property
    def count(self) -> int:
        return self.__count

    def __gen_hash(self, key: str) -> int:
        hash = 0
        for c in key:
            hash = self.__rand8[hash ^ ord(c)]
        return hash

    def get(self, key: str) -> Union[Any, None]:
        hash = self.__gen_hash(key)
        entry = self.__data[hash]
        if entry is not None:
            while entry.next is not None:
                if entry.key == key:
                    return entry.data
                else:
                    entry = entry.next
            if entry.key == key:
                return entry.data
        return None

    def put(self, key: str, data: Any) -> None:
        # TODO: same key add will remove chained items
        hash = self.__gen_hash(key)
        b = Bucket(key, data)
        entry = self.__data[hash]
        if entry is None:
            self.__data[hash] = b
        else:
            while entry is not None:
                if entry.next is None:
                    entry.next = b
                    break
                entry = entry.next
        self.__count = self.count + 1

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.size!r})'

    def __str__(self) -> str:
        output = ""
        for b in self.__data:
            if b is not None:
                output += f'{b.data}'
                next = b.next
                while next is not None:
                    output += f' -> {next.data}'
                    next = next.next
                output += '\n'
        return output
