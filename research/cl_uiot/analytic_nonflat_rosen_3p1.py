"""Nonflat analytic Rosen vacuum wave; exact Taylor metric coefficients."""
from fractions import Fraction as Q
from math import factorial
from tt_gravity_wave_3p1 import profile

def metric_series(order):
    if type(order) is not int or order<0:
        raise ValueError("nonnegative integer order required")
    fields=[]
    for n in range(1,order+1):
        h=[[{} for _ in range(4)] for _ in range(4)]
        if n%2==0:
            c=Q(2**(n-1),factorial(n))
            h[1][1]=profile([0]*n+[-(-1)**(n//2)*c])
            h[2][2]=profile([0]*n+[-c])
        fields.append(h)
    return fields

def scaled_tidal(epsilon):
    """A''/A and B''/B, exact, in a nonsingular Rosen patch."""
    e=Q(epsilon)
    return -e*e,e*e

def tail_bound(order,radius):
    """Uniform component Taylor tail on |epsilon*u|<=radius<=1/2."""
    if type(order) is not int or order<0:
        raise ValueError("nonnegative integer order required")
    r=Q(radius)
    if not 0<=r<=Q(1,2):raise ValueError("radius outside certified patch")
    n=2*(order//2+1)
    return Q(2**(n-1),factorial(n))*r**n/(1-Q(4)*r*r/((n+1)*(n+2)))
