# pylint: skip-file
import pytest
import random
import string

from vega.utils.data_types.hash_table import Bucket
from vega.utils.data_types.hash_table import HashTable


class MockHashTable(HashTable):
    pass


def describe_bucket():
    @pytest.fixture
    def bucket():
        return Bucket('foo', 5)

    def describe_iterator():
        def iterator(bucket):
            b: Bucket = Bucket('bar', 3)
            bucket.next = b
            elements = [i.data for i in bucket]

            assert elements == [5, 3]

    def describe_bucket_chain():
        def chaining(bucket):
            b: Bucket = Bucket('bar', 3)
            c: Bucket = bucket + b

            assert c.next == b

        @pytest.mark.parametrize("first, second, overwrite", [
            (12, 6, "hello world"),
            (9, 23, "foobar")
        ])
        def overwrite_element_in_chain(bucket, first, second, overwrite):
            a: Bucket = Bucket('blubb', first)
            b: Bucket = Bucket('bar', second)
            c: Bucket = bucket + a + b

            assert c.next.data == first
            assert c.next.next.data == second

            x: Bucket = Bucket('blubb', overwrite)
            c: Bucket = bucket + x

            assert c.next.data == overwrite
            assert c.next.next.data == second


def describe_hash_table():
    def mock_gen_hash(*args, **kwargs):
        return 10

    @pytest.fixture(autouse=True)
    def mocked_hash_table(monkeypatch):
        monkeypatch.setattr(MockHashTable, "_HashTable__gen_hash",
                            mock_gen_hash)
        hash_table = MockHashTable()
        return hash_table

    @pytest.mark.parametrize("first, second", [
        pytest.param("while", "if", id="keywords"),
        pytest.param("variable1", "variable2", id="identifier")
    ])
    def describe_retrieving_data():
        def simple_retrieval(first, second):
            hash_table = HashTable()
            hash_table.put(first, first)
            hash_table.put(second, second)

            assert len(hash_table) == 2
            assert hash_table.get(first) == first
            assert hash_table.get(second) == second

        def retrieval_after_collision(mocked_hash_table, first, second):
            mocked_hash_table.put(first, first)
            mocked_hash_table.put(second, second)

            assert len(mocked_hash_table) == 2
            assert mocked_hash_table.get(first) == first
            assert mocked_hash_table.get(second) == second

        def retrieval_after_overwrite(mocked_hash_table, first, second):
            mocked_hash_table.put(first, first)
            mocked_hash_table.put(second, second)
            mocked_hash_table.put(first, second)

            assert len(mocked_hash_table) == 2
            assert mocked_hash_table.get(first) == second

    def describe_performance():

        def random_strings():
            rlist = []
            for entry in range(128):
                rlist.append(''.join([random.choice(string.ascii_letters +
                                                    string.digits) for n in
                                      range(random.randrange(1, 32))]))
            return rlist

        def enforce_collision():
            collisions = 0
            for i in range(100):
                hash_table = HashTable()
                random_entries = list(set(random_strings()))
                for entry in random_entries:
                    hash_table.put(entry, entry)
                collisions += hash_table.collisions / 100
                del hash_table
            assert collisions < 30

