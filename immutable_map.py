from immutables import Map
from functools import reduce

def immutable_map(dictionary):
    return immutable_add(dictionary, Map())

def immutable_add(pairs, m):
    return reduce(lambda m, kv: m.set(*kv), pairs.items(), m)
