"""Exact Schwarzschild invariant diagnostic in geometrized units."""
from fractions import Fraction as Q
from coordinate_atlas import point,reflect,step

def diagnostic(r,m=1):
    r,m=Q(r),Q(m)
    if m<=0 or r<0:
        raise ValueError("positive mass and nonnegative radius required")
    if r==0:
        return "curvature_singularity",None
    k=48*m*m/r**6
    return ("coordinate_horizon" if r==2*m else "regular"),k

def inverse_step(p):
    u,v=point(*p)
    return point(u,v+u)

def curvature_scaled(r,m=1):
    r,m=Q(r),Q(m)
    if r<=0 or m<=0:
        raise ValueError("positive radius and mass required")
    return diagnostic(r,m)[1]*r**6

def reciprocal_curvature(r,m=1):
    r,m=Q(r),Q(m)
    if r<0 or m<=0:
        raise ValueError("domain")
    return r**6/(48*m*m)
