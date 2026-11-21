"""Exact 3+1 translation Noether stress tensor for a free real scalar doublet.

Signature (+---), L=1/2 sum_mu eta[mu] |partial_mu phi|^2
-1/2 m^2 |phi|^2.
Canonical mixed tensor T^mu_nu = eta[mu] (partial_mu phi)·(partial_nu phi)
- delta^mu_nu L.
Off-shell: partial_mu T^mu_nu = (box phi+m^2 phi)·partial_nu phi.
Note: this is the FREE scalar limit, not the interacting gauge-field tensor.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA, add, scale, mul, deriv
from coupled_scalar_u1_3p1 import dot

def partial(phi,mu):
    return (deriv(phi[0],mu),deriv(phi[1],mu))

def free_lagrangian(phi,mass_squared=Q(1)):
    kinetic=add(*(scale(dot(partial(phi,mu),partial(phi,mu)),
                        Q(ETA[mu],2)) for mu in range(4)))
    return add(kinetic,scale(dot(phi,phi),-Q(mass_squared)/2))

def free_eom(phi,mass_squared=Q(1)):
    return tuple(add(*(scale(deriv(deriv(comp,mu),mu),ETA[mu])
                       for mu in range(4)),
                     scale(comp,mass_squared)) for comp in phi)

def stress(phi,mu,nu,mass_squared=Q(1)):
    if mu not in range(4) or nu not in range(4):
        raise ValueError("indices must be 0..3")
    return add(scale(dot(partial(phi,mu),partial(phi,nu)),ETA[mu]),
               scale(free_lagrangian(phi,mass_squared),-int(mu==nu)))

def divergence_stress(phi,nu,mass_squared=Q(1)):
    return add(*(deriv(stress(phi,mu,nu,mass_squared),mu)
                 for mu in range(4)))

def noether_residual(phi,nu,mass_squared=Q(1)):
    return add(divergence_stress(phi,nu,mass_squared),
               scale(dot(free_eom(phi,mass_squared),partial(phi,nu)),-1))

def demo():
    phi=({(2,0,0,0):Q(2),(0,1,0,0):Q(1)},
         {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})
    on_shell=({(1,0,0,0):Q(2)}, {(0,1,0,0):Q(3)})
    return {
        "off_shell_translation_noether_identity":
            all(noether_residual(phi,nu,Q(3))=={} for nu in range(4)),
        "massless_linear_field_on_shell":
            free_eom(on_shell,Q(0))==({},{}),
        "on_shell_stress_conserved":
            all(divergence_stress(on_shell,nu,Q(0))=={} for nu in range(4)),
        "scope":"free scalar doublet, exact polynomials; coupled gauge stress not yet modeled"
    }

if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
