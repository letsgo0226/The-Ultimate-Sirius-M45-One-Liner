"""Exact amplitude damping on real qubit states, rational survival amplitude."""
from fractions import Fraction as Q
from quantum_entropy_2level import density,mul,transpose,entropy

def kraus(r):
    r=Q(r)
    if not 0<=r<=1:raise ValueError("survival amplitude outside [0,1]")
    # E0 exact; E1 = sqrt(1-r²) times L.
    return ((Q(1),Q(0)),(Q(0),r)),((0,1),(0,0)),1-r*r

def evolve(a,b,r,n=1):
    density(a,b)
    r=Q(r);kraus(r)
    if type(n) is not int or n<0:raise ValueError("invalid iteration count")
    return density(1-(1-Q(a))*r**(2*n),Q(b)*r**n)

def trace_distance_squared(a,b,r,n):
    R=evolve(a,b,r,n)
    return R[1][1]**2+R[0][1]**2

def entropy_after(a,b,r,n):
    R=evolve(a,b,r,n)
    return entropy(R[0][0],R[0][1])
