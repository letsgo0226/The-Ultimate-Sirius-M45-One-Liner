"""Exact depolarizing invariant slice of the logical renormalization map."""
from fractions import Fraction as Q
from qec_concatenated_5qubit import probability
from physical_error_floor import logical_distribution

def renormalize(w):
    return logical_distribution(w)

def depolarizing(p):
    p=probability(p)
    return (1-p,p/3,p/3,p/3)

def scalar(p):
    p=probability(p)
    a=1-4*p/3
    return Q(3,4)*(1-(5*a**3-3*a**5)/2)

def derivative(p):
    a=1-4*probability(p)/3
    return Q(15,2)*a*a*(1-a*a)

def threshold_bracket(steps):
    if type(steps) is not int or steps<0:raise ValueError("invalid steps")
    lo,hi=Q(0),Q(3,4)
    for _ in range(steps):
        mid=(lo+hi)/2
        if mid==0 or scalar(mid)<mid:lo=mid
        else:hi=mid
    return lo,hi

def iterate_scalar(p,n):
    p=probability(p)
    if type(n) is not int or n<0:raise ValueError("invalid depth")
    for _ in range(n):p=scalar(p)
    return p
