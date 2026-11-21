"""Einstein tensor and contracted Bianchi identity on conformal 3+1 patches.

g_ab=Omega² eta_ab, eta=(+---), Omega>0.
Polynomial E_ab := Omega² G_ab = Omega² R_ab
                                  - 1/2 eta_ab Omega*(Omega³ R).
The contracted Bianchi identity is checked without polynomial division:
Omega * sum_mu eta[mu] partial_mu E_mu nu
 - sum_mu,rho eta[mu] (Omega Gamma^rho_mu nu) E_mu rho = 0.
This is a geometric identity for a prescribed conformally flat metric,
not Einstein's dynamical field equation.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,deriv
from conformal_geometry_3p1 import (
    ricci_numerator,scalar_curvature_numerator,christoffel_numerator
)

def einstein_numerator(omega,mu,nu):
    if mu not in range(4) or nu not in range(4):
        raise ValueError("indices must be 0..3")
    trace=mul(omega,scalar_curvature_numerator(omega))
    return add(ricci_numerator(omega,mu,nu),
               scale(trace,-Q(ETA[mu],2) if mu==nu else 0))

def trace_residual(omega):
    """eta^{ab} E_ab + Omega*(Omega³ R) = 0 in four dimensions."""
    return add(*(scale(einstein_numerator(omega,mu,mu),ETA[mu])
                 for mu in range(4)),
               mul(omega,scalar_curvature_numerator(omega)))

def contracted_bianchi_residual(omega,nu):
    """Polynomial form of Omega^5 nabla_mu G^mu_nu."""
    if nu not in range(4):
        raise ValueError("index must be 0..3")
    divergence=add(*(scale(deriv(einstein_numerator(omega,mu,nu),mu),
                           ETA[mu]) for mu in range(4)))
    connection=add(*(
        scale(mul(christoffel_numerator(omega,rho,mu,nu),
                  einstein_numerator(omega,mu,rho)),ETA[mu])
        for mu in range(4) for rho in range(4)))
    return add(mul(omega,divergence),scale(connection,-1))

def demo():
    omega={(0,0,0,0):Q(2),(2,0,0,0):Q(1),
           (0,0,2,0):Q(1)}
    return {
        "einstein_trace_identity":trace_residual(omega)=={},
        "contracted_bianchi_all_four_components":
            all(contracted_bianchi_residual(omega,nu)=={} for nu in range(4)),
        "nontrivial_einstein_tensor":
            any(einstein_numerator(omega,mu,nu)
                for mu in range(4) for nu in range(4)),
        "scope":"conformally flat prescribed geometry; no Einstein field equations"
    }

if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
