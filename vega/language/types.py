"""Vega language types

Representation of vega variable types

The following variable types are defined here:

Basic Types: INT, FLOAT, CHAR, BOOL
Complex Types: Array, String

"""
from typing import List

from vega.language.token import Tag
from vega.language.token import Word


class Type(Word):
    """Simple type

    Simple or basic variable types are integers, floating point numbers, chars
    or boolean values.

    Each of them can be created after reading the correct keyword and uses a
    pre defined amount of memory space.

    """

    def __init__(self, var_type: str, tag: Tag, width: int) -> None:
        """Create new variable type

        Args:
            var_type: variable type
            tag: type tag (used to differ between basic and more complex types)
            width: memory width
        """
        super().__init__(var_type, tag)
        self.__width: int = width

    @property
    def width(self) -> int:
        """Width property

        Returns:
            memory width of type
        """
        return self.__width


INT = Type("int", Tag.BASIC, 4)
FLOAT = Type("float", Tag.BASIC, 8)
CHAR = Type("char", Tag.BASIC, 1)
BOOL = Type("bool", Tag.BASIC, 1)


class Array(Type):
    """Array type

    Arrays are a more complex type as they are defined by a basic type and
    a size of number of elements to be stored in the array. Arrays can also be
    nested.

    """

    def __init__(self, var_type: Type, **kwargs) -> None:
        """Create new array

        When a new array is created the size of the array is stored
        alongside the amount of memory to be allocated for storing the
        number of elements of the array type. For nested elements each array
        size is stored in a list to be able to compare nested arrays with each
        other.

        Args:
            var_type: array type (basic types, another array)
            **kwargs: size of the array
        """
        self.__size: int = kwargs.get('size', 0)
        self.__dimensions: List = [self.__size]
        self.__type: Type = var_type
        if isinstance(var_type, Array):
            self.__dimensions = var_type.dimensions + self.__dimensions
            self.__type = var_type.type
        super().__init__('[]',
                         Tag.INDEX,
                         self.__size * var_type.width)

    @property
    def dimensions(self) -> List:
        """Dimension property

        Returns:
            list of array dimensions
        """
        return self.__dimensions

    @property
    def type(self) -> Type:
        """Array type property

        Returns:
            basic array type (INT, CHAR, BOOL, FLOAT)
        """
        return self.__type

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.type}{self.dimensions!r})'

    def __str__(self) -> str:
        return f'{self.type}{self.dimensions}'


class String(Array):
    """String Type

    Basically Strings are just char arrays. Therefore we only create a new
    array with the CHAR base type.

    """

    def __init__(self, **kwargs):
        """Create char array"""
        super().__init__(CHAR, **kwargs)
