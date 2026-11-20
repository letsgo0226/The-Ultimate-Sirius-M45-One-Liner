"""Exact symmetric-slice Jacobian polynomial and critical tangent splitting."""
from fractions import Fraction as Q
from math import comb
from universal_pauli import coefficients

def slice_jacobian_polynomials():
    out=[]
    for d in coefficients()[1:]:
        row=[]
        for j in (1,2,3):
            a=[Q(0)]*5
            for k,c in d:
                for h,sign in ((j,1),(0,-1)):
                    if not k[h]:continue
                    i=k[0]-(h==0);r=4-i
                    for l in range(i+1):
                        a[r+l]+=Q(sign*c*k[h]*comb(i,l)*(-1)**l,3**r)
            row.append(tuple(a))
        out.append(tuple(row))
    return tuple(out)

def critical_jacobian():
    expected=(Q(0),Q(20,3),Q(-200,9),Q(640,27),Q(-640,81))
    if any(a!=expected for row in slice_jacobian_polynomials() for a in row):
        raise ArithmeticError("slice polynomial mismatch")
    return ((Q(5,9),)*3,)*3

def split(v):
    v=tuple(map(Q,v))
    if len(v)!=3:raise ValueError("three tangent coordinates required")
    a=sum(v)/3
    return (a,)*3,tuple(x-a for x in v)
