"""Volterra factorial convergence on any bounded symmetric interval."""
from fractions import Fraction as Q
from math import factorial
from volterra_rosen_3p1 import step

def bound_parameter(k,L):
    L=Q(L)
    if L<0:raise ValueError("negative radius")
    return L**2*sum(abs(Q(a))*L**i for i,a in enumerate(k))

def tail_bound(k,L,n):
    if type(n) is not int or n<0:raise ValueError("invalid iteration count")
    z=bound_parameter(k,L)
    m=n+1
    ratio=z/((2*m+1)*(2*m+2))
    if ratio>=1:raise ValueError("increase iteration count for geometric tail certificate")
    return z**m/Q(factorial(2*m))/(1-ratio)

def iterate(k,L,sign,n):
    if sign not in (-1,1):raise ValueError("invalid sign")
    error=tail_bound(k,L,n)
    f=[Q(1)]
    for _ in range(n):f=step(k,f,sign)
    return f,error

def positive_certificate(f,L,error):
    """Conservative lower bound for exact solution from polynomial approximation."""
    L,error=Q(L),Q(error)
    if L<0 or error<0 or not f:raise ValueError("invalid certificate data")
    return Q(f[0])-sum(abs(Q(a))*L**i for i,a in enumerate(f[1:],1))-error
