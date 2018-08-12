import AST
from misp import environment, evaluate
from decimal import Decimal

def fn_type(): pass

def EVAL(source, env=environment):
    return evaluate(source, env)

def test_fn_creation():
    res = EVAL("Fn[{x} *[x x]]")
    assert type(res) is type(fn_type)

def test_single_arg_fn_application():
    assert EVAL("Fn[{x} *[x x]][12]") == Decimal(144)

def test_number_expr_eval():
    assert EVAL("3.14159") == Decimal('3.14159')

def test_string_expr_eval():
    assert EVAL('"This is some text"') == "This is some text"

def test_addition():
    assert EVAL("+[1 2]") == Decimal(3)
    assert EVAL("+[1 2 3]") == Decimal(6)

def test_subtraction():
    assert EVAL("-[10 9]") == Decimal(1)
    assert EVAL("-[1 2 3]") == Decimal(-4)

def test_multiplication():
    assert EVAL("*[10 3]") == Decimal(30)
    assert EVAL("*[0.1 10 3]") == Decimal(3)

def test_division():
    assert EVAL("/[100 10]") == Decimal(10)
    assert EVAL("/[10 5 2]") == Decimal(1)

def test_equal():
    assert EVAL("=[4 +[2 2]]")
    assert EVAL("=[4 +[2 2] *[2 2]]")
    assert not EVAL("=[7 3]")
    assert not EVAL("=[3 3 100]")

def test_postfix_fn_application():
    assert EVAL("+[1 2 3]") == EVAL("[1 2 3||+]")
    assert EVAL("Fn[{x} *[x x]][12]") == EVAL("[12||Fn[{x} *[x x]]]")

def test_classic_lisp_fn_application():
    assert EVAL("+[1 2 3]") == EVAL("(+ 1 2 3)")
    assert EVAL("Fn[{x} *[x x]][12]") == EVAL("((Fn {x} (* x x)) 12)")



