from AST import SExpression, BuiltIn, Keyword, Expression, Number, Symbol
from env import Env

from functools import wraps

FLAG = "misp_intermediate_fn"

def builtin(f):
    named = FLAG in f.__dict__.keys()
    return BuiltIn(f, name=f.__name__ if named else None)

def named(name):
    """
    Changes the name of the decorated function
    """
    def decorated_fn(f):
        f.__name__ = name
        f.__dict__[FLAG] = True
        return f
    return decorated_fn

def procedure(f):
    @wraps(f)
    def wrapper(args, env):
        args = [a.evaluate(env) for a in args]
        return f(args, env)
    return wrapper

def arity(argc, ellipsis=None):
    def decorated_fn(f):
        @wraps(f)
        def wrapper(args, env):

            lt = len(args) < argc
            gt = len(args) > argc
            eq = len(args) == argc

            if not eq and (ellipsis is not ... or not gt):
                addendum = "at least " if lt and ellipsis is ... else ""
                msg = f"Wrong number of arguments to `{f.__name__}`. " + \
                      f"Expected {addendum}{argc}, got {len(args)}"
                raise AssertionError(msg)

            return f(args, env)
        return wrapper
    return decorated_fn

def number_map(f):
    """
    Decorator that accepts a function with signature:
        *PythonNumber -> PythonNumber
    Returns a function with signature:
        *Number -> Number
    """
    @wraps(f)
    def wrapper(args, env):
        numbers = args

        if any(type(n) is not Number for n in numbers):
            msg = f"Arguments to `{f.__name__}` must all be numbers: {numbers}"
            raise AssertionError(msg)

        numbers = [n.value for n in numbers]
        py_num = f(numbers, env)
        
        return Number(py_num)
    return wrapper

def truthy(expr: Expression) -> bool:
    non_null = not expr == SExpression()
    non_false = not expr == Keyword(":F")
    return non_null and non_false

def pybool_into_kwbool(e: bool) -> Keyword:
    if e:
        return Keyword(":T")
    else:
        return Keyword(":F")

def expr_into_kwbool(e: Expression) -> Keyword:
    if truthy(e):
        return Keyword(":T")
    else:
        return Keyword(":F")


def collect_builtins(locs):
    builtins = { Symbol(b.name): b for b in locs.values() if type(b) is BuiltIn }
    return Env(parent=None, locals_=builtins)
