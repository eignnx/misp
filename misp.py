#!/usr/bin/python3.6

import argparse as ap

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
    argparser = ap.ArgumentParser(prog="misp", description="Executes misp code")
    argparser.add_argument("filename", nargs="?")
    argparser.add_argument(
        "-a", "--ast", action="store_true",
        help="prints out the syntax tree of the given expression"
    )
    argparser.add_argument(
        "-i", "--interactive", action="store_true",
        help="runs the code in file `filename`, then opens repl"
    )

    args = argparser.parse_args()

    if args.filename:
        with open(args.filename, "r") as f:
            source = "".join(f)
            evaluate(source, args.ast)

    if args.interactive or args.filename is None:
        while True:
            source = input("::> ")
            evaluate(source, args.ast)
