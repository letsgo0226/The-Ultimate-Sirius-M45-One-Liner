"""Second-order contracted Bianchi identity, mixed-index expansion."""
from maxwell_3p1 import ETA,add,scale,mul,deriv
from linearized_einstein_3p1 import einstein_linear
from second_order_einstein_3p1 import einstein2,gamma1

I=range(4)

def divergence2(h,b):
    return add(*(scale(deriv(einstein2(h,a,b),a),ETA[a]) for a in I))

def mixed_inverse_correction(h,a,b):
    return add(*(scale(mul(h[a][s],einstein_linear(h,s,b)),
                        -ETA[a]*ETA[s]) for s in I))

def bianchi2_residual(h,b):
    return add(divergence2(h,b),
               *(deriv(mixed_inverse_correction(h,a,b),a) for a in I),
               *(scale(mul(gamma1(h,a,a,s),einstein_linear(h,s,b)),ETA[s])
                 for a in I for s in I),
               *(scale(mul(gamma1(h,s,a,b),einstein_linear(h,a,s)),-ETA[a])
                 for a in I for s in I))
