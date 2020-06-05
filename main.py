"""Vega compiler"""
from argparse import ArgumentParser
from argparse import FileType

from vega.front_end.parser import Parser
from vega.front_end.exception import BaseError

if __name__ == "__main__":
    parser = ArgumentParser(description="Compile")
    parser.add_argument('code', type=FileType('r'))
    args = parser.parse_args()

    code = args.code

    parser = Parser(code)
    try:
        parser.parse()
    except BaseError as e:
        print(e.message)
