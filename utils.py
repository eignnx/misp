from AST import SExpression, BuiltIn, Keyword, Expression, Number

from functools import wraps


def builtin(f):
    return BuiltIn(f)

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

            gt = len(args) > argc
            eq = len(args) == argc

            addendum = "at least" if gt and ellipsis is ... else ""
            msg = f"Wrong number of arguments. Expected {addendum}" + \
                  f"{argc}, got {len(args)}"
            assert eq or (ellipsis is ... and gt), msg

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
        msg = f"Arguments must all be numbers: {numbers}"
        assert all(type(n) is Number for n in numbers), msg

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

