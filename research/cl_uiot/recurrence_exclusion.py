"""Forward-invariant high-amplitude cubes and recurrence exclusion."""
from fractions import Fraction as Q
from universal_pauli import from_bloch
from basin_separation import closed_bloch
from radial_angular import scalar

def certificate(z):
    z=tuple(map(Q,z))
    from_bloch(*z)
    a=min(map(abs,z))
    if a*a<Q(2,3):raise ValueError("outside invariant cube")
    lower=scalar(a)
    nxt=min(map(abs,closed_bloch(*z)))
    if nxt<lower or lower<a:raise ArithmeticError("comparison violation")
    return {"minimum":a,"next_minimum":nxt,"lower":lower,
            "vertex_basin":a*a>Q(2,3)}

def endpoint_gap(a):
    a=Q(a)
    if not Q(4,5)<=a<=1:raise ValueError("outside endpoint bound")
    return (1-a)**2*(6*a**3+7*a*a-2*a-1)/4
