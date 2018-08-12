#!/usr/bin/python3.6

from parser import Parser
from lexer import Lexer
import AST

parser = Parser()
lexer = Lexer()

environment = AST.builtins

def evaluate(source, debug=True):
    source = source.strip()
    ast = parser.parse(lexer.tokenize(source))
    if debug:
        print()
        print(repr(ast))
        print()
    res = ast.evaluate(environment)
    print(">", res)


if __name__ == "__main__":
    while True:
        source = input("::> ")
        evaluate(source)
