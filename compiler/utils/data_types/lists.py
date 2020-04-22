"""Basic Implementations of Lists as data structures"""

from typing import Union, Any


class Node:
    """Single element in any list"""

    def __init__(self, data: Any) -> None:
        """

        Args:
            data: stored data
        """
        self.__data: Any = data
        self.__prev: Union['Node', None] = None
        self.__next: Union['Node', None] = None

    @property
    def prev(self) -> Union['Node', None]:
        return self.__prev

    @prev.setter
    def prev(self, prev: 'Node') -> None:
        self.__prev = prev

    @property
    def next(self) -> Union['Node', None]:
        return self.__next

    @next.setter
    def next(self, next: 'Node') -> None:
        self.__next = next

    @property
    def data(self) -> Any:
        return self.__data


class MetaList:
    """Meta implementation for lists"""

    def __init__(self) -> None:
        self.__tail: Union['Node', None] = None
        self.__head: Union['Node', None] = None
        self.__count: int = 0

    @property
    def tail(self) -> Union['Node', None]:
        return self.__tail

    @tail.setter
    def tail(self, tail: Union['Node', None]):
        self.__tail = tail

    @property
    def head(self) -> Union['Node', None]:
        return self.__head

    @head.setter
    def head(self, head: Union['Node', None]):
        self.__head = head

    @property
    def count(self) -> int:
        return self.__count

    def __increment(self) -> None:
        self.__count = self.__count + 1

    def __decrement(self) -> None:
        self.__count = self.__count - 1

    def is_empty(self) -> bool:
        return not bool(self.head and self.tail)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.count!r})'

    def __str__(self) -> str:
        return f'{self.count}'


class Stack(MetaList):
    """Stack implementation

    New elements are always added ot top and also removed from the top
    """

    def __init__(self) -> None:
        super().__init__()
        self.__count: int = 0

    @property
    def count(self) -> int:
        return self.__count

    def __increment(self) -> None:
        self.__count = self.__count + 1

    def __decrement(self) -> None:
        self.__count = self.__count - 1

    def push(self, data: Any) -> None:
        """Put data on top of the stack

        Args:
            data: stored data

        Returns:

        """
        node: Node = Node(data)
        if self.is_empty():
            self.tail = node
            self.head = node
        else:
            old_node = self.head
            self.head = node
            old_node.next = node
            node.prev = old_node
        self.__increment()

    def pop(self) -> Any:
        """Remove data from the top

        Returns:
            Stored data from the top

        """
        if self.is_empty():
            raise IndexError('Pop from empty stack')
        else:
            node: Node = self.head
            if node == self.tail:
                self.tail = None
                self.head = None
            else:
                self.head = node.prev
                self.head.next = None
            data = node.data
            del node
            self.__decrement()
        return data


class Queue(MetaList):
    """Queue implementation

    Data is always added from behind and removed from the top
    """

    def __init__(self):
        super().__init__()
        self.__count = 0

    @property
    def count(self) -> int:
        return self.__count

    def __increment(self) -> None:
        self.__count = self.__count + 1

    def __decrement(self) -> None:
        self.__count = self.__count - 1

    def add(self, data: Any):
        """Add data behind the top element

        Args:
            data: stored data

        Returns:

        """
        node: Node = Node(data)
        if self.is_empty():
            self.tail = node
            self.head = node
        else:
            old_node = self.tail
            self.tail = node
            old_node.prev = node
            node.next = old_node
        self.__increment()

    def remove(self) -> Any:
        """Remove data from the top

        Returns:
            stored data from the top
        """
        if self.is_empty():
            raise IndexError('Remove from empty queue')
        else:
            node: Node = self.head
            if node == self.tail:
                self.tail = None
                self.head = None
            else:
                self.head = node.prev
                self.head.next = None
            data = node.data
            del node
            self.__decrement()
        return data
