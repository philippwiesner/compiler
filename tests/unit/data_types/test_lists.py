# pylint: skip-file
import pytest

from vega.utils.data_types.lists import MetaList
from vega.utils.data_types.lists import Queue
from vega.utils.data_types.lists import Stack


def describe_meta_list():

    @pytest.fixture
    def meta_list():
        return MetaList()

    def describe_initialization():

        def initialization(meta_list):
            assert meta_list.tail is None
            assert meta_list.head is None
            assert len(meta_list) == 0

    def describe_empty_list():

        def empty_list(meta_list):
            assert meta_list.is_empty() is True

    def describe_representation():

        def object_representation(meta_list):
            assert repr(meta_list) == 'MetaList(0)'

        def string_representation(meta_list):
            assert str(meta_list) == '0'


def describe_stack():

    @pytest.fixture()
    def stack():
        return Stack()

    def describe_initialization():

        def initialization(stack):
            assert len(stack) == 0

    def describe_adding_elements():

        @pytest.mark.parametrize("add_one, add_two, add_three, count", [
            (1, 5, 4, 3),
            (9, 5, 0, 3)
        ])
        def add_multiple_elements(stack, add_one, add_two, add_three, count):
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

    def describe_removing_elements():

        def on_empty(stack):
            with pytest.raises(IndexError):
                stack.pop()

        @pytest.mark.parametrize("add_one, add_two, add_three, count", [
            (5, 78, 8, 2),
            (1, 7, 56, 2)
        ])
        def after_two_elements(stack, add_one, add_two, add_three, count):
            stack.push(add_one)
            stack.push(add_two)
            stack.push(add_three)

            element: int = stack.pop()
            assert element == add_three
            assert len(stack) == count
            assert stack.head.data == add_two
            assert stack.head.next is None


def describe_queue():

    @pytest.fixture()
    def queue():
        return Queue()

    def describe_initialization():

        def initialization(queue):
            assert len(queue) == 0

    def describe_adding_elements():

        @pytest.mark.parametrize("add_one, add_two, add_three, count", [
            (1, 5, 4, 3),
            (9, 5, 0, 3)
        ])
        def test_add_multiple_elements(queue, add_one, add_two, add_three, count):
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

    def describe_removing_elements():

        def on_empty(queue):
            with pytest.raises(IndexError):
                queue.remove()

        @pytest.mark.parametrize("add_one, add_two, add_three, count", [
            (5, 78, 8, 2),
            (1, 7, 56, 2)
        ])
        def after_two_elements(queue, add_one, add_two, add_three, count):
            queue.add(add_one)
            queue.add(add_two)
            queue.add(add_three)

            element: int = queue.remove()
            assert element == add_one
            assert len(queue) == count
            assert queue.head.data == add_two
            assert queue.head.next is None
