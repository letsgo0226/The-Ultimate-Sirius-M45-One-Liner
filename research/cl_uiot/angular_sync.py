"""Pairwise ratio contraction in a certified high-magnitude region."""
from fractions import Fraction as Q
from global_basin import factors,spread
from basin_separation import closed_bloch

def region(z):
    z=tuple(map(Q,z))
    if len(z)!=3 or max(map(abs,z))>1:raise ValueError("invalid coordinates")
    return min(x*x for x in z)>=Q(3,5)

def ratio_step(z):
    z=tuple(map(Q,z))
    if not region(z):raise ValueError("outside certified region")
    out=closed_bloch(*z)
    before,after=spread(z),spread(out)
    if after>before or (before>1 and after==before):
        raise ArithmeticError("ratio contraction violation")
    return before,after

def crossing_identity(x,y,z):
    x,y,z=map(Q,(x,y,z))
    a,b,_=factors((x,y,z))
    return 4*(x*x*a-y*y*b),(x*x-y*y)*(5*z*z-x**4-x*x*y*y-y**4)
