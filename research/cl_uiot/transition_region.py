"""Global maximum-amplitude comparison for Pauli renormalization."""
from fractions import Fraction as Q
from universal_pauli import from_bloch
from basin_separation import closed_bloch
from radial_angular import scalar

def maximum(z):
    z=tuple(map(Q,z))
    from_bloch(*z)
    return max(map(abs,z))

def compare(z):
    z=tuple(map(Q,z))
    m=maximum(z)
    out=closed_bloch(*z)
    n=maximum(out)
    upper=scalar(m)
    if n>upper:raise ArithmeticError("comparison violation")
    return {"maximum":m,"next_maximum":n,"upper":upper,
            "central_basin":m*m<Q(2,3)}

def contraction(z):
    m=maximum(z)
    if m*m>=Q(2,3):raise ValueError("outside strict certificate")
    return (5*m*m-3*m**4)/2
