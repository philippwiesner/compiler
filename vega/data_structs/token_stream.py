"""Token stream implementation for lexical scanner

Tokens are placed on a queue and enriched with new data like the line number
the token has occured in the program code for better error messages.

"""

from dataclasses import dataclass
from typing import Tuple

from vega.language.token import TokenType
from vega.utils.data_types.lists import Queue


@dataclass
class Bucket:
    """Bucket to Token Stream

    Put Token and line of occurence in code into Token Stream
    """
    token: TokenType
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
        token: TokenType = bucket.token
        line: int = bucket.line
        return token, line
