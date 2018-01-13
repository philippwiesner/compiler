from lexer.lexer import Lexer
from argparse import ArgumentParser, FileType

parser = ArgumentParser(description="Compile")
parser.add_argument('code', type=FileType('r'))
args = parser.parse_args()

code = args.code

l = Lexer(code)

while True:
    l.scan()
