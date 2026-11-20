"""Local second-order correction for polynomial TT waves traveling along +z."""
from fractions import Fraction as Q
from maxwell_3p1 import add,scale
from tt_gravity_wave_3p1 import tt_wave,profile
from second_order_einstein_3p1 import einstein2
from linearized_einstein_3p1 import einstein_linear

def correction(plus,cross):
    h=tt_wave(plus,cross)
    # G2_00 = S(t-z). Extract S at z=x=y=0.
    s=einstein2(h,0,0)
    degree=max((e[0] for e in s if e[1:]==(0,0,0)),default=0)
    # j_11=j_22=q(u) gives G1_ab=q'' k_a k_b.
    q=[Q(0),Q(0)]+[-s.get((n,0,0,0),Q(0))/Q((n+1)*(n+2))
                     for n in range(degree+1)]
    j=[[{} for _ in range(4)] for _ in range(4)]
    j[1][1]=j[2][2]=profile(q)
    return j

def residual(plus,cross,a,b):
    return add(einstein_linear(correction(plus,cross),a,b),
               einstein2(tt_wave(plus,cross),a,b))
