"""Exact angular synchronization checks outside the depolarizing octahedron."""
from fractions import Fraction as Q
from universal_pauli import weights,bloch
from basin_separation import closed_bloch

def factors(z):
    x,y,z=map(Q,z)
    return tuple((5*b*b+5*c*c-a**4-5*b*b*c*c)/4 for a,b,c in ((x,y,z),(y,z,x),(z,x,y)))

def spread(z):
    a=sorted(map(abs,z))
    if not a[0]:raise ValueError("zero coordinate")
    return a[-1]/a[0]

def angular_step(w):
    z=bloch(weights(w))
    if sum(map(abs,z))<=1:return {"status":"central"}
    out=closed_bloch(*z)
    if sum(map(abs,out))<=1:return {"status":"entered"}
    a,b=spread(z),spread(out)
    return {"status":"outside","before":a,"after":b}
