"""Logical Pauli error floor under independent depolarizing noise."""
from fractions import Fraction as Q
from itertools import product
from qec_perfect_5qubit import residual,stabilize
from qec_concatenated_5qubit import probability

def witness():
    S=stabilize()
    for v in product("IXYZ",repeat=5):
        p="".join(v)
        if sum(c!="I" for c in p)==2 and residual(p) not in S:return p
    raise ArithmeticError("missing witness")

def single_floor(p):
    p=probability(p)
    return (p/3)**2*(1-p)**3

def logical_distribution(weights):
    w=tuple(map(probability,weights))
    if len(w)!=4 or sum(w)!=1:raise ValueError("invalid Pauli distribution")
    S=stabilize()
    cosets=[S]+[{__import__("qec_perfect_5qubit").multiply_labels(g*5,x) for x in S} for g in "XYZ"]
    lookup={x:i for i,c in enumerate(cosets) for x in c}
    out=[Q(0)]*4
    for v in product(range(4),repeat=5):
        r=residual("".join("IXYZ"[i] for i in v))
        a=Q(1)
        for i in v:a*=w[i]
        out[lookup[r]]+=a
    return tuple(out)

def concatenate(p,n):
    p=probability(p)
    if type(n) is not int or n<0:raise ValueError("invalid depth")
    w=(1-p,p/3,p/3,p/3)
    for _ in range(n):w=logical_distribution(w)
    return w

def full_support_floor(p,n):
    p=probability(p)
    if type(n) is not int or n<0:raise ValueError("invalid depth")
    return min(1-p,p/3)**(5**n)
