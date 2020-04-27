"""HashTable implementation

"""

from typing import Any, Union, List
from random import sample


class Bucket:
    """Bucket

    """

    def __init__(self, key: str, data: Any) -> None:
        """

        Args:
            key:
            data:
        """
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

    @data.setter
    def data(self, data: Any) -> None:
        self.__data = data

    @property
    def next(self) -> Union['Bucket', None]:
        return self.__next

    @next.setter
    def next(self, bucket: 'Bucket') -> None:
        self.__next = bucket

    def __iter__(self) -> 'BucketIterator':
        return BucketIterator(bucket=self)

    def __add__(self, bucket: 'Bucket') -> 'Bucket':
        last: Union[Bucket, None] = None
        for last in self:
            if last.key == bucket.key:
                last.data = bucket.data
                return self
        last.next = bucket
        return self


class BucketIterator:
    def __init__(self, bucket: Bucket):
        self.bucket = bucket

    def __iter__(self) -> 'BucketIterator':
        return self

    def __next__(self) -> Union['Bucket', None]:
        if self.bucket is None:
            raise StopIteration
        bucket: 'Bucket' = self.bucket
        self.bucket = bucket.next
        return bucket


class HashTable:

    __size: int = 256

    def __init__(self):
        self.__rand8: List[int] = sample(range(self.size), self.size)
        self.__data: List[Union['Bucket', None]] = [None] * self.__size
        self.__count: int = 0

    @property
    def size(self) -> int:
        return self.__size

    def __len__(self) -> int:
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
            for bucket in entry:
                if bucket.key == key:
                    return bucket.data
        return None

    def put(self, key: str, data: Any) -> None:
        hash = self.__gen_hash(key)
        b = Bucket(key, data)
        entry = self.__data[hash]
        if entry is None:
            self.__data[hash] = b
        else:
            bucket = None
            for bucket in entry:
                pass
            bucket += b
        self.__count += 1

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.size!r})'

    def __str__(self) -> str:
        output = ""
        for b in self.__data:
            if b is not None:
                output += f'{b.data}'
                for e in b:
                    output += f' -> {e.data}'
                output += '\n'
        return output
