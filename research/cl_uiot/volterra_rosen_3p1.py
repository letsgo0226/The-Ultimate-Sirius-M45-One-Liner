"""Certified local Volterra iteration for polynomial Rosen curvature."""
from fractions import Fraction as Q

def contraction_bound(k,L):
    L=Q(L)
    if L<0:raise ValueError("nonnegative interval radius required")
    return L*L*sum(abs(Q(a))*L**i for i,a in enumerate(k))/2

def step(k,f,sign):
    if sign not in (-1,1):raise ValueError("sign must be +/-1")
    out=[Q(1),Q(0)]+[Q(0)]*max(0,len(k)+len(f)-1)
    for i,a in enumerate(k):
        for j,b in enumerate(f):
            n=i+j
            out[n+2]+=sign*Q(a)*Q(b)/((n+1)*(n+2))
    return out

def iterate(k,L,sign,n):
    if type(n) is not int or n<0:raise ValueError("nonnegative integer iteration count required")
    if sign not in (-1,1):raise ValueError("sign must be +/-1")
    q=contraction_bound(k,L)
    if q>=Q(1,2):raise ValueError("certified positive patch requires q<1/2")
    f=[Q(1)]
    for _ in range(n):f=step(k,f,sign)
    return f,q**(n+1)/(1-q)

def positivity_bound(k,L):
    q=contraction_bound(k,L)
    if q>=Q(1,2):raise ValueError("certified positive patch requires q<1/2")
    return 1-q/(1-q)
