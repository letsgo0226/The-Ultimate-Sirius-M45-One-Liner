"""Radial comparison with an exact angular-error bound."""
from fractions import Fraction as Q
from universal_pauli import from_bloch
from basin_separation import closed_bloch
from angular_sync import region

def scalar(a):
    a=Q(a)
    if not 0<=a<=1:raise ValueError("invalid amplitude")
    return (5*a**3-3*a**5)/2

def radial(z):
    z=tuple(map(Q,z))
    from_bloch(*z)
    if not region(z):raise ValueError("outside synchronization region")
    a=tuple(map(abs,z))
    m=sum(a)/3
    width=max(a)-min(a)
    out=tuple(map(abs,closed_bloch(*z)))
    mean=sum(out)/3
    error=5*width
    if abs(mean-scalar(m))>error:raise ArithmeticError("radial bound violation")
    return {"mean":m,"next_mean":mean,"width":width,"error":error,
            "lower":max(Q(0),scalar(m)-error),"upper":min(Q(1),scalar(m)+error)}

def drift(a):
    a=Q(a)
    return scalar(a)-a
