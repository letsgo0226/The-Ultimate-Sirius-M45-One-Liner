"""Exact polynomial Moyal coefficients in canonical (X,Px,Y,Py) order."""
from fractions import Fraction as Q
from math import factorial
from maxwell_3p1 import add,mul,scale,deriv

def bidifferential(a,b,n):
    if type(n) is not int or n<0:raise ValueError("nonnegative order")
    terms=[(a,b,1)]
    for _ in range(n):
        terms=[(da,db,c*s) for f,g,c in terms
               for i,j,s in ((0,1,1),(1,0,-1),(2,3,1),(3,2,-1))
               if (da:=deriv(f,i)) and (db:=deriv(g,j))]
    return add(*(scale(mul(f,g),c) for f,g,c in terms)) if terms else {}

def moyal_coefficient(a,b,r):
    if type(r) is not int or r<0:raise ValueError("nonnegative order")
    return scale(bidifferential(a,b,2*r+1),Q((-1)**r,4**r*factorial(2*r+1)))

def hamiltonian(k):
    k=Q(k)
    return {e:v for e,v in [((0,2,0,0),Q(1,2)),((0,0,0,2),Q(1,2)),
                            ((2,0,0,0),k/2),((0,0,2,0),-k/2)] if v}

def liouville(k,w):
    return moyal_coefficient(hamiltonian(k),w,0)
