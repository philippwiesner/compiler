"""Basic Implementations of Lists as data structures"""
from typing import Any
from typing import Union


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
        """previous element property

        Returns:
            previous element
        """
        return self.__prev

    @prev.setter
    def prev(self, prev: 'Node') -> None:
        self.__prev = prev

    @property
    def next(self) -> Union['Node', None]:
        """next element property

        Returns:
            next element
        """
        return self.__next

    @next.setter
    def next(self, next_node: 'Node') -> None:
        self.__next = next_node

    @property
    def data(self) -> Any:
        """data property

        Returns:
            data
        """
        return self.__data


class MetaList:
    """Meta implementation for lists"""

    def __init__(self) -> None:
        self.__tail: Union['Node', None] = None
        self.__head: Union['Node', None] = None
        self._count: int = 0

    @property
    def tail(self) -> Union['Node', None]:
        """tail property

        Returns:
            last element
        """
        return self.__tail

    @tail.setter
    def tail(self, tail: Union['Node', None]):
        self.__tail = tail

    @property
    def head(self) -> Union['Node', None]:
        """head property

        Returns:
            first element
        """
        return self.__head

    @head.setter
    def head(self, head: Union['Node', None]):
        self.__head = head

    def __len__(self) -> int:
        return self._count

    def _increment(self) -> None:
        self._count += 1

    def _decrement(self) -> None:
        self._count -= 1

    def is_empty(self) -> bool:
        """check if list is empty

        Returns:
            True when empty, false otherwise
        """
        return not bool(self.head and self.tail)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({len(self)!r})'

    def __str__(self) -> str:
        return f'{len(self)}'


class Stack(MetaList):
    """Stack implementation

    New elements are always added ot top and also removed from the top
    """

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
        self._increment()

    def pop(self) -> Any:
        """Remove data from the top

        Returns:
            Stored data from the top

        """
        if self.is_empty():
            raise IndexError('Pop from empty stack')

        node: Node = self.head
        if node == self.tail:
            self.tail = None
            self.head = None
        else:
            self.head = node.prev
            self.head.next = None
        data = node.data
        del node
        self._decrement()
        return data


class Queue(MetaList):
    """Queue implementation

    Data is always added from behind and removed from the top
    """

    # pylint: disable=unused-argument
    def add(self, data: Any, *args, **kwargs) -> None:
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
        self._increment()

    def remove(self) -> Any:
        """Remove data from the top

        Returns:
            stored data from the top
        """
        if self.is_empty():
            raise IndexError('Remove from empty queue')

        node: Node = self.head
        if node == self.tail:
            self.tail = None
            self.head = None
        else:
            self.head = node.prev
            self.head.next = None
        data = node.data
        del node
        self._decrement()
        return data
