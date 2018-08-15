from sly import Parser
from lexer import Lexer
import AST

class Parser(Parser):
    tokens = Lexer.tokens

#    @_("expression")
#    def program(self, p):
#        return p.expression

    @_("expressions")
    def program(self, p):
        return p.expressions
    
    @_("LPAREN expressions RPAREN")
    def paren_expression(self, p):
        return AST.SExpression(*p.expressions)

    @_("LPAREN RPAREN")
    def paren_expression(self, p):
        return AST.SExpression()

    @_("expression LBRACK RBRACK")
    def brack_expression(self, p):
        return AST.SExpression(p.expression)

    @_("expression LBRACK expressions RBRACK",
       "LBRACK expressions PIPE expression RBRACK")
    def brack_expression(self, p):
        return AST.SExpression(p.expression, *p.expressions)

    @_("LBRACE expressions RBRACE")
    def brace_expression(self, p):
        return AST.SExpression(AST.Symbol("List"), *p.expressions)

    @_("LBRACE RBRACE")
    def brace_expression(self, p):
        return AST.SExpression(AST.Symbol("List"))

    @_("QUOTE expression")
    def quoted_expression(self, p):
        return AST.SExpression(AST.Symbol("Quote"), p.expression)

    @_("expressions expression")
    def expressions(self, p):
        return p.expressions + [p.expression]

    @_("expression")
    def expressions(self, p):
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

    @_("KEYWORD")
    def expression(self, p):
        return AST.Keyword(p.KEYWORD)
    
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


