from functools import reduce
from operator import add, mul, eq

from AST import Symbol, Number, Keyword, SExpression
from proc import Procedure
from env import Env
from builtin import BuiltIn

from utils import *

# Define empty list for use in these fn definitions
nil = SExpression()

def all_type(seq, typ):
    return all(type(x) is typ for x in seq)

@builtin
@procedure
@arity(2, ...)
def plus(args, env):
    return reduce(add, args)

@builtin
@procedure
@arity(2, ...)
def minus(args, env):
    return args[0] - reduce(add, args[1:])

@builtin
@procedure
@arity(2, ...)
def times(args, env):
    return reduce(mul, args)

@builtin
@procedure
@arity(2, ...)
def divide(args, env):
    return args[0] / reduce(mul, args[1:])

@builtin
@procedure
@arity(2, ...)
def all_eq(args, env):
    return pybool_into_kwbool(reduce(eq, args))

@builtin
@procedure
@arity(1)
def head(args, env):
    return args[0].head()

@builtin
@procedure
@arity(1)
def body(args, env):
    return SExpression(*args[0].body())

@builtin
@arity(2)
def fn(args, env):
    """
    Fn[{x y z} +[x y z]]
    """

    [quote, params], body = args

    msg = "First argument must be a list of symbols"
    assert type(params) is SExpression and all_type(params, Symbol), msg

    return Procedure(formals=params, body=body, creation_env=env)

@builtin
@arity(2)
def define(args, env):

    sym, val = args

    msg = "First argument to `Def` must be a symbol"
    assert type(sym) is Symbol, msg

    env.declare(sym)
    val = val.evaluate(env)
    env[sym] = val
    return val

@builtin
@arity(2)
def defn(args, env):
    """
    Defn[f[x] x]
    """
    header, body = args

    msg = "Header of `Defn` must be a list expression"
    assert type(header) is SExpression, msg
    msg = "Header of `Defn` must only contain symbols"
    assert all_type(header, Symbol), msg
    msg = "Header of `Defn` must be non-empty"
    assert len(header) > 0, msg
    
    name, *params = header
    params = SExpression(Symbol("Quote"), SExpression(*params))
    sexpr_fn = SExpression(params, body)
    proc = fn.apply(sexpr_fn, env)

    # Call `define`, which is `def`d right above
    return define.apply(SExpression(name, proc), env)

@builtin
@arity(2)
def set_bang(args, env):
    sym, val = args
    val = val.evaluate(env)
    env[sym] = val
    return val

@builtin
@arity(1, ...)
def do(args, env):
    for arg in args[:-1]:
        arg.evaluate(env)
    return args[-1].evaluate(env)

@builtin
@arity(2)
def let(args, env):
    """
    Let[{x 12
         y 13
         z 14}
       +[x y]]
    """
    [quote, defs], body = args

    msg = "First argument of `Let` must be a list of symbol-value pairs"
    assert type(defs) is SExpression and len(defs) % 2 == 0, msg

    # Split into evens and odds
    syms, vals = defs[::2], defs[1::2]

    msg = "Non-symbols cannot be assigned to in `Let` expression"
    assert all_type(syms, Symbol), msg

    vals = [val.evaluate(env) for val in vals]

    proc = Procedure(syms, body, env)
    return proc.apply(vals)

@builtin
@procedure
@arity(1)
def eval_(args, env):
    [expr] = args
    return expr.evaluate(env)

@builtin
@procedure
@arity(2)
def apply_(args, env):
    fn, args = args

    if type(fn) is Procedure:
        return fn.apply(args)
    if type(fn) is BuiltIn:
        return fn.apply(args, env)
    else:
        raise Exception("First argument to `Apply` must evaluate to a callable type")

@builtin
@arity(1)
def quote(args, env):
    return args[0]

@builtin
@procedure
@arity(0, ...)
def list_(args, env):
    return SExpression(*args)

@builtin
@arity(3)
def if_(args, env):
    assert len(args) == 3, f"`If` takes 3 arguments, {len(args)} given"
    condition, consequent, alternative = args
    if truthy(condition.evaluate(env)):
        return consequent.evaluate(env)
    else:
        return alternative.evaluate(env)

@builtin
@arity(0, ...)
def or_(args, env):
    for arg in args:
        arg = arg.evaluate(env)
        if truthy(arg):
            return arg
    else:
        return Keyword(":F")

@builtin
@arity(0, ...)
def and_(args, env):
    for arg in args[:-1]:
        arg = arg.evaluate(env)
        if not truthy(arg):
            return arg
    else:
        return args[-1].evaluate(env)

@builtin
@procedure
@arity(1)
def not_(args, env):
    [a] = args
    return pybool_into_kwbool(not truthy(a))

@builtin
@procedure
@arity(0, ...)
def print_(args, env):
    if args:
        for arg in args:
            print(arg)
    else:
        print() # newline

    return args[-1] if args else nil

@builtin
@procedure
@arity(1)
def type_(args, env): ######### TODO: How to represent types?
    [arg] = args
    return Keyword(":" + type(arg).__name__)


@builtin
@procedure
@arity(1)
@number_map
def inc(args, env):
    [n] = args
    return n + 1

@builtin
@procedure
@arity(1)
@number_map
def dec(args, env):
    [n] = args
    return n - 1

builtins = Env(locals_={
    Symbol("Nil"):   nil,
    Symbol("+"):     plus,
    Symbol("-"):     minus,
    Symbol("*"):     times,
    Symbol("/"):     divide,
    Symbol("="):     all_eq,
    Symbol("Head"):  head,
    Symbol("Body"):  body,
    Symbol("Fn"):    fn,
    Symbol("Def"):   define,
    Symbol("Defn"):  defn,
    Symbol("Set!"):  set_bang,
    Symbol("Do"):    do,
    Symbol("Let"):   let,
    Symbol("Eval"):  eval_,
    Symbol("Apply"):  apply_,
    Symbol("Quote"): quote,
    Symbol("List"):  list_,
    Symbol("If"):    if_,
    Symbol("Or"):    or_,
    Symbol("And"):   and_,
    Symbol("Not"):   not_,
    Symbol("Print"): print_,
    Symbol("Type"):  type_,
    Symbol("Inc"):   inc,
    Symbol("Dec"):   dec,
})

