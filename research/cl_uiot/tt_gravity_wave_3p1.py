"""Polynomial TT plane waves and gauge-invariant linearized tidal curvature."""
from fractions import Fraction as Q
from maxwell_3p1 import add,scale,deriv,mul
from linearized_einstein_3p1 import trace,box,gauge_shift,einstein_linear,d2
from harmonic_linearized_gravity_3p1 import harmonic_constraint

def profile(coeffs):
    u={(1,0,0,0):Q(1),(0,0,0,1):Q(-1)}
    result={}
    for c in reversed(coeffs):
        result=add(mul(result,u),{(0,0,0,0):Q(c)} if c else {})
    return result

def tt_wave(plus,cross):
    h=[[{} for _ in range(4)] for _ in range(4)]
    h[1][1]=profile(plus)
    h[2][2]=scale(h[1][1],-1)
    h[1][2]=h[2][1]=profile(cross)
    return h

def tidal(h,i,j):
    # R^(1)_0i0j for R^rho_sigma mu nu = d_mu Gamma^rho_nu sigma - d_nu Gamma^rho_mu sigma
    return scale(add(d2(h[0][j],i,0),d2(h[i][0],0,j),
                     scale(d2(h[0][0],i,j),-1),
                     scale(d2(h[i][j],0,0),-1)),Q(1,2))

def demo():
    h=tt_wave([0,0,2],[0,0,0,3])
    return {"trace_zero":trace(h)=={},
            "harmonic":all(harmonic_constraint(h,i)=={} for i in range(4)),
            "vacuum":all(einstein_linear(h,i,j)=={} for i in range(4) for j in range(4)),
            "nonzero_tidal_curvature":bool(tidal(h,1,1)),
            "scope":"local polynomial plane waves at linear order"}
if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
