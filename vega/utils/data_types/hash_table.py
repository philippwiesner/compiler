"""HashTable implementation

A hash table is used in meany places in the compiler. Mainly as a storage for
symbols in the symbol table for lookups on variables.

"""

from random import sample
from typing import Any
from typing import List
from typing import Union


class Bucket:
    """Bucket

    Storage container for data inside the hash table.

    The bucket can be linked together resulting in a simple linked list. An
    iterator over the buckets gives the flexibility to iterate over them.
    Bucket can be linked together using the overloaded add (+) operator.

    """

    def __init__(self, key: str, data: Any) -> None:
        """Create new bucket with a name and data to be stored

        Args:
            key: name or identifier for the data
            data: data to be stored
        """
        self.__key: str = key
        self.__data: Any = data
        self.__next: Union['Bucket', None] = None

    @property
    def key(self) -> str:
        """Key property

        Returns:
            name of the data
        """
        return self.__key

    @key.setter
    def key(self, key: str) -> None:
        self.__key = key

    @property
    def data(self) -> Any:
        """Data property

        Returns:
            data inside the bucket
        """
        return self.__data

    @data.setter
    def data(self, data: Any) -> None:
        self.__data = data

    @property
    def next(self) -> Union['Bucket', None]:
        """Next bucket property

        Returns:
            next bucket of the current one
        """
        return self.__next

    @next.setter
    def next(self, bucket: 'Bucket') -> None:
        self.__next = bucket

    def __iter__(self) -> 'BucketIterator':
        """Define iterator for bucket element

        Returns:
            bucket iterator
        """
        return BucketIterator(bucket=self)

    def __add__(self, bucket: 'Bucket') -> 'Bucket':
        """Overload add operator for linking buckets together

        If the new bucket name is already present in the linked bucket list,
        just override the data of the old bucket in the list with the new one.
        This gives the possibility to simply update the data of one bucket.

        Args:
            bucket: new bucket to be added to the list

        Returns:
            Current bucket with the new one added to the list
        """
        last: Union[Bucket, None] = None
        for last in self:
            if last.key == bucket.key:
                last.data = bucket.data
                return self
        last.next = bucket
        return self


class BucketIterator:
    """Bucket iterator

    """

    def __init__(self, bucket: Bucket):
        self.bucket = bucket

    def __iter__(self) -> 'BucketIterator':
        return self

    def __next__(self) -> Union['Bucket', None]:
        """Go to next bucket via next links of bucket elements"""
        if self.bucket is None:
            raise StopIteration
        bucket: 'Bucket' = self.bucket
        self.bucket = bucket.next
        return bucket


class HashTable:
    """Hash table

    """
    __size: int = 256

    def __init__(self):
        """Create new hashtable

        The hashtable contains a list of the numbers from 1 to 256 randomly
        shuffled as a seed for its hash function. It uses a simple hashing
        function to calculate the hash. On collision of elements
        the buckets will the linked using the linked list implementation of
        the bucket class.

        """
        self.__rand8: List[int] = sample(range(self.size), self.size)
        self.__data: List[Union['Bucket', None]] = [None] * self.__size
        self.__count: int = 0

    @property
    def size(self) -> int:
        """Size property

        Returns:
            size of the hashtable
        """
        return self.__size

    def __len__(self) -> int:
        return self.__count

    def __gen_hash(self, key: str) -> int:
        """Generate hash of a given key

        The hash function works as follows:

        On start:
            set hash_code to 0
        On first iteration (first char from key):
            or-conjunction between hash_code and ordeal number of char
            use resulting number as index for retrieving number from random
            shuffled list
            set this number to new hash_code
        Iterate through key till the end

        Args:
            key: key to generate hash for

        Returns:
            hash of the key
        """
        hash_code = 0
        for char in key:
            hash_code = self.__rand8[hash_code ^ ord(char)]
        return hash_code

    def get(self, key: str) -> Union[Any, None]:
        """Get element from hash table by key

        Args:
            key: key to identify element in hash table

        Returns:
            element to be stored in hash table, if no element can be found,
            return None
        """
        hash_code = self.__gen_hash(key)
        entry = self.__data[hash_code]
        if entry is not None:
            for bucket in entry:
                if bucket.key == key:
                    return bucket.data
        return None

    def put(self, key: str, data: Any) -> None:
        """Store element in hash table

        Args:
            key: key to generate hash for element
            data: element to be stored

        Returns:

        """
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
