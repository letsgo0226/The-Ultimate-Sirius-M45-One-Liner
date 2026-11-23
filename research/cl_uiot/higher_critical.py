"""Cubic stable graph coefficient at the algebraic critical point."""
from fractions import Fraction as Q
from algebraic_curvature import K,lift,jet,critical

def radial_cubic(v):
    v=tuple(map(lift,v))
    if len(v)!=4 or v[0]!=0 or sum(v)!=0:raise ValueError("transverse tangent required")
    return sum(a[3] for a in jet(v)[1:])

def cubic_graph(v):
    return Q(-3,5)*radial_cubic(v)

def cubic_formula(v):
    v=tuple(map(lift,v))
    if len(v)!=4 or v[0]!=0 or sum(v)!=0:raise ValueError("transverse tangent required")
    w=critical()
    return -18*(w[0]**2+3*w[1]**2)*v[1]*v[2]*v[3]
