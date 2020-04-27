import unittest
from unittest.mock import MagicMock, patch
from compiler.utils.data_types.hashTable import Bucket, HashTable


class TestBucket(unittest.TestCase):

    def setUp(self):
        self.bucket = Bucket(key='foo', data=5)

    def test_iterator(self):
        b = Bucket('bar', 3)
        self.bucket.next = b

        elements = [i.data for i in self.bucket]

        self.assertEqual(elements, [5, 3])

    def test_chaining(self):
        b = Bucket('bar', 3)
        c = self.bucket + b

        self.assertEqual(c.next, b)

    def test_overwriting_existing_element(self):
        a = Bucket('blubb', 12)
        b = Bucket('bar', 6)

        c = self.bucket + a + b

        self.assertEqual(c.next.data, 12)
        self.assertEqual(c.next.next.data, 6)

        x = Bucket('blubb', 'hello world')
        c = self.bucket + x

        self.assertEqual(c.next.data, 'hello world')
        self.assertEqual(c.next.next.data, 6)


class TestHashTable(unittest.TestCase):

    class TestData:
        def __init__(self, name: str, data: str):
            self.name = name
            self.data = data

    def setUp(self) -> None:
        self.hashTable = HashTable()
        self.testData1 = TestHashTable.TestData('foo', 'Hello World')
        self.testData2 = TestHashTable.TestData('bar', 'Hello Jupiter')

    def test_store_data(self):
        self.hashTable._HashTable__gen_hash = MagicMock(return_value=10)
        self.hashTable.put(self.testData1.name, self.testData1.data)

        self.assertEqual(self.hashTable._HashTable__data[10].data, 'Hello World')
        self.assertEqual(len(self.hashTable), 1)

    def test_collision(self):
        self.hashTable._HashTable__gen_hash = MagicMock(return_value=10)
        self.hashTable.put(self.testData1.name, self.testData1.data)
        self.hashTable.put(self.testData2.name, self.testData2.data)

        self.assertEqual(self.hashTable._HashTable__data[10].data, 'Hello World')
        self.assertEqual(self.hashTable._HashTable__data[10].next.data, 'Hello Jupiter')
        self.assertEqual(len(self.hashTable), 2)

    def test_element_overwrite(self):
        self.hashTable._HashTable__gen_hash = MagicMock(return_value=10)
        self.hashTable.put(self.testData1.name, self.testData1.data)

        self.assertEqual(self.hashTable._HashTable__data[10].data, 'Hello World')

        self.hashTable.put(self.testData1.name, 'Hello Mars')

        self.assertEqual(self.hashTable._HashTable__data[10].data, 'Hello Mars')

    def test_element_retrieval(self):
        self.hashTable.put(self.testData1.name, self.testData1.data)

        self.assertEqual(self.hashTable.get('foo'), 'Hello World')

    def test_element_retrieval_after_collision(self):
        self.hashTable._HashTable__gen_hash = MagicMock(return_value=10)
        self.hashTable.put(self.testData1.name, self.testData1.data)
        self.hashTable.put(self.testData2.name, self.testData2.data)

        self.assertEqual(self.hashTable.get('foo'), 'Hello World')
        self.assertEqual(self.hashTable.get('bar'), 'Hello Jupiter')


if __name__ == '__main__':
    unittest.main()
