import unittest
from vega.utils.data_types.lists import MetaList, Stack, Queue


class TestMetaList(unittest.TestCase):

    def setUp(self):
        self.meta_list: MetaList = MetaList()

    def test_initialization(self):
        self.assertEqual(self.meta_list.tail, None)
        self.assertEqual(self.meta_list.head, None)
        self.assertEqual(len(self.meta_list), 0)

    def test_empty_list(self):
        self.assertEqual(self.meta_list.is_empty(), True)

    def test_private_methods(self):
        with self.assertRaises(AttributeError):
            count: int = self.meta_list.__count
            head: object = self.meta_list.__head
            tail: object = self.meta_list.__tail

    def test_setter_methods(self):
        node = 5
        self.meta_list.head = node
        self.meta_list.tail = node
        self.assertEqual(self.meta_list.head, node)
        self.assertEqual(self.meta_list.tail, node)

    def test_object_representation(self):
        self.assertEqual(self.meta_list.__repr__(), 'MetaList(0)')

    def test_string_representation(self):
        self.assertEqual(self.meta_list.__str__(), '0')


class TestStack(unittest.TestCase):

    def setUp(self) -> None:
        self.stack = Stack()

    def test_initialization(self):
        self.assertEqual(len(self.stack), 0)

    def test_add_one_element(self):
        self.stack.push(1)

        self.assertEqual(len(self.stack), 1)
        self.assertEqual(self.stack.tail.data, 1)
        self.assertEqual(self.stack.head.data, 1)

    def test_add_two_elements(self):
        self.stack.push(1)
        self.stack.push(5)

        self.assertEqual(len(self.stack), 2)
        self.assertEqual(self.stack.head.data, 5)
        self.assertEqual(self.stack.tail.data, 1)
        self.assertEqual(self.stack.head.prev.data, 1)
        self.assertEqual(self.stack.tail.next.data, 5)
        self.assertEqual(self.stack.tail.prev, None)
        self.assertEqual(self.stack.head.next, None)

    def test_remove_element_on_empty(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_remove_element(self):
        self.stack.push(1)
        self.stack.push(5)
        self.stack.push(7)

        element: int = self.stack.pop()
        self.assertEqual(element, 7)
        self.assertEqual(len(self.stack), 2)
        self.assertEqual(self.stack.head.data, 5)
        self.assertEqual(self.stack.head.next, None)


class TestQueue(unittest.TestCase):

    def setUp(self) -> None:
        self.queue = Queue()

    def test_initialization(self):
        self.assertEqual(len(self.queue), 0)

    def test_add_one_element(self):
        self.queue.add(1)

        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue.tail.data, 1)
        self.assertEqual(self.queue.head.data, 1)

    def test_add_two_elements(self):
        self.queue.add(1)
        self.queue.add(5)

        self.assertEqual(len(self.queue), 2)
        self.assertEqual(self.queue.tail.data, 5)
        self.assertEqual(self.queue.head.data, 1)
        self.assertEqual(self.queue.tail.next.data, 1)
        self.assertEqual(self.queue.head.prev.data, 5)
        self.assertEqual(self.queue.tail.prev, None)
        self.assertEqual(self.queue.head.next, None)

    def test_remove_element_on_empty(self):
        with self.assertRaises(IndexError):
            self.queue.remove()

    def test_remove_element(self):
        self.queue.add(1)
        self.queue.add(5)
        self.queue.add(7)

        element: int = self.queue.remove()
        self.assertEqual(element, 1)
        self.assertEqual(len(self.queue), 2)
        self.assertEqual(self.queue.head.data, 5)
        self.assertEqual(self.queue.head.next, None)


if __name__ == '__main__':
    unittest.main()
