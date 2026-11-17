"""Exact polynomial 3+1 Maxwell curvature and gauge invariance.

Minkowski signature (+---), x=(t,x,y,z). All coefficients rational.
The free Maxwell Lagrangian is -F_{mu nu} F^{mu nu}/4.
No PDE solver, boundary integration, or quantization is implemented.
"""
from fractions import Fraction as Q
from itertools import combinations

N=4
ETA=(1,-1,-1,-1)

def clean(p):
    return {k:Q(v) for k,v in p.items() if v}
def add(*ps):
    out={}
    for p in ps:
        for k,v in p.items():
            out[k]=out.get(k,Q(0))+v
    return clean(out)
def scale(p,c):
    return clean({k:Q(c)*v for k,v in p.items()})
def mul(p,q):
    out={}
    for a,v in p.items():
        for b,w in q.items():
            key=tuple(x+y for x,y in zip(a,b))
            out[key]=out.get(key,Q(0))+v*w
    return clean(out)
def deriv(p,mu):
    if mu not in range(N):
        raise ValueError("coordinate index must be 0..3")
    out={}
    for powers,c in p.items():
        if powers[mu]:
            k=list(powers)
            k[mu]-=1
            key=tuple(k)
            out[key]=out.get(key,Q(0))+c*powers[mu]
    return clean(out)
def check_p(p):
    if any(len(k)!=N or any(not isinstance(v,int) or v<0 for v in k) for k in p):
        raise ValueError("polynomial keys must be 4 nonnegative integer exponents")
def check_A(A):
    if len(A)!=N:
        raise ValueError("expected four covariant potential components")
    for p in A:check_p(p)
def strength(A,mu,nu):
    check_A(A)
    if mu not in range(N) or nu not in range(N):
        raise ValueError("index out of range")
    return add(deriv(A[nu],mu),scale(deriv(A[mu],nu),-1))
def gauge_shift(A,chi):
    check_A(A)
    check_p(chi)
    return tuple(add(A[mu],deriv(chi,mu)) for mu in range(N))
def lagrangian(A):
    check_A(A)
    out={}
    for mu,nu in combinations(range(N),2):
        f=strength(A,mu,nu)
        out=add(out,scale(mul(f,f),-Q(1,2)*ETA[mu]*ETA[nu]))
    return out
def maxwell_divergence(A):
    """j^nu=partial_mu F^{mu nu}; off-shell induced current."""
    check_A(A)
    result=[]
    for nu in range(N):
        terms=[]
        for mu in range(N):
            if mu!=nu:
                terms.append(scale(deriv(strength(A,mu,nu),mu),
                                   ETA[mu]*ETA[nu]))
        result.append(add(*terms))
    return tuple(result)
def current_divergence(j):
    if len(j)!=N:
        raise ValueError("expected four current components")
    return add(*(deriv(j[nu],nu) for nu in range(N)))
def check_bianchi(A):
    """partial_lambda F_mu nu + cyclic = 0 for distinct indices."""
    check_A(A)
    for a,b,c in combinations(range(N),3):
        cyclic=add(deriv(strength(A,b,c),a),
                   deriv(strength(A,c,a),b),
                   deriv(strength(A,a,b),c))
        if cyclic:return False
    return True
def check_gauge_invariance(A,chi):
    shifted=gauge_shift(A,chi)
    return (all(strength(A,i,j)==strength(shifted,i,j)
                for i,j in combinations(range(N),2))
            and lagrangian(A)==lagrangian(shifted))
def demo():
    A=({(0,1,0,0):Q(2)}, {(2,0,0,0):Q(1)},
       {(0,0,1,0):Q(3)}, {(0,0,0,1):Q(4)})
    chi={(1,1,1,0):Q(2)}
    return {"dimension":"3+1", "gauge_invariant":check_gauge_invariance(A,chi),
            "bianchi_identity":check_bianchi(A),
            "induced_current_conserved":current_divergence(maxwell_divergence(A))=={},
            "scope":"exact rational classical Abelian identities, not a Maxwell PDE solver"}
if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
