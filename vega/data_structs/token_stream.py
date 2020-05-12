from dataclasses import dataclass
from typing import Tuple

from vega.utils.data_types.lists import Queue
from vega.language.token import TokenType


@dataclass
class Bucket:
    """Bucket to Token Stream

    Put Token and line of occurence in code into Token Stream
    """
    data: TokenType
    line: int


class TokenStream(Queue):
    """Stream of Tokens

    Store Tokens in order of occurrence
    """

    def add(self, data: TokenType, *args, **kwargs) -> None:
        """Add Token to stream

        Args:
            data: Token to store
            line: line number in code
        """
        line: int = kwargs.pop('line')
        super().add(Bucket(data, line), **kwargs)

    def remove(self) -> Tuple[TokenType, int]:
        """Remove object from stream

        Returns:
            Tuple of Token and line number
        """
        bucket: Bucket = super().remove()
        data: TokenType = bucket.data
        line: int = bucket.line
        return data, line
