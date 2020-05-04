from io import TextIOWrapper
from vega.utils.data_types.hashTable import HashTable
from vega.utils.data_types.lists import Queue
from vega.language.token import Token, Word, Num, Real, Literal, Tag
from vega.language import vocabulary


class Lexer:

    def __init__(self, code: TextIOWrapper) -> None:
        self.__line: int = 1
        self.__peek: ''
        self.__code: TextIOWrapper = code
        self.__token_stream: Queue = Queue()
        self.__words: HashTable = HashTable()
        for keyword in vocabulary.keywords:
            self.__words.put(keyword.lexeme, keyword)

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

    def __readcch(self, c: str) -> bool:
        """Read next char from code stream and validate against ``c``

        Args:
            c: char to validate

        Returns:
            True when c matches, False otherwise
        """
        self.__readch()
        if self.__peek != c:
            return False
        self.__peek = ''
        return True

    def __scan_combined_tokens(self, first_sign: str, second_sign: str, word: Word) -> None:
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
            s: str = ''
            self.__token_stream.add(Token(indicator))
            while self.__peek != indicator:
                s += self.__peek
                self.__readch()
            self.__token_stream.add(Literal(s))

    def __scan_numbers(self) -> None:
        """Scan for numbers

        Add natural or real numbers to token stream

        Returns:

        """
        if self.__peek.isdecimal():
            v: int = 0
            while self.__peek.isdecimal():
                v = 10 * v + int(self.__peek)
                self.__readch()
            if self.__peek != '.':
                self.__token_stream.add(Num(v))
                return None
            x: float = v
            d: float = 10
            self.__readch()
            while self.__peek.isdecimal():
                x = x + int(self.__peek) / d
                d *= 10
                self.__readch()
            self.__token_stream.add(Real(x))

    def __scan_words(self) -> None:
        """Scan for words

        Add words (keywords or identifier) to token stream

        Returns:

        """
        if self.__peek.isalpha():
            s: str = ''
            while self.__peek.isalnum():
                s += self.__peek
                self.__readch()
            lookup: Word = self.__words.get(s)
            if lookup is not None:
                self.__token_stream.add(lookup)
                return None
            w = Word(s, Tag.ID)
            self.__words.put(s, w)
            self.__token_stream.add(w)

    def scan(self) -> Queue:
        """lexical scan method

        Scan code for tokens and add them to token stream

        Returns:

        """
        while self.__readch():
            # text control characters
            if self.__peek == ' ' or self.__peek == '\t':
                continue
            elif self.__peek == '\n' or self.__peek == '\r':
                self.__line += 1
            else:
                self.__scan_combined_tokens('&', '&', vocabulary.AND)
                self.__scan_combined_tokens('|', '|', vocabulary.OR)
                self.__scan_combined_tokens('=', '=', vocabulary.EQ)
                self.__scan_combined_tokens('!', '=', vocabulary.NE)
                self.__scan_combined_tokens('<', '=', vocabulary.LE)
                self.__scan_combined_tokens('>', '=', vocabulary.GE)
                self.__scan_combined_tokens('-', '>', vocabulary.RETURN_TYPE)
                self.__scan_literals('\'')
                self.__scan_literals('"')
                self.__scan_numbers()
                self.__scan_words()
                # Add remaining tokens
                self.__token_stream.add(Token(self.__peek))

        return self.__token_stream