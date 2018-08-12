from functools import reduce
from env import Env
from decimal import Decimal

INDENT_SPACES = 4


class Expression:
    def __eq__(self, other):
        if not isinstance(other, Expression):
            return False
        return (type(self) == type(other)) and \
            (self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not (self == other)

    def evaluate(self, env):
        raise NotImplementedError()

class Atom(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value if type(self.value) is str else str(self.value)

    def __repr__(self):
        return self.tree_repr()

    def __hash__(self):
        return self.value.__hash__()

    def tree_repr(self, level=0):
        class_name = self.__class__.__name__
        return "{indent}{}({})".format(
            class_name,
            str(self),
            indent=(" " * INDENT_SPACES * level))

    def evaluate(self, env):
        return self

class Symbol(Atom):
    def evaluate(self, env):
        return env[self]

class Number(Atom):
    def __add__(self, other):
        return Number(self.value + other.value)

    def __sub__(self, other):
        return Number(self.value - other.value)

    def __mul__(self, other):
        return Number(self.value * other.value)

    def __truediv__(self, other):
        return Number(self.value / other.value)

    def __mod__(self, other):
        return Number(self.value % other.value)

    def __pow__(self, other):
        return Number(self.value ** other.value)

class String(Atom):
    def __str__(self):
        return repr(self.value)

from proc import Procedure
from builtin import BuiltIn

class SExpression(Expression):
    def __init__(self, *values):
        self.values = values

    def __str__(self):
        return "'({})".format(" ".join(str(v) for v in self.values))

    def __repr__(self):
        return self.tree_repr()

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, i):
        return self.values[i]
    
    def tree_repr(self, level=0):
        class_name = self.__class__.__name__
        level_str = lambda child: child.tree_repr(level+1)
        children = (level_str(child) for child in self.values)
        return "{indent}{}(\n{}\n{indent})".format(
            class_name,
            ",\n".join(children),
            indent=(" " * INDENT_SPACES * level))

    def head(self):
        return self.values[0]

    def body(self):
        return self.values[1:]

    def evaluate(self, env):

        head, *body = self.values
        body = SExpression(*body)

        if isinstance(head, Symbol):
            res = head.evaluate(env)
            return SExpression(res, *body).evaluate(env)

        elif isinstance(head, SExpression):
            res = head.evaluate(env)
            return SExpression(res, *body).evaluate(env)

        elif type(head) is Procedure:
            args = body.evaluate(env)
            return head.apply(args)

        elif type(head) is BuiltIn:
            return head.apply(body, env)

        else:
            return self

