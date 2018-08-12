from sly import Lexer
from decimal import Decimal

class Lexer(Lexer):
    tokens = {
        SEP, PIPE, NAME,
        NUM, STR,
        QUOTE,
        LPAREN, RPAREN,
        LBRACK, RBRACK,
        LBRACE, RBRACE
    }
    
    SEP = r"\s+"
    PIPE = r"\|\|"
    NAME = r"[a-zA-Z\-+*\/=<>][a-zA-Z0-9_\-=<>]*['!?]*"
    
    NUM = r"[\-]?\d+\.?\d*|\.\d+"
    STR = r'("[^"]*")'

    QUOTE = r"'"

    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACK = r"\["
    RBRACK = r"\]"
    LBRACE = r"\{"
    RBRACE = r"\}"

    def NUM(self, t):
        t.value = Decimal(t.value)
        return t

    def STR(self, t):
        t.value = t.value[1:-1]
        return t


if __name__ == "__main__":
    lex = Lexer()

    def lexit(txt):
        for tok in lex.tokenize(txt):
            print(tok)

