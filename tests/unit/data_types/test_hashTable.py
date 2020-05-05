# pylint: skip-file
import pytest

from vega.utils.data_types.hash_table import Bucket
from vega.utils.data_types.hash_table import HashTable


@pytest.fixture
def bucket():
    return Bucket('foo', 5)


def mock_gen_hash(*args, **kwargs):
    return 10


@pytest.fixture(autouse=True)
def hash_table(monkeypatch):
    monkeypatch.setattr(HashTable, "_HashTable__gen_hash", mock_gen_hash)
    h = HashTable()
    return h


class TestBucket:

    def test_iterator(self, bucket):
        b = Bucket('bar', 3)
        bucket.next = b

        elements = [i.data for i in bucket]

        assert elements == [5, 3]

    def test_chaining(self, bucket):
        b = Bucket('bar', 3)
        c = bucket + b

        assert c.next == b

    @pytest.mark.parametrize("first, second, overwrite", [
        (12, 6, "hello world"),
        (9, 23, "foobar")
    ])
    def test_overwriting_existing_element(self, bucket, first, second, overwrite):
        a = Bucket('blubb', first)
        b = Bucket('bar', second)

        c = bucket + a + b

        assert c.next.data == first
        assert c.next.next.data == second

        x = Bucket('blubb', overwrite)
        c = bucket + x

        assert c.next.data == overwrite
        assert c.next.next.data == second


@pytest.mark.parametrize("first, second", [
    ("while", "if"),
    ("variable1", "variable2")
])
class TestHashTable:

    def test_store_data(self, hash_table, first, second):
        hash_table.put(first, first)

        assert hash_table._HashTable__data[10].data == first
        assert len(hash_table) == 1

    def test_collision(self, hash_table, first, second):
        hash_table.put(first, first)
        hash_table.put(second, second)

        assert hash_table._HashTable__data[10].data == first
        assert hash_table._HashTable__data[10].next.data == second
        assert len(hash_table) == 2

    def test_element_overwrite(self, hash_table, first, second):
        hash_table.put(first, first)

        assert hash_table._HashTable__data[10].data == first

        hash_table.put(first, second)

        assert hash_table._HashTable__data[10].data == second

    def test_element_retrieval(self, first, second):
        hash_table = HashTable()
        hash_table.put(first, first)
        hash_table.put(second, second)

        assert hash_table.get(first) == first
        assert hash_table.get(second) == second

    def test_element_retrieval_after_collision(self, hash_table, first, second):
        hash_table.put(first, first)
        hash_table.put(second, second)

        assert hash_table.get(first) == first
        assert hash_table.get(second) == second
