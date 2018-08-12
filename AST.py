from functools import reduce
import operator
from decimal import Decimal
from immutable_map import immutable_map, immutable_add

INDENT_SPACES = 4

def evaluate_with(env):
    """
    Produces an evaluator fn that can be used with
    higher-order functions.

    Ex:
        evaluated = map(evaluate_with(env), to_evaluate)
    """
    def evaluator(expr):
        return expr.evaluate(env)
    return evaluator

def sums(args, env):
    return sum(arg.evaluate(env) for arg in args)

def diffs(args, env):
    (first, *rest) = map(evaluate_with(env), args)
    return first - sum(rest)

def prod(args, env):
    args = list(map(evaluate_with(env), args))
    return reduce(operator.mul, args, Decimal(1))

def divs(args, env):
    args = map(evaluate_with(env), args)
    return reduce(operator.truediv, args[1:], args[0])

def all_eq(args, env):
    (first, *rest) = map(evaluate_with(env), args)
    for arg in rest:
        if first != arg:
            return False
    return True

def Fn(args, env):
    (formal_args, body) = args

    def procedure_obj(actual_args, env):
        actual_args = map(evaluate_with(env), actual_args)
        new_pairs = dict(zip(formal_args, actual_args))
        new_env = immutable_add(new_pairs, env)
        return body.evaluate(new_env)

    return procedure_obj


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
        return self.value

class Symbol(Atom):
    def evaluate(self, env):
        try:
            return env[self]
        except KeyError:
            return self
            #print()
            #print("Uh-oh. Lemme dump the env...")
            #print()
            #for k, v in env.items():
            #    print(repr(k), "->", v, sep="\t")
            #print()
            #msg = "I don't recognize '{}' as a name".format(self.value)
            #raise NameError(msg)

class Number(Atom):
    pass

class String(Atom):
    def __str__(self):
        return repr(self.value)


class SExpression(Expression):
    def __init__(self, *values):
        self.values = values

    def __str__(self):
        return "'({})".format(", ".join(str(v) for v in self.values))

    def __repr__(self):
        return self.tree_repr()

    def __iter__(self):
        return iter(self.values)
    
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
        if isinstance(self.head(), Symbol):
            (operator, *operands) = self.values
            operator = operator.evaluate(env)
            try:
                return operator(operands, env)
            except TypeError:
                print("Almost got a type error...")
                return self

        elif isinstance(self.head(), SExpression):
            evaluated_fn = self.head().evaluate(env)
            new_self = SExpression(evaluated_fn, *self.body())
            return new_self.evaluate(env)

        elif type(self.head()) is type(Fn):
            return self.head()(self.body(), env)

        else:
            return self
            #msg = "I can't call '{}' like a function"
            #msg = msg.format(type(self.head()))
            #raise TypeError(msg)

class List(SExpression):

    def __str__(self):
        return "{{{}}}".format(", ".join(str(v) for v in self.values))

    def evaluate(self, env):
        return List(*map(evaluate_with(env), self.values))

class Quoted(SExpression):

    def evaluate(self, env):
        return self


builtins = immutable_map({
    Symbol("+"): sums,
    Symbol("-"): diffs,
    Symbol("*"): prod,
    Symbol("/"): divs,
    Symbol("="): all_eq,
    Symbol("Head"): lambda args: args[0],
    Symbol("Body"): lambda args: args[1:],
    Symbol("Fn"): Fn,
})
