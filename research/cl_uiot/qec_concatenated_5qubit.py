"""Exact concatenated five-qubit ideal independent Pauli noise bound."""
from fractions import Fraction as Q
from math import comb
from itertools import product
from qec_perfect_5qubit import residual,stabilize

def probability(p):
    p=Q(p)
    if not 0<=p<=1:raise ValueError("invalid probability")
    return p

def bound(p):
    p=probability(p)
    return sum(comb(5,k)*p**k*(1-p)**(5-k) for k in range(2,6))

def iterate(p,n):
    p=probability(p)
    if type(n) is not int or n<0:raise ValueError("invalid depth")
    for _ in range(n):p=bound(p)
    return p

def certified_bound(p,n):
    p=probability(p)
    if p>=Q(1,10):raise ValueError("requires p < 1/10")
    if type(n) is not int or n<0:raise ValueError("invalid depth")
    return (10*p)**(2**n)/10

def failure_counts():
    S=stabilize()
    counts=[0]*6
    for v in product("IXYZ",repeat=5):
        p="".join(v)
        if residual(p) not in S:counts[sum(c!="I" for c in p)]+=1
    return tuple(counts)

def depolarizing_failure(p):
    p=probability(p)
    return sum(c*(p/3)**k*(1-p)**(5-k) for k,c in enumerate(failure_counts()))
