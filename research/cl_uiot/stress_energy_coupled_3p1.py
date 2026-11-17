"""Exact polynomial total symmetric stress tensor: coupled scalar + U(1).

Signature (+---). Mixed T^mu_nu:
  eta[mu] D_mu phi·D_nu phi
  - sum_rho eta[mu]eta[rho] F_mu rho F_nu rho
  - delta^mu_nu (L_matter + L_gauge).

Off-shell identity:
  ∂_mu T^mu_nu = E_phi·D_nu phi - R_A^rho F_nu rho
where E_phi=D_mu D^mu phi + m²phi and R_A^rho=∂_mu F^{mu rho}-j^rho.
All operations are exact rational polynomials; not a PDE solver.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,deriv,strength
from coupled_scalar_u1_3p1 import D,dot,matter_lagrangian
from maxwell_3p1 import lagrangian as gauge_lagrangian
from coupled_eom_3p1 import eom_scalar,gauge_equation_residual

def total_stress(phi,A,mu,nu,mass_squared=Q(1),q=Q(1)):
    if mu not in range(4) or nu not in range(4):
        raise ValueError("indices must be 0..3")
    matter=scale(dot(D(phi,A,mu,q),D(phi,A,nu,q)),ETA[mu])
    electromagnetic=add(*(
        scale(mul(strength(A,mu,rho),strength(A,nu,rho)),
              -ETA[mu]*ETA[rho]) for rho in range(4) if rho!=mu and rho!=nu))
    L=add(matter_lagrangian(phi,A,mass_squared,q),gauge_lagrangian(A))
    return add(matter,electromagnetic,scale(L,-int(mu==nu)))

def stress_divergence(phi,A,nu,mass_squared=Q(1),q=Q(1)):
    return add(*(deriv(total_stress(phi,A,mu,nu,mass_squared,q),mu)
                 for mu in range(4)))

def noether_residual(phi,A,nu,mass_squared=Q(1),q=Q(1)):
    scalar_term=dot(eom_scalar(phi,A,mass_squared,q),D(phi,A,nu,q))
    gauge_res=gauge_equation_residual(phi,A,q)
    force=add(*(mul(gauge_res[rho],strength(A,nu,rho))
                for rho in range(4) if rho!=nu))
    rhs=add(scalar_term,scale(force,-1))
    return add(stress_divergence(phi,A,nu,mass_squared,q),scale(rhs,-1))

def demo():
    phi=({(1,0,0,0):Q(2),(0,1,0,0):Q(1)},
         {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})
    A=({(0,1,0,0):Q(2)}, {(1,0,0,0):Q(1)}, {},
       {(0,0,1,0):Q(3)})
    return {"off_shell_total_stress_identity":
            all(noether_residual(phi,A,nu,Q(3),Q(2))=={} for nu in range(4)),
            "scope":"classical coupled gauge-invariant stress tensor; polynomial identity only"}

if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
