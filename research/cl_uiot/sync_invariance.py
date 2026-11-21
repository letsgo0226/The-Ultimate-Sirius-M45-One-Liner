"""Two rigorously invariant subsets of the synchronization cone."""
from fractions import Fraction as Q
from persistent_gap import cone,certificate
from basin_separation import closed_bloch
from universal_pauli import from_bloch

def region(z):
    z=tuple(map(Q,z))
    from_bloch(*z)
    if not cone(z):return None
    m,M=min(map(abs,z)),max(map(abs,z))
    if M*M<=Q(2,3):return "subcritical"
    if 5*m*m>=3*M*M:return "ratio"
    return None

def invariant_step(z):
    z=tuple(map(Q,z))
    label=region(z)
    if label is None:raise ValueError("outside certified invariant subsets")
    certificate(z)
    out=closed_bloch(*z)
    m,M=min(map(abs,out)),max(map(abs,out))
    if not cone(out):raise ArithmeticError("cone violation")
    if label=="subcritical" and M*M>Q(2,3):raise ArithmeticError("radial violation")
    if label=="ratio" and 5*m*m<3*M*M:raise ArithmeticError("ratio violation")
    return out
