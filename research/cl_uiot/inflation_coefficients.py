"""Exact parameterization of compatible involutive block extensions."""
from fractions import Fraction as Q

def matrix(a):
    if not isinstance(a,(list,tuple)) or not 1<=len(a)<=32:
        raise ValueError("matrix rows")
    if any(not isinstance(r,(list,tuple)) for r in a):
        raise ValueError("matrix row")
    n=len(a[0])
    if not 1<=n<=32 or any(len(r)!=n for r in a):
        raise ValueError("matrix shape")
    if any(type(v) not in (int,Q) for r in a for v in r):
        raise ValueError("exact entries required")
    return tuple(tuple(map(Q,r)) for r in a)

def mul(a,b):
    if len(a[0])!=len(b):
        raise ValueError("incompatible dimensions")
    return tuple(tuple(sum(x*y for x,y in zip(r,c)) for c in zip(*b)) for r in a)

def identity(n):
    return tuple(tuple(Q(i==j) for j in range(n)) for i in range(n))

def involution(a):
    a=matrix(a)
    if len(a)!=len(a[0]) or mul(a,a)!=identity(len(a)):
        raise ValueError("involution required")
    return a

def project(t,s,x):
    t,s,x=involution(t),involution(s),matrix(x)
    if len(x)!=len(t) or len(x[0])!=len(s):
        raise ValueError("coupling shape")
    y=mul(mul(t,x),s)
    return tuple(tuple((a-b)/2 for a,b in zip(r,q)) for r,q in zip(x,y))

def extend(t,s,a):
    t,s,a=involution(t),involution(s),matrix(a)
    if len(t)+len(s)>32:
        raise ValueError("extension dimension cap")
    if project(t,s,a)!=a:
        raise ValueError("incompatible coupling")
    return tuple(r+q for r,q in zip(t,a))+tuple((Q(0),)*len(t)+r for r in s)
