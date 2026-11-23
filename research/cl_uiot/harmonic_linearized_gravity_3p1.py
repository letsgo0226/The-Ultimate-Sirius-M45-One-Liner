"""Trace reversal and harmonic-gauge reduction of linearized gravity.

All tensors are symmetric 4x4 rational-polynomial fields, signature (+---).
For arbitrary h, G^(1)_ab = -1/2 Box bar_h_ab
 + 1/2 (partial_a C_b + partial_b C_a - eta_ab partial^rho C_rho),
C_b = partial^rho bar_h_rho b.
In harmonic gauge C=0 this becomes the linearized wave equation.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,deriv
from linearized_einstein_3p1 import validate,trace,box,einstein_linear,gauge_shift

def trace_reverse(h):
    validate(h)
    tr=trace(h)
    return [[add(h[a][b],scale(tr,-Q(ETA[a],2) if a==b else 0))
             for b in range(4)] for a in range(4)]

def harmonic_constraint(h,nu):
    bh=trace_reverse(h)
    return add(*(scale(deriv(bh[mu][nu],mu),ETA[mu])
                 for mu in range(4)))

def constraint_divergence(h):
    return add(*(scale(deriv(harmonic_constraint(h,mu),mu),ETA[mu])
                 for mu in range(4)))

def reduced_einstein(h,mu,nu):
    bh=trace_reverse(h)
    return scale(box(bh[mu][nu]),-Q(1,2))

def constraint_correction(h,mu,nu):
    return scale(add(deriv(harmonic_constraint(h,nu),mu),
                     deriv(harmonic_constraint(h,mu),nu),
                     scale(constraint_divergence(h),
                           -ETA[mu] if mu==nu else 0)),Q(1,2))

def reduction_residual(h,mu,nu):
    return add(einstein_linear(h,mu,nu),
               scale(reduced_einstein(h,mu,nu),-1),
               scale(constraint_correction(h,mu,nu),-1))

def gauge_constraint_shift_residual(xi,nu):
    """Under h -> h+partial xi+partial xi, delta C_nu=Box xi_nu."""
    return add(harmonic_constraint(gauge_shift(xi),nu),
               scale(box(xi[nu]),-1))

def demo():
    h=[[{} for _ in range(4)] for _ in range(4)]
    h[0][0]={(0,2,0,0):Q(2)}
    h[0][1]=h[1][0]={(1,1,0,0):Q(3)}
    xi=[{(2,0,0,0):Q(1)}, {}, {(0,0,2,0):Q(2)}, {}]
    return {
        "general_reduction_identity":
            all(reduction_residual(h,a,b)=={} for a in range(4) for b in range(4)),
        "gauge_constraint_transformation":
            all(gauge_constraint_shift_residual(xi,nu)=={} for nu in range(4)),
        "scope":"linearized Minkowski gravity; no physical wave solution claimed"
    }

if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
