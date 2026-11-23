"""Exact polynomial map and tangent Jacobian on the Pauli simplex."""
from fractions import Fraction as Q
from itertools import product
from functools import lru_cache
from qec_perfect_5qubit import residual,stabilize,multiply_labels
from physical_error_floor import logical_distribution

@lru_cache(maxsize=1)
def coefficients():
    S=stabilize()
    cosets=[S]+[{multiply_labels(g*5,x) for x in S} for g in "XYZ"]
    lookup={x:i for i,c in enumerate(cosets) for x in c}
    out=[{} for _ in range(4)]
    for v in product("IXYZ",repeat=5):
        k=tuple(v.count(c) for c in "IXYZ")
        d=out[lookup[residual("".join(v))]]
        d[k]=d.get(k,0)+1
    return tuple(tuple(sorted(d.items())) for d in out)

def monomial(w,k):
    a=Q(1)
    for v,n in zip(w,k):a*=v**n
    return a

def weights(w):
    w=tuple(map(Q,w))
    if len(w)!=4 or min(w)<0 or sum(w)!=1:raise ValueError("invalid simplex point")
    return w

def evaluate(w):
    w=weights(w)
    return tuple(sum(c*monomial(w,k) for k,c in d) for d in coefficients())

def jacobian(w):
    w=weights(w)
    def partial(d,j):
        return sum(c*k[j]*monomial(w,tuple(v-(i==j) for i,v in enumerate(k))) for k,c in d if k[j])
    return tuple(tuple(partial(d,j)-partial(d,0) for j in (1,2,3)) for d in coefficients()[1:])

def bloch(w):
    _,a,b,c=weights(w)
    return 1-2*(b+c),1-2*(a+c),1-2*(a+b)

def from_bloch(x,y,z):
    x,y,z=map(Q,(x,y,z))
    return weights(((1+x+y+z)/4,(1+x-y-z)/4,(1-x+y-z)/4,(1-x-y+z)/4))

def bloch_map(x,y,z):
    return bloch(evaluate(from_bloch(x,y,z)))
