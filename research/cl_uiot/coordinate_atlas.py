"""Exact rational projective line; bounded local demonstration."""
from fractions import Fraction as Q

def point(u,v):
    u,v=Q(u),Q(v)
    if v:
        return u/v,Q(1)
    if u:
        return Q(1),Q(0)
    raise ValueError("zero homogeneous pair")

def chart(p,kind):
    u,v=point(*p)
    if kind=="x" and v:
        return u/v
    if kind=="y" and u:
        return v/u
    raise ValueError("chart unavailable")

def lift(z,kind):
    if kind=="x":
        return point(z,1)
    if kind=="y":
        return point(1,z)
    raise ValueError("unknown chart")

def reflect(p):
    u,v=point(*p)
    return point(-u,v)

def step(p):
    # x -> x/(1-x); in reciprocal chart y -> y-1.
    u,v=point(*p)
    return point(u,v-u)

def regular_step(p):
    # For nonzero x (including projective infinity), use reciprocal chart.
    u,v=point(*p)
    if u:
        return lift(chart((u,v),"y")-1,"y")
    return point(0,1)
