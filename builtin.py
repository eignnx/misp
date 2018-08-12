from AST import Expression


class BuiltIn(Expression):
    def __init__(self, fn):
        self.fn = fn

    def apply(self, args, env):
        return self.fn(args, env)
