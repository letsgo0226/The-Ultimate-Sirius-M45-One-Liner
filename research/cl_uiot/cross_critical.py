"""Quantitative maximum deficit near the critical amplitude."""
from fractions import Fraction as Q
from transition_region import maximum
from radial_angular import scalar
from basin_separation import closed_bloch

def deficit(z):
    z=tuple(map(Q,z))
    M=maximum(z)
    if M*M<Q(2,3) or M>Q(5,6):raise ValueError("outside critical shell")
    w=M-min(map(abs,z))
    upper=scalar(M)-w/8
    nxt=maximum(closed_bloch(*z))
    if nxt>upper:raise ArithmeticError("deficit violation")
    return {"width":w,"upper":upper,"next_maximum":nxt,
            "central_basin":upper*upper<Q(2,3)}

