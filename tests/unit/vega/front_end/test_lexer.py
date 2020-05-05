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


class TestLexer:

    def test_initialization(self):
        with patch('builtins.open', mock_open(read_data='')) as m:
            with open('foo') as code_file:
                lexer: Lexer = Lexer(code_file)

        for keyword in vocabulary.keywords:
            word: Word = lexer._Lexer__words.get(keyword.lexeme)
            assert word == keyword

    def test_char_retrieval_from_stream(self):
        with patch('builtins.open', mock_open(read_data='ab')) as m:
            with open('foo') as code_file:
                lexer: Lexer = Lexer(code_file)

        assert lexer._Lexer__readch() is True
        assert lexer._Lexer__peek == 'a'
        assert lexer._Lexer__readch() is True
        assert lexer._Lexer__peek == 'b'
        assert lexer._Lexer__readch() is False
        assert lexer._Lexer__peek == ''

    def test_char_retrieval_validation(self):
        with patch('builtins.open', mock_open(read_data='ab')) as m:
            with open('foo') as code_file:
                lexer: Lexer = Lexer(code_file)

        assert lexer._Lexer__readcch('a') is True
        assert lexer._Lexer__peek == ''
        assert lexer._Lexer__readcch('a') is False
        assert lexer._Lexer__peek == 'b'

    @pytest.mark.parametrize(
        "code, first_char, second_char, word, tag",
        [
            ('!=', '!', '=', vocabulary.NE, Tag.NE),
            ('->', '-', '>', vocabulary.RETURN_TYPE, Tag.RETURN_TYPE),
        ]
    )
    def test_scan_combined_tokens(self, code, first_char, second_char, word, tag):
        with patch('builtins.open', mock_open(read_data=code)) as m:
            with open('foo') as code_file:
                lexer: Lexer = Lexer(code_file)

        lexer._Lexer__readch()
        lexer._Lexer__scan_combined_tokens(first_char, second_char, word)
        assert lexer._Lexer__token_stream.is_empty() is False
        token: Word = lexer._Lexer__token_stream.remove()
        assert token.lexeme == code
        assert token.tag == tag

    @pytest.mark.parametrize(
        "code, first_char, second_char, word",
        [
            ('>-', '>', '=', vocabulary.GE),
        ]
    )
    def test_scan_combined_tokens_single_token(self, code, first_char, second_char, word):
        with patch('builtins.open', mock_open(read_data=code)) as m:
            with open('foo') as code_file:
                lexer = Lexer(code_file)

        lexer._Lexer__readch()
        lexer._Lexer__scan_combined_tokens(first_char, second_char, word)
        assert lexer._Lexer__token_stream.is_empty() is False
        token: Token = lexer._Lexer__token_stream.remove()
        assert token.tag == first_char

    @pytest.mark.parametrize(
        "code, indicator",
        [
            ("'a'", "'"),
            ('"b"', '"'),
            ('""', '"'),
            ("'foobar'", "'"),
            ('"barfoo"', '"'),
            ("'a + 5'", "'")
        ]
    )
    def test_scan_literals(self, code, indicator):
        with patch('builtins.open', mock_open(read_data=code)) as m:
            with open('foo') as code_file:
                lexer = Lexer(code_file)

        lexer._Lexer__readch()
        lexer._Lexer__scan_literals(indicator)
        assert lexer._Lexer__token_stream.is_empty() is False
        token: Token = lexer._Lexer__token_stream.remove()
        assert token.tag == indicator
        literal: Literal = lexer._Lexer__token_stream.remove()
        assert literal.content == code[1:-1]
        assert literal.tag == Tag.LITERAL
