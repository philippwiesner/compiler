from argparse import ArgumentParser
from argparse import FileType

from vega.front_end.lexer import Lexer

if __name__ == 'main':
    parser = ArgumentParser(description="Compile")
    parser.add_argument('code', type=FileType('r'))
    args = parser.parse_args()

    code = args.code

    lexer = Lexer(code)
    token_stream = lexer.scan()
