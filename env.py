class Env:
    """
    Represents a scoped variable environment. See assertion
    tests at bottom of module for examples.
    """

    def __init__(self, parent=None, local=None):
        self.parent = parent if parent is not None else EmptyDict()
        self.local = local if local is not None else dict()

    def __getitem__(self, name):
        val = self.local.get(name)
        if val:
            return val
        else:
            return self.parent[name]

    def declare(self, name):
        self.local[name] = None

    def declare_all(self, *names):
        self.local.update((name, None) for name in names)

    def __setitem__(self, name, value):
        if name in self.local:
            self.local[name] = value
        else:
            self.parent[name] = value

    def __contains__(self, name):
        return name in self.local or name in self.parent

    def __repr__(self):
        fmt = "Env(parent: {}, local: {})"
        return fmt.format(self.parent, self.local)


class EmptyDict:
    def __getitem__(self, name):
        raise KeyError("Unbound variable '{}'".format(name))

    def __setitem__(self, name, value):
        raise KeyError("Unbound variable '{}'".format(name))

    def __contains__(self, name):
        return False

    def __str__(self):
        return "{}"

    def __repr__(self):
        return "EmptyDict()"


if __name__ == "__main__":

    glob = Env() # A global scope with no parent scope
    loc = Env(glob) # A local scope contained within `glob`

    glob.declare_all("name", "age") # Declare multiple vars
    glob["name"] = "Kat"
    glob["age"] = 22
    
    assert loc["name"] == "Kat"
    
    loc["name"] = "Ben" # Reassign global variable
    
    assert loc["name"] == "Ben"
    assert glob["name"] == "Ben"

    loc.declare("name") # Make a local variable
    loc["name"] = "Jen" # Assign to local variable

    assert loc["name"] == "Jen"
    assert glob["name"] == "Ben"

    assert loc["age"] == 22
    assert glob["age"] == 22

    print("Tests Passed")

