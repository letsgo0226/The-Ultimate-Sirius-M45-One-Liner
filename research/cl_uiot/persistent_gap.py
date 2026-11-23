"""Scale-dependent angular synchronization certificate."""
from fractions import Fraction as Q
from universal_pauli import from_bloch
from basin_separation import closed_bloch

def cone(z):
    z=tuple(map(Q,z))
    from_bloch(*z)
    m,M=min(map(abs,z)),max(map(abs,z))
    return m>0 and 5*m*m>=3*M**4

def certificate(z):
    z=tuple(map(Q,z))
    if not cone(z):raise ValueError("outside synchronization cone")
    a=tuple(map(abs,z))
    b=tuple(map(abs,closed_bloch(*z)))
    r=max(a)/min(a)
    s=max(b)/min(b)
    if s>r or (r>1 and s==r):raise ArithmeticError("contraction violation")
    return r,s
