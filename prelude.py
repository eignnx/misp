from functools import reduce
from operator import add, mul, eq

from AST import Symbol, Number, SExpression
from proc import Procedure
from env import Env
from builtin import BuiltIn

def builtin(f):
    return BuiltIn(f)

def procedure(f):
    def wrapper(args, env):
        args = [a.evaluate(env) for a in args]
        return f(args, env)
    return wrapper

def all_type(seq, typ):
    return all(type(x) is typ for x in seq)

@builtin
@procedure
def plus(args, env):
    return reduce(add, args)

@builtin
@procedure
def minus(args, env):
    return args[0] - reduce(add, args[1:])

@builtin
@procedure
def times(args, env):
    return reduce(mul, args)

@builtin
@procedure
def divide(args, env):
    return args[0] / reduce(mul, args[1:])

@builtin
@procedure
def all_eq(args, env):
    return reduce(eq, args)

@builtin
@procedure
def head(args, env):
    return args[0]

@builtin
@procedure
def body(args, env):
    return SExperession(args[1:])

@builtin
def fn(args, env):
    if len(args) != 2:
        raise Error("Wrong number of arguments to `Fn`")

    params, body = args

    if type(params) is not SExpression or not all_type(params, Symbol):
        raise Error("First argument must be a list of symbols")

    return Procedure(formals=params, body=body, creation_env=env)

@builtin
def define(args, env):
    if len(args) != 2:
        raise Error("`Def` requires exactly 2 arguments")

    new_def, value = args

    if type(new_def) is not Symbol:
        raise Error("First argument to `Def` must be a symbol")

    sym = new_def
    env.declare(sym)
    env[sym] = value.evaluate(env)
    return None

@builtin
def defn(args, env):
    header, body = args
    assert type(header) is SExpression, "Header of `Defn` must be a list expression"
    assert all_type(header, Symbol), "Header of `Defn` must only contain symbols"
    assert len(header) > 0, "Header of `Defn` must be non-empty"
    
    name, *params = header
    params = SExpression(*params)
    sexpr_fn = SExpression(params, body)
    proc = fn.apply(sexpr_fn, env)
    return define.apply(SExpression(name, proc), env)

@builtin
def quote(args, env):
    return args

@builtin
def if_(args, env):
    assert len(args) == 3, f"`If` takes 3 arguments, {len(args)} given"
    condition, consequent, alternative = args
    if condition:
        return consequent.evaluate(env)
    else:
        return alternative.evaluate(env)

builtins = Env(locals_={
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
    Symbol("Quote"): quote,
    Symbol("If"):    if_,
})

