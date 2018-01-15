from typing import TypeVar, Generic, Type, Union, List
from random import sample

TData = TypeVar('Data')


class Node(Generic[TData]):

    def __init__(self, data: TData) -> None:
        self.__data = data
        self.__prev = None
        self.__next = None

    @property
    def prev(self) -> 'Node':
        return self.__prev

    @prev.setter
    def prev(self, prev: 'Node') -> None:
        self.__prev = prev

    @property
    def next(self) -> 'Node':
        return self.__next

    @next.setter
    def next(self, next: 'Node') -> None:
        self.__next = next

    @property
    def data(self) -> TData:
        return self.__data

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.data!r})'

    def __str__(self) -> str:
        return f'{self.data}'


TListElement = Union[Node, None]


class MetaList(Type[Node]):

    def __init__(self) -> None:
        self.__tail = None
        self.__head = None
        self.__count: int = 0

    @property
    def tail(self) -> TListElement:
        return self.__tail

    @tail.setter
    def tail(self, tail: TListElement):
        self.__tail = tail

    @property
    def head(self) -> TListElement:
        return self.__head

    @head.setter
    def head(self, head: TListElement):
        self.__head = head

    @property
    def count(self) -> int:
        return self.__count

    def increment(self) -> None:
        self.__count = self.__count + 1

    def decrement(self) -> None:
        self.__count = self.__count - 1

    def empty_list(self) -> bool:
        return not bool(self.head and self.tail)

    def print_list(self) -> None:
        node = self.tail
        while node is not None:
            print(node.data)
            node = node.next

    def clear_list(self) -> None:
        node = self.tail
        while not node == self.head:
            next_node = node.next
            self.tail = next_node
            next_node.prev = None
            del node
            node = next_node
            self.decrement()
        else:
            self.head = None
            self.tail = None
            del node
            self.decrement()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.count!r})'

    def __str__(self) -> str:
        return f'{self.count}'


class Stack(MetaList):

    def __init__(self) -> None:
        super().__init__()

    def push(self, data: TData) -> None:
        new_node = Node(data)
        if self.empty_list():
            self.tail = new_node
            self.head = new_node
        else:
            old_node = self.head
            self.head = new_node
            old_node.next = new_node
            new_node.prev = old_node
        self.increment()

    def pop(self):
        if self.empty_list():
            raise Exception(self, "Empty Stack")
        else:
            node = self.head
            if node == self.tail:
                self.tail = None
                self.head = None
            else:
                self.head = node.prev
                self.head.next = None
            data = node.data
            del node
            self.decrement()
        return data


class Queue(MetaList):

    def __init__(self):
        super().__init__()

    def add(self, data: TData):
        new_node = Node(data)
        if self.empty_list():
            self.tail = new_node
            self.head = new_node
        else:
            old_node = self.tail
            self.tail = new_node
            old_node.prev = new_node
            new_node.next = old_node
        self.increment()

    def remove(self):
        if self.empty_list():
            raise Exception(self, "Empty List")
        else:
            node = self.head
            if node == self.tail:
                self.tail = None
                self.head = None
            else:
                self.head = node.prev
                self.head.next = None
            data = node.data
            del node
            self.decrement()
        return data


class Bucket(Type[TData]):

    def __init__(self, key: str, data: TData) -> None:
        self.__key = key
        self.__data = data
        self.__next = None

    @property
    def key(self) -> str:
        return self.__key

    @property
    def data(self) -> TData:
        return self.__data

    @property
    def next(self) -> Union['Bucket', None]:
        return self.__next

    @next.setter
    def next(self, b: 'Bucket') -> None:
        self.__next = b

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.key!r})'

    def __str__(self) -> str:
        return f'{{\'{self.key}\': \'{self.data}\'}}'


class HashTable:

    __size: int = 256
    __count: int = 0

    def __init__(self):
        self.__rand8 = sample(range(self.size), self.size)
        self.__data: List[Bucket] = [None] * self.size
        self.__count = 0

    @property
    def size(self) -> int:
        return self.__size

    @property
    def count(self) -> int:
        return self.__count

    def __gethash(self, key: str) -> int:
        hash = 0
        for c in key:
            hash = self.__rand8[hash ^ ord(c)]
        return hash

    def get(self, key: str) -> Union[TData, None]:
        hash = self.__gethash(key)
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

    def put(self, key: str, data: TData) -> None:
        hash = self.__gethash(key)
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
                output += f'{b}'
                next = b.next
                while next is not None:
                    output += f' -> {next}'
                    next = next.next
                output += '\n'
        return output
