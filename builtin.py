from AST import Expression


class BuiltIn(Expression):
    def __init__(self, fn, name=None):
        self.fn = fn
        self.name = name if name is not None else f"@ {id(self)}"

    def apply(self, args, env):
        return self.fn(args, env)

    def __str__(self):
        return f"<BuiltIn {self.name}>"
