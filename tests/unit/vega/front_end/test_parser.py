# pylint: skip-file
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from vega.front_end.parser import Parser


def describe_parser():
    @pytest.fixture
    def parser(code):
        with patch('builtins.open', mock_open(read_data=code)):
            with open('foo') as code_file:
                parser: Parser = Parser(code_file)
        return parser

    def describe_parsing():

        @pytest.mark.parametrize("code", [
            pytest.param("""
func foobar(k: float, i: int, g: int = 6) -> float {
    while (true) {
        while (k[i] <= g) {
            i = i + 1;
        }
        k[i] = 32 + 5 * 6;
        if (not -5 < 6) {
            k[1] = k[2] * 6;
            k[3] = 7;
        }
        if (not True and not (True or False)) {
        pass;
        }
    }
    return k;
}

func main() -> int {
    i: const int = 5;
    k, l: float = 0;
    m: str = "Hello World";
    n: char = 'g';
    j: int[5] = [1, 2, 3, 4, 5];
    l = foobar(1.2, i);
}

""", id="full_example")
        ])
        def vega_code(parser, code):
            parser.parse()
