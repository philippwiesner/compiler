"""Vega compiler"""
from argparse import ArgumentParser
from argparse import FileType

from vega.front_end.parser import Parser

if __name__ == 'main':
    parser = ArgumentParser(description="Compile")
    parser.add_argument('code', type=FileType('r'))
    args = parser.parse_args()

    code = args.code

    parser = Parser(code)
    parser.parse()
