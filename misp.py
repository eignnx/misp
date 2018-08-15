#!/usr/bin/python3.6

import argparse as ap

from parser import Parser
from lexer import Lexer
import AST
import prelude

parser = Parser()
lexer = Lexer()

environment = prelude.builtins

def evaluate(source, debug=True):
    source = source.strip()
    ast_list = parser.parse(lexer.tokenize(source))
    for ast in ast_list:
        if debug:
            print()
            print(repr(ast))
            print()
        try:
            res = ast.evaluate(environment)
            print("-->", str(res))
        except Exception as e:
            print("ERROR:", str(e))


if __name__ == "__main__":
    argparser = ap.ArgumentParser(
        prog="misp",
        description="Executes misp code"
    )
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
            try:
                source = input("::> ")
            except EOFError:
                print("\nExiting...")
                break
            if source:
                evaluate(source, args.ast)
