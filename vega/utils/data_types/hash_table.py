"""HashTable implementation

"""

from random import sample
from typing import Any
from typing import List
from typing import Union


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
        hash_code = 0
        for char in key:
            hash_code = self.__rand8[hash_code ^ ord(char)]
        return hash_code

    def get(self, key: str) -> Union[Any, None]:
        hash_code = self.__gen_hash(key)
        entry = self.__data[hash_code]
        if entry is not None:
            for bucket in entry:
                if bucket.key == key:
                    return bucket.data
        return None

    def put(self, key: str, data: Any) -> None:
        hash_code = self.__gen_hash(key)
        new_bucket = Bucket(key, data)
        entry = self.__data[hash_code]
        if entry is None:
            self.__data[hash_code] = new_bucket
        else:
            for bucket in entry:
                if bucket.key == key:
                    entry += new_bucket
                    return
            entry += new_bucket

        self.__count += 1

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.size!r})'

    def __str__(self) -> str:
        output = ""
        for bucket in self.__data:
            if bucket is not None:
                output += f'{bucket.data}'
                for element in iter(bucket):
                    output += f' -> {element.data}'
                output += '\n'
        return output
