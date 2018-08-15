# misp
An M-expression-based Lisp descendant implemented on top of Python3.6 and SLY

## Code Example
Misp supports both the Lisp-like S-expression syntax as well as what I'm calling "M-expression syntax":

| M-expression Syntax     | S-expression Syntax     |
| :---------------------: | :---------------------: |
| `+[1 2 3]`              | `(+ 1 2 3)`             |
| `Def[x 100]`            | `(Def x 100)`           |
| `side-effects-please[]` | `(side-effects-please)` |

The following is an implementation of a function that recursively generates the n-th fibnonacci number: 

```mathematica
Defn[fib[n]
    If[Or[=[n 0] =[n 1]]
       n
       +[ fib[-[n 1]] fib[-[n 2]] ]
    ]
]
    
fib[20] 
```

The program returns `6765`.

## Postfix Notation

An expression of the form

```mathematica
f[a b c d]
```

can also be written in postfix form by putting the function at the end of the list and separating it from the arguments with the double-pipe (`||`) delimiter:

```mathematica
[a b c d || f]
```

As an example, the following two expressions both return `10`:

```mathematica
+[1 2 3 4]
[1 2 3 4 || +]
```

## Special Values

* **Truthiness**
  * `:F`
    * A keyword representing the boolean false value
  * `Nil`
    * A symbol bound to the empty list
    * Is also considered false
  * `:T`
    * A keyword representing the boolean true value
    * Not uniquely "true" since anything that is not `:F` or `Nil` is considered true.

## Built-in Functions

* `+`, `-`, `*`,`/`
  * Arithmetic operators. Each can take a variable number of arguments

* `=[x y z ...]`
  * Returns `:T` if all arguments are equal

* `Head[list]`
  * Like `car`. Returns the first element of the list argument

* `Body[list]`
  * Like `cdr`. Returns a list of all but the first elements in a list

* `Fn[{x y z ...} body]`
  * Replaces Lisp's `lambda`.
  * Accepts a list of formal parameters, and a body.
  * `Fn[{x} *[x x]][12]` returns `144`

* `Def[symbol value]`
  * Declares and assigns to `symbol` the value of the expression `value`
  * `Def[x 100]` binds the symbol `x` to the number `100` in the current environment (scope)
  * Returns the `value`

* `Defn[f[x y z ...] body]`
  * Equivalent to `Def[f Fn[{x y z ...} body]]`
  * Returns the procedure that gets assigned to `f`

* `Set![x v]`

  * Sets the previously-defined symbol `x` to the value of `v`
  * Returns `v`

* `Do[e1 e2 e3 ... en]`

  * Evaluates `e1`, `e2`, ... `en` in order

  * Returns the value of `en`

  * The following program returns `1` after setting `x` to `3` and `y` to `1`:

    ```mathematica
    Do[
        Def[x 1]
        Def[y x]
        Set![x 3]
        y
    ]
    ```

* `Let[{x v1 y v2 ...} body]`

  * Binds `x` to `v1`, `y` to `v2`, etc., then evaluates `body`
  * The variable bindings are only valid during the execution of `body`
  * Equivalent to the immediately invoked lambda expression: `Fn[{x y ...} body][v1 v2 ...]`

* `Quote[expression]` or `'expression`

  * Returns `expression` , unevaluated, as an abstract syntax tree

* `List[v1 v2 v3 ...]` or `{v1 v2 v3 ...}`

  * Returns the abstract syntax tree representing a list which contains the specified values
  * Equivalent to `'(v1 v2 v3 ...)` or `Quote[(1 2 3)]`

* `If[condition e1 e2]`

  * Returns the value of `e1` if `condition` is "truthy" (not `:F` or `Nil`), otherwise, returns the value of `e2`

* `Print[v1 v2 v3 ... vn]`

  * Prints `v1`, `v2`, etc to stdout.
  * Returns the value of `vn`
