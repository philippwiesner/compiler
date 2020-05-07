# pylint: skip-file
from typing import Union
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from vega.utils.data_types.lists import Queue
from vega.front_end.lexer import Lexer
from vega.language import vocabulary
from vega.language.token import Literal
from vega.language.token import Tag
from vega.language.token import Token
from vega.language.token import Word
from vega.language.token import Num
from vega.language.token import Real


def describe_lexer():

    @pytest.fixture
    def lexer(code):
        with patch('builtins.open', mock_open(read_data=code)) as m:
            with open('foo') as code_file:
                lexer: Lexer = Lexer(code_file)
        return lexer

    def describe_initialization():

        @pytest.mark.parametrize("code", [''])
        def initialize(lexer, code):
            for keyword in vocabulary.keywords:
                word: Word = lexer.words.get(keyword.lexeme)
                assert word == keyword

    def describe_scan():

        @pytest.mark.parametrize(
            "code, tag",
            [
                pytest.param('!=', Tag.NE, id="not_equal"),
                pytest.param('->', Tag.RETURN_TYPE, id="return_type"),
            ]
        )
        def combined_tokens(lexer, code, tag):
            token_stream: Queue = lexer.scan()

            assert token_stream.is_empty() is False
            token: Word = token_stream.remove()
            assert token.lexeme == code
            assert token.tag == tag

        @pytest.mark.parametrize(
            "code, recognized_tokens",
            [
                pytest.param('>-', ['>', '-'], id="greater"),
            ]
        )
        def single_token(lexer, code, recognized_tokens):
            token_stream: Queue = lexer.scan()

            assert token_stream.is_empty() is False

            for recognized_token in recognized_tokens:
                token: Token = token_stream.remove()
                assert token.tag == recognized_token

        @pytest.mark.parametrize(
            "code, indicator, literal",
            [
                pytest.param("'a'", "'", 'a', id="char_single"),
                pytest.param('"b"', '"', 'b', id="char_double"),
                pytest.param('""', '"', '', id="empty"),
                pytest.param("'foobar'", "'", 'foobar', id="string_single"),
                pytest.param('"barfoo"', '"', 'barfoo', id="string_double"),
                pytest.param("'a + 5'", "'", 'a + 5', id="expression_string"),
                pytest.param("'1234", "'", '1234', id="fail_missing_closing", marks=pytest.mark.xfail)
            ]
        )
        def literals(lexer, code, indicator, literal):
            token_stream: Queue = lexer.scan()
            assert token_stream.is_empty() is False
            assert len(token_stream) == 3

            start_indicator_token: Token = token_stream.remove()
            assert start_indicator_token.tag == indicator

            literal_token: Literal = token_stream.remove()
            assert literal_token.content == literal
            assert literal_token.tag == Tag.LITERAL

            end_indicator_token: Token = token_stream.remove()
            assert end_indicator_token.tag == indicator

        @pytest.mark.parametrize(
            "code, value",
            [
                pytest.param("0", 0, id="zero"),
                pytest.param("1", 1, id="single_number"),
                pytest.param("0030303", 30303, id="zero_leading_number"),
                pytest.param("123.54", 123.54, id="normal_fraction"),
                pytest.param("0.543456", 0.543456, id="zero_fraction"),
            ]
        )
        def numbers(lexer, code, value):
            token_stream: Queue = lexer.scan()
            assert token_stream.is_empty() is False

            token: Union[Num, Real] = token_stream.remove()
            assert token.tag == Tag.NUM or token.tag == Tag.REAL
            assert token.value == pytest.approx(value)
