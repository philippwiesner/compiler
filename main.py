from lexer.lexer import Lexer
from utils.base_types import HashTable
import random
import string

l = Lexer()

print(l.words)

print(l.words.get('true'))
print(l.words.get('char'))
print(l.words.get('if'))
print(l.words.get('while'))
print(l.words.get('break'))
print(l.words.get('do'))
print(l.words.get('bool'))
print(l.words.get('float'))
print(l.words.get('int'))
print(l.words.get('else'))
print(l.words.get('false'))