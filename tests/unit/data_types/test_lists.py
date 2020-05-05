# pylint: skip-file
import pytest

from vega.utils.data_types.lists import MetaList
from vega.utils.data_types.lists import Queue
from vega.utils.data_types.lists import Stack


@pytest.fixture
def meta_list():
    return MetaList()


@pytest.fixture()
def stack():
    return Stack()


@pytest.fixture()
def queue():
    return Queue()


class TestMetaList:

    def test_initialization(self, meta_list):
        assert meta_list.tail is None
        assert meta_list.head is None
        assert len(meta_list) == 0

    def test_empty_list(self, meta_list):
        assert meta_list.is_empty() is True

    def test_private_methods(self, meta_list):
        with pytest.raises(AttributeError):
            count: int = meta_list.__count
            head: object = meta_list.__head
            tail: object = meta_list.__tail

    def test_setter_methods(self, meta_list):
        node = 5

        meta_list.head = node
        meta_list.tail = node
        assert meta_list.head == node
        assert meta_list.tail == node

    def test_object_representation(self, meta_list):
        assert meta_list.__repr__() == 'MetaList(0)'

    def test_string_representation(self, meta_list):
        assert meta_list.__str__() == '0'


class TestStack:

    def test_initialization(self, stack):
        assert len(stack) == 0

    def test_add_one_element(self, stack):
        stack.push(1)

        assert len(stack) == 1
        assert stack.tail.data == 1
        assert stack.head.data == 1

    @pytest.mark.parametrize("add_one, add_two, add_three, count", [
        (1, 5, 4, 3),
        (9, 5, 0, 3)
    ])
    def test_add_multiple_elements(self, stack, add_one, add_two, add_three, count):
        stack.push(add_one)
        stack.push(add_two)
        stack.push(add_three)

        assert len(stack) == count
        assert stack.head.data == add_three
        assert stack.tail.data == add_one
        assert stack.head.prev.data == add_two
        assert stack.tail.next.data == add_two
        assert stack.head.next is None
        assert stack.tail.prev is None

    def test_remove_element_on_empty(self, stack):
        with pytest.raises(IndexError):
            stack.pop()

    @pytest.mark.parametrize("add_one, add_two, add_three, count", [
        (5, 78, 8, 2),
        (1, 7, 56, 2)
    ])
    def test_remove_element(self, stack, add_one, add_two, add_three, count):
        stack.push(add_one)
        stack.push(add_two)
        stack.push(add_three)

        element: int = stack.pop()
        assert element == add_three
        assert len(stack) == 2
        assert stack.head.data == add_two
        assert stack.head.next is None


class TestQueue:

    def test_initialization(self, queue):
        assert len(queue) == 0

    def test_add_one_element(self, queue):
        queue.add(1)

        assert len(queue) == 1
        assert queue.tail.data == 1
        assert queue.head.data == 1

    @pytest.mark.parametrize("add_one, add_two, add_three, count", [
        (1, 5, 4, 3),
        (9, 5, 0, 3)
    ])
    def test_add_multiple_elements(self, queue, add_one, add_two, add_three, count):
        queue.add(add_one)
        queue.add(add_two)
        queue.add(add_three)

        assert len(queue) == count
        assert queue.tail.data == add_three
        assert queue.head.data == add_one
        assert queue.tail.next.data == add_two
        assert queue.head.prev.data == add_two
        assert queue.tail.prev is None
        assert queue.head.next is None

    def test_remove_element_on_empty(self, queue):
        with pytest.raises(IndexError):
            queue.remove()

    @pytest.mark.parametrize("add_one, add_two, add_three, count", [
        (5, 78, 8, 2),
        (1, 7, 56, 2)
    ])
    def test_remove_element(self, queue, add_one, add_two, add_three, count):
        queue.add(add_one)
        queue.add(add_two)
        queue.add(add_three)

        element: int = queue.remove()
        assert element == add_one
        assert len(queue) == count
        assert queue.head.data == add_two
        assert queue.head.next is None
