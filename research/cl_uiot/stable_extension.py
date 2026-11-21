"""Exact finite preimage certificates for rational polynomial observables."""
from fractions import Fraction as Q
from universal_pauli import weights,evaluate
from interval_basin import box,step

def preimage(w,n,predicate):
    w=weights(w)
    if type(n) is not int or n<0:raise ValueError("invalid depth")
    for _ in range(n):w=evaluate(w)
    return bool(predicate(w))

def pullback(bounds,n,digits=12):
    b=box(bounds)
    if type(n) is not int or n<0:raise ValueError("invalid depth")
    for _ in range(n):b=step(b,digits)
    return b

def intersects(a,b):
    a,b=box(a),box(b)
    c=tuple((max(x[0],y[0]),min(x[1],y[1])) for x,y in zip(a,b))
    try:box(c)
    except ValueError:return False
    return True

def exclude(bounds,target,n,digits=12):
    return not intersects(pullback(bounds,n,digits),target)
