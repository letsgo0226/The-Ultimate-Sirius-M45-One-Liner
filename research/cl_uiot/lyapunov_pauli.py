"""Strict Lyapunov certificate on the Bloch l1 unit ball."""
from fractions import Fraction as Q
from basin_separation import closed_bloch

def coordinates(z):
    z=tuple(map(Q,z))
    if len(z)!=3 or sum(map(abs,z))>1:raise ValueError("outside l1 unit ball")
    return z

def lyapunov(z):return sum(map(abs,coordinates(z)))

def factor():return Q(9,16)

def step(z):
    z=coordinates(z)
    out=closed_bloch(*z)
    if lyapunov(out)>factor()*lyapunov(z):raise ArithmeticError("contraction violation")
    return out

def bound(z,n):
    if type(n) is not int or n<0:raise ValueError("invalid depth")
    return factor()**n*lyapunov(z)
