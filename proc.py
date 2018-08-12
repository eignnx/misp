from env import Env
from AST import Expression, Symbol
from typing import Collection

class Procedure(Expression):
    def __init__(self, formals: Collection[Symbol], body, creation_env: Env):
        self.formals = formals # The names of the formal parameters
        self.body = body # The body AST
        self.creation_env = creation_env # A ref to the env where the proc was defined

    def apply(self, args):
        if len(self.formals) != len(args):
            raise Exception("Wrong number of arguments!")

        local_bindings = dict(zip(self.formals, args))
        env = Env(locals_=local_bindings, parent=self.creation_env)
        return self.body.evaluate(env)

    def evaluate(self, env):
        return self
