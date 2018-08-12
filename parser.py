from sly import Parser
from lexer import Lexer
import AST

class Parser(Parser):
    tokens = Lexer.tokens

    @_("expression")
    def program(self, p):
        return p.expression
    
    @_("LPAREN args RPAREN")
    def paren_expression(self, p):
        return AST.SExpression(*p.args)

    @_("LPAREN RPAREN")
    def paren_expression(self, p):
        return AST.SExpression()

    @_("expression LBRACK args RBRACK",
       "LBRACK args PIPE expression RBRACK",
       "LBRACK args SEP PIPE expression RBRACK",
       "LBRACK args PIPE SEP expression RBRACK",
       "LBRACK args SEP PIPE SEP expression RBRACK")
    def brack_expression(self, p):
        return AST.SExpression(p.expression, *p.args)

    @_("LBRACE args RBRACE")
    def brace_expression(self, p):
        return AST.List(*p.args)

    @_("LBRACE RBRACE")
    def brace_expression(self, p):
        return AST.List()

    @_("QUOTE expression")
    def quoted_expression(self, p):
        return AST.Quoted(*p.expression)

    @_("args SEP expression")
    def args(self, p):
        return p.args + [p.expression]

    @_("expression")
    def args(self, p):
        return [p.expression]

    @_("NUM")
    def expression(self, p):
        return AST.Number(p.NUM)
    
    @_("NAME")
    def expression(self, p):
        return AST.Symbol(p.NAME)
    
    @_("STR")
    def expression(self, p):
        return AST.String(p.STR)
    
    @_("brack_expression")
    def expression(self, p):
        return p.brack_expression

    @_("paren_expression")
    def expression(self, p):
        return p.paren_expression

    @_("brace_expression")
    def expression(self, p):
        return p.brace_expression

    @_("quoted_expression")
    def expression(self, p):
        return p.quoted_expression

    precedence = [
        ("right", QUOTE),
        ("right", PIPE),
        ("left", LBRACK),
    ]

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser()

    def parse(txt):
        return parser.parse(lexer.tokenize(txt))


