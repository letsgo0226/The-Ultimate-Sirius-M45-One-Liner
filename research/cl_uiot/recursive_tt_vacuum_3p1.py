"""Finite recursive vacuum corrections for local polynomial TT plane waves."""
from fractions import Fraction as Q
from formal_einstein_3p1 import coefficients
from tt_gravity_wave_3p1 import tt_wave,profile

def zero():
    return [[{} for _ in range(4)] for _ in range(4)]

def solve(plus,cross,order):
    if type(order) is not int or order<1:
        raise ValueError("positive integer order required")
    fields=[tt_wave(plus,cross)]
    if any(coefficients(fields)[1][a][b] for a in range(4) for b in range(4)):
        raise ArithmeticError("first-order vacuum required")
    for n in range(2,order+1):
        G=coefficients(fields+[zero()])[n]
        s=G[0][0]
        degree=max((e[0] for e in s if e[1:]==(0,0,0)),default=0)
        q=[Q(0),Q(0)]+[-s.get((k,0,0,0),Q(0))/Q((k+1)*(k+2))
                         for k in range(degree+1)]
        j=zero()
        j[1][1]=j[2][2]=profile(q)
        fields.append(j)
        if coefficients(fields)!=[zero() for _ in range(n+1)]:
            raise ArithmeticError("ansatz failed at order "+str(n))
    return fields
