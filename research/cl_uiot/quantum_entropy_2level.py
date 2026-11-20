"""Exact real two-level density matrix invariants, plus numerical entropy."""
from fractions import Fraction as Q
from math import sqrt,log2

def density(a,b):
    a,b=Q(a),Q(b)
    if not 0<=a<=1 or b*b>a*(1-a):raise ValueError("not a density matrix")
    return ((a,b),(b,1-a))

def mul(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def transpose(A):
    return tuple(zip(*A))

def rotation(t):
    t=Q(t)
    c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
    return ((c,-s),(s,c))

def evolve(a,b,t):
    U=rotation(t)
    return mul(mul(U,density(a,b)),transpose(U))

def invariants(a,b):
    R=density(a,b)
    return R[0][0]*R[1][1]-R[0][1]**2,sum(v*v for row in R for v in row)

def entropy(a,b):
    d,_=invariants(a,b)
    # Stable small eigenvalue via product of eigenvalues.
    p=2*float(d)/(1+sqrt(max(0,1-4*float(d))))
    return -sum(x*log2(x) for x in (p,1-p) if x>0)

def measurement_entropy(a,b):
    density(a,b)
    return entropy(a,0)
