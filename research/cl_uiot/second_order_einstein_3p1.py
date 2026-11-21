"""Second-order Einstein coefficient for g=eta+epsilon*h, exact polynomials."""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,deriv
from linearized_einstein_3p1 import validate,ricci_linear,scalar_linear

I=range(4)
def gamma1(h,r,a,b):
    return scale(add(deriv(h[r][b],a),deriv(h[r][a],b),
                     scale(deriv(h[a][b],r),-1)),Q(ETA[r],2))

def gamma2(h,r,a,b):
    return add(*(scale(mul(h[r][s],gamma1(h,s,a,b)),-ETA[r]) for s in I))

def ricci2(h,a,b):
    return add(*(add(deriv(gamma2(h,r,a,b),r),
                     scale(deriv(gamma2(h,r,a,r),b),-1),
                     *(add(mul(gamma1(h,r,r,s),gamma1(h,s,a,b)),
                           scale(mul(gamma1(h,r,b,s),gamma1(h,s,a,r)),-1))
                       for s in I)) for r in I))

def scalar2(h):
    return add(*(scale(ricci2(h,a,a),ETA[a]) for a in I),
               *(scale(mul(h[a][b],ricci_linear(h,a,b)),-ETA[a]*ETA[b])
                 for a in I for b in I))

def einstein2(h,a,b):
    validate(h)
    return add(ricci2(h,a,b),
               scale(scalar2(h),-Q(ETA[a],2) if a==b else 0),
               scale(mul(h[a][b],scalar_linear(h)),-Q(1,2)))
