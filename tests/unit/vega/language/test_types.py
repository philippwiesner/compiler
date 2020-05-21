# pylint: skip-file
import pytest

from vega.language.token import Tag
from vega.language.types import Array
from vega.language.types import CHAR
from vega.language.types import INT
from vega.language.types import String


def describe_array():
    @pytest.fixture
    def empty_array():
        return Array(INT)

    def describe_empty_arrays():
        def int_type(empty_array):
            assert empty_array.type == INT
            assert empty_array.tag == Tag.INDEX

        def one_dimension_size(empty_array):
            assert empty_array.width == 0
            assert empty_array.dimensions == [0]

        def multi_dimension_size(empty_array):
            new_array: Array = Array(Array(empty_array))

            assert new_array.width == 0
            assert new_array.dimensions == [0, 0, 0]

    @pytest.fixture
    def int_array():
        return Array(INT, size=2)

    def describe_int_arrays():
        def one_dimension_size(int_array):
            assert int_array.width == 8
            assert int_array.dimensions == [2]

        def multi_dimension_size(int_array):
            new_array: Array = Array(Array(int_array, size=3), size=5)

            assert new_array.width == 120
            assert new_array.dimensions == [2, 3, 5]


def describe_string():
    @pytest.fixture
    def string():
        return String(size=10)

    def simple_string(string):
        assert string.type == CHAR
        assert string.tag == Tag.INDEX
        assert string.width == 10

    def compare_char_array(string):
        char_array = Array(CHAR, size=10)

        assert string.type == char_array.type

    def array_of_strings(string):
        string_array: Array = Array(string, size=5)

        assert string_array.type == CHAR
        assert string_array.tag == Tag.INDEX
        assert string_array.width == 50
        assert string_array.dimensions == [10, 5]
