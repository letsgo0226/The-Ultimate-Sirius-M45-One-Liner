"""Exact finite Fourier period averaging for real TT profiles.
Modes are integer harmonics of a common angular frequency w.
Coefficients are rational (cosine, sine) pairs; zero-mode sine is ignored.
"""
from fractions import Fraction as Q

def average(f):
    return {0:(Q(f.get(0,(0,0))[0]),Q(0))} if f.get(0,(0,0))[0] else {}

def shift_derivative(f):
    """Derivative with respect to dimensionless phase."""
    return {n:(n*Q(b),-n*Q(a)) for n,(a,b) in f.items() if n and (a or b)}

def inner_average(f,g):
    return Q(f.get(0,(0,0))[0])*Q(g.get(0,(0,0))[0])+sum(
        (Q(a)*Q(g[n][0])+Q(b)*Q(g[n][1]))/2
        for n,(a,b) in f.items() if n>0 and n in g)

def energy_kernel(plus,cross,w=1):
    """Averaged K_ab, omitting 1/(32 pi G_N)."""
    p=shift_derivative(plus)
    q=shift_derivative(cross)
    e=2*Q(w)**2*(inner_average(p,p)+inner_average(q,q))
    k=(1,0,0,-1)
    return tuple(tuple(e*a*b for b in k) for a in k)
