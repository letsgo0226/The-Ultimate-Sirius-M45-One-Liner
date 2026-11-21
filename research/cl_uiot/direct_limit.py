"""Bounded block direct limit with exact rational finite restrictions."""
from fractions import Fraction as Q

def exact(x):
    if type(x) not in (int,Q):
        raise ValueError("exact rational required")
    return Q(x)

def coupling(k):
    if type(k) is not int or k<1:
        raise ValueError("positive block index required")
    return Q(1,k)

def apply(values):
    if not isinstance(values,(tuple,list)) or not 1<=len(values)<=4096:
        raise ValueError("finite vector length 1..4096")
    v=tuple(map(exact,values))
    out=[]
    for j in range(0,len(v)-1,2):
        a,b=v[j:j+2]
        out.extend((-a+coupling(j//2+1)*b,b))
    if len(v)%2:
        out.append(-v[-1])
    return tuple(out)

def embed(values):
    v=tuple(values)
    if not 1<=len(v)<4096:
        raise ValueError("embedding length cap")
    return tuple(map(exact,v))+(Q(0),)

def norm_squared(values):
    return sum((exact(x)**2 for x in values),Q(0))
