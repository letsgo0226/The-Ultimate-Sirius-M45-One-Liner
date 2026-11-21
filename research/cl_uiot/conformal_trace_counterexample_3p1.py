"""Counterexample: conformal Einstein-Hilbert stationarity != vacuum Einstein.

On a positive patch, Omega(t)=2+t has Box_eta Omega=0 and hence
the restricted conformal EH Euler-Lagrange derivative vanishes.
Yet its Einstein tensor is nonzero, so the full vacuum equations fail.
All expressions are exact rational polynomials.
"""
from fractions import Fraction as Q
from conformal_geometry_3p1 import box,scalar_curvature_numerator
from conformal_einstein_hilbert_3p1 import euler_lagrange_density,variation_residual
from conformal_einstein_bianchi_3p1 import (
    einstein_numerator,trace_residual,contracted_bianchi_residual
)

def example():
    omega={(0,0,0,0):Q(2),(1,0,0,0):Q(1)}
    delta={(2,0,0,0):Q(3),(0,1,0,0):Q(2)}
    return {
        "omega":omega,
        "restricted_eom_zero":euler_lagrange_density(omega)=={},
        "ricci_scalar_zero":scalar_curvature_numerator(omega)=={},
        "nonzero_einstein_components":[
            (mu,nu,einstein_numerator(omega,mu,nu))
            for mu in range(4) for nu in range(4)
            if einstein_numerator(omega,mu,nu)
        ],
        "trace_identity":trace_residual(omega)=={},
        "bianchi_identity":all(
            contracted_bianchi_residual(omega,nu)=={} for nu in range(4)),
        "variational_identity":variation_residual(omega,delta)=={}
    }

def demo():
    result=example()
    return {
        "restricted_eom_zero":result["restricted_eom_zero"],
        "scalar_curvature_zero":result["ricci_scalar_zero"],
        "full_vacuum_einstein_equation_fails":
            bool(result["nonzero_einstein_components"]),
        "geometric_consistency":result["trace_identity"] and
            result["bianchi_identity"] and result["variational_identity"],
        "scope":"counterexample on patch t>-2, not a gravity solution"
    }

if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
