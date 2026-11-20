"""Certified exclusion of a weak-coordinate near-critical band."""
from fractions import Fraction as Q
from transition_region import maximum
from basin_separation import closed_bloch
from radial_angular import scalar

def ceiling():
    return max(Q(1,4),Q(5,8),
        scalar(Q(5,6))-Q(10)*Q(2,3)*Q(11,36)*Q(2,15)/4,
        scalar(Q(5,6))-Q(5)*Q(11,36)*Q(2,9)/8)

def band(z):
    z=tuple(map(Q,z))
    m=maximum(z)
    return Q(2,3)<=m*m and m<=Q(5,6) and min(map(abs,z))<=Q(2,3)

def certificate(z):
    z=tuple(map(Q,z))
    if not band(z):raise ValueError("outside certified band")
    out=maximum(closed_bloch(*z))
    upper=ceiling()
    if out>upper:raise ArithmeticError("bound violation")
    return {"next_maximum":out,"upper":upper,"central_basin":upper**2<Q(2,3)}
