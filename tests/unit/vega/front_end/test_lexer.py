# pylint: skip-file
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

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
                word: Word = lexer._Lexer__words.get(keyword.lexeme)
                assert word == keyword

    def describe_char_retrieval():

        @pytest.mark.parametrize("code", ['ab'])
        def readch(lexer, code):
            assert lexer._Lexer__readch() is True
            assert lexer._Lexer__peek == 'a'
            assert lexer._Lexer__readch() is True
            assert lexer._Lexer__peek == 'b'
            assert lexer._Lexer__readch() is False
            assert lexer._Lexer__peek == ''

        @pytest.mark.parametrize("code", ['ab'])
        def readcch(lexer, code):
            assert lexer._Lexer__readcch('a') is True
            assert lexer._Lexer__peek == ''
            assert lexer._Lexer__readcch('a') is False
            assert lexer._Lexer__peek == 'b'

    def describe_scan_combined_tokens():

        @pytest.mark.parametrize(
            "code, first_char, second_char, word, tag",
            [
                pytest.param('!=', '!', '=', vocabulary.NE, Tag.NE, id="not_equal"),
                pytest.param('->', '-', '>', vocabulary.RETURN_TYPE, Tag.RETURN_TYPE, id="return_type"),
            ]
        )
        def combined_tokens(lexer, code, first_char, second_char, word, tag):
            lexer._Lexer__readch()
            lexer._Lexer__scan_combined_tokens(first_char, second_char, word)
            assert lexer._Lexer__token_stream.is_empty() is False
            token: Word = lexer._Lexer__token_stream.remove()
            assert token.lexeme == code
            assert token.tag == tag

        @pytest.mark.parametrize(
            "code, first_char, second_char, word",
            [
                pytest.param('>-', '>', '=', vocabulary.GE, id="greater"),
            ]
        )
        def single_token(lexer, code, first_char, second_char, word):
            lexer._Lexer__readch()
            lexer._Lexer__scan_combined_tokens(first_char, second_char, word)
            assert lexer._Lexer__token_stream.is_empty() is False
            token: Token = lexer._Lexer__token_stream.remove()
            assert token.tag == first_char

    def describe_scan_literals():

        @pytest.mark.parametrize(
            "code, indicator",
            [
                pytest.param("'a'", "'", id="char_single"),
                pytest.param('"b"', '"', id="char_double"),
                pytest.param('""', '"', id="empty"),
                pytest.param("'foobar'", "'", id="string_single"),
                pytest.param('"barfoo"', '"', id="string_double"),
                pytest.param("'a + 5'", "'", id="expression_string"),
                pytest.param("'1234", "'", id="fail_missing_closing", marks=pytest.mark.xfail)
            ]
        )
        def literals(lexer, code, indicator):
            lexer._Lexer__readch()
            lexer._Lexer__scan_literals(indicator)
            assert lexer._Lexer__token_stream.is_empty() is False
            token: Token = lexer._Lexer__token_stream.remove()
            assert token.tag == indicator
            literal: Literal = lexer._Lexer__token_stream.remove()
            assert literal.content == code[1:-1]
            assert literal.tag == Tag.LITERAL

    def describe_scan_numbers():

        @pytest.mark.parametrize(
            "code, value",
            [
                pytest.param("1", 1, id="single_number"),
                pytest.param("0030303", 30303, id="zero_leading_number"),
                pytest.param("123.54", 123.54, id="fail_float", marks=pytest.mark.xfail)
            ]
        )
        def natural_numbers(lexer, code, value):
            lexer._Lexer__readch()
            lexer._Lexer__scan_numbers()
            assert lexer._Lexer__token_stream.is_empty() is False
            token: Num = lexer._Lexer__token_stream.remove()
            assert token.tag == Tag.NUM
            assert token.value == value
