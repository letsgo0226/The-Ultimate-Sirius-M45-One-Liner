"""Exact rational enclosure of prime-weighted nonnegative residual series."""
from fractions import Fraction as Q

def primes(n):
    a=[]
    k=2
    while len(a)<n:
        if all(k%p for p in a if p*p<=k):
            a.append(k)
        k+=1
    return a

def enclosure(residuals,sigma=2):
    if type(sigma) is not int or not 2<=sigma<=16:
        raise ValueError("integer sigma in 2..16")
    if not isinstance(residuals,(tuple,list)) or not 1<=len(residuals)<=1024:
        raise ValueError("1..1024 residuals required")
    if any(type(r) not in (int,Q) or r<0 for r in residuals):
        raise ValueError("exact nonnegative residuals required")
    ps=primes(len(residuals))
    lo=sum((Q(r)/(1+r)/p**sigma for r,p in zip(residuals,ps)),Q(0))
    tail=Q(1,(sigma-1)*ps[-1]**(sigma-1))
    return {"lower":lo,"upper":lo+tail,"tail_bound":tail,
            "status":"NONZERO" if lo>0 else "UNKNOWN"}

def matrix_residual(lam,mu):
    if any(type(v) not in (int,Q) for v in (lam,mu)):
        raise ValueError("exact rational coefficients required")
    return Q(mu)**2*(1+Q(lam)**2)
