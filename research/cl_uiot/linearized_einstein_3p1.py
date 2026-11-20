"""Linearized Einstein tensor for arbitrary symmetric polynomial h_ab in 3+1.

g_ab=eta_ab+epsilon h_ab, eta=(+---). Exact rational polynomial
linear order only. Gauge h_ab -> h_ab + d_a xi_b + d_b xi_a.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,deriv

def validate(h):
    if len(h)!=4 or any(len(row)!=4 for row in h):
        raise ValueError("h must be 4x4")
    if any(h[a][b]!=h[b][a] for a in range(4) for b in range(4)):
        raise ValueError("h must be symmetric")

def d2(p,a,b):
    return deriv(deriv(p,a),b)

def trace(h):
    validate(h)
    return add(*(scale(h[a][a],ETA[a]) for a in range(4)))

def box(p):
    return add(*(scale(d2(p,a,a),ETA[a]) for a in range(4)))

def ricci_linear(h,mu,nu):
    validate(h)
    if mu not in range(4) or nu not in range(4):
        raise ValueError("indices must be 0..3")
    term1=add(*(scale(d2(h[rho][nu],rho,mu),ETA[rho]) for rho in range(4)))
    term2=add(*(scale(d2(h[rho][mu],rho,nu),ETA[rho]) for rho in range(4)))
    return scale(add(term1,term2,scale(d2(trace(h),mu,nu),-1),
                     scale(box(h[mu][nu]),-1)),Q(1,2))

def scalar_linear(h):
    return add(*(scale(ricci_linear(h,mu,mu),ETA[mu]) for mu in range(4)))

def einstein_linear(h,mu,nu):
    return add(ricci_linear(h,mu,nu),
               scale(scalar_linear(h),-Q(ETA[mu],2) if mu==nu else 0))

def bianchi_residual(h,nu):
    return add(*(scale(deriv(einstein_linear(h,mu,nu),mu),ETA[mu])
                 for mu in range(4)))

def gauge_shift(xi):
    if len(xi)!=4:raise ValueError("xi must have four components")
    return [[add(deriv(xi[b],a),deriv(xi[a],b))
             for b in range(4)] for a in range(4)]

def gauge_residual(xi,mu,nu):
    return einstein_linear(gauge_shift(xi),mu,nu)

def demo():
    z={}
    h=[[z for _ in range(4)] for _ in range(4)]
    h[0][0]={(0,2,0,0):Q(2)}
    h[0][1]=h[1][0]={(1,1,0,0):Q(3)}
    xi=[{(2,0,0,0):Q(1)}, {}, {(0,0,2,0):Q(2)}, {}]
    return {
        "linearized_bianchi":all(bianchi_residual(h,nu)=={} for nu in range(4)),
        "gauge_invariance":all(gauge_residual(xi,mu,nu)=={}
                               for mu in range(4) for nu in range(4)),
        "nontrivial_linearized_einstein":
            any(einstein_linear(h,mu,nu) for mu in range(4) for nu in range(4)),
        "scope":"linear order around Minkowski only"
    }
if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
