"""Implements lexical scanner for Vega language

"""
from io import TextIOWrapper

from vega.language import vocabulary
from vega.language.token import Literal
from vega.language.token import Num
from vega.language.token import Real
from vega.language.token import Tag
from vega.language.token import Token
from vega.language.token import Word
from vega.utils.data_types.hash_table import HashTable
from vega.utils.data_types.lists import Queue


# pylint: disable=too-few-public-methods
class Lexer:
    """Lexer class"""

    def __init__(self, code: TextIOWrapper) -> None:
        """On lexer initialization create hash table
        with keywords for easier matching

        Args:
            code: vega program code
        """
        self.__line: int = 1
        self.__peek: str = ''
        self.__code: TextIOWrapper = code
        self.__token_stream: Queue = Queue()
        self.__words: HashTable = HashTable()
        for keyword in vocabulary.keywords:
            self.__words.put(keyword.lexeme, keyword)

    @property
    def words(self) -> HashTable:
        """Word property

        Returns:
            hash table of stored keywords and identifiers

        """
        return self.__words

    def __readch(self) -> bool:
        """Read next char from code stream

        Read char from code stream and write to attribute ``__peek``

        Returns:
            True when char left on input stream, False otherwise
        """
        self.__peek = self.__code.read(1)
        if len(self.__peek) == 0:
            return False
        return True

    def __readcch(self, char: str) -> bool:
        """Read next char from code stream and validate against ``c``

        Args:
            c: char to validate

        Returns:
            True when c matches, False otherwise
        """
        self.__readch()
        if self.__peek != char:
            return False
        self.__peek = ''
        return True

    def __scan_combined_tokens(self, first_sign: str, second_sign: str,
                               word: Word) -> None:
        """Scan for combined tokens like '!=' or '=='

        Args:
            first_sign: first token char
            second_sign: second token char
            word: word to add to token stream for combined token

        Returns:

        """
        if self.__peek == first_sign:
            if self.__readcch(second_sign):
                self.__token_stream.add(word)
            else:
                self.__token_stream.add(Token(first_sign))

    def __scan_literals(self, indicator: str) -> None:
        """Scan for literals

        Add literals like char or strings to token stream

        Args:
            indicator: literal indicator for chars and strings

        Returns:

        """
        if self.__peek == indicator:
            string: str = ''
            self.__token_stream.add(Token(indicator))
            self.__readch()
            eof: bool = True
            while self.__peek != indicator and eof:
                string += self.__peek
                eof = self.__readch()
            self.__token_stream.add(Literal(string))

    def __scan_numbers(self) -> None:
        """Scan for numbers

        Add natural or real numbers to token stream

        Returns:

        """
        if self.__peek.isdecimal():
            value: int = 0
            while self.__peek.isdecimal():
                value = 10 * value + int(self.__peek)
                self.__readch()
            if self.__peek != '.':
                self.__token_stream.add(Num(value))
                return
            real: float = value
            fraction: float = 10
            self.__readch()
            while self.__peek.isdecimal():
                real = real + int(self.__peek) / fraction
                fraction *= 10
                self.__readch()
            self.__token_stream.add(Real(real))

    def __scan_words(self) -> None:
        """Scan for words

        Add words (keywords or identifier) to token stream

        Returns:

        """
        if self.__peek.isalpha():
            string: str = ''
            while self.__peek.isalnum():
                string += self.__peek
                self.__readch()
            lookup: Word = self.__words.get(string)
            if lookup is not None:
                self.__token_stream.add(lookup)
                return
            word = Word(string, Tag.ID)
            self.__words.put(string, word)
            self.__token_stream.add(word)

    def __skip_whitespace(self):
        return bool(self.__peek in [' ', '', '\t'])

    def scan(self) -> Queue:
        """lexical scan method

        Scan code for tokens and add them to token stream

        Returns:
            Queue: token stream for parsing
        """
        while self.__readch():
            self.__scan_combined_tokens('&', '&', vocabulary.AND)
            self.__scan_combined_tokens('|', '|', vocabulary.OR)
            self.__scan_combined_tokens('=', '=', vocabulary.EQ)
            self.__scan_combined_tokens('!', '=', vocabulary.NE)
            self.__scan_combined_tokens('<', '=', vocabulary.LE)
            self.__scan_combined_tokens('>', '=', vocabulary.GE)
            self.__scan_combined_tokens('-', '>', vocabulary.RETURN_TYPE)
            self.__scan_literals("'")
            self.__scan_literals('"')
            self.__scan_numbers()
            self.__scan_words()
            # text control characters
            if self.__skip_whitespace():
                continue
            elif self.__peek == '\n' or self.__peek == '\r':
                self.__line += 1
                continue
            # Add remaining tokens
            self.__token_stream.add(Token(self.__peek))

        return self.__token_stream
