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
       +[ fib[-[n 1]] fib[-[n 2]]] ]
    ]
    
fib[20] 
```

The program returns `6765`.
