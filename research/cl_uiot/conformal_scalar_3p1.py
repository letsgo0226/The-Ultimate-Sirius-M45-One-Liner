"""Exact conformally-flat curved-background scalar action (3+1).

g_mu_nu=Omega(x)^2 eta_mu_nu, sqrt(-g)=Omega^4 (Omega>0).
The densitized free scalar Lagrangian is
 L_density=1/2 Omega² eta^mu nu ∂_mu phi·∂_nu phi
           -1/2 Omega⁴ m² phi·phi.
Its Euler-Lagrange density is
 E_density=∂_mu(Omega² eta^mu nu ∂_nu phi)+Omega⁴ m² phi.
This checks a nonconstant background and a local variational identity;
it does not solve Einstein equations or implement arbitrary metrics.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,deriv
from coupled_scalar_u1_3p1 import dot

def power(p,n):
    if n<0:raise ValueError("nonnegative polynomial power required")
    out={(0,0,0,0):Q(1)}
    for _ in range(n):out=mul(out,p)
    return out

def gradient(phi,mu):
    return (deriv(phi[0],mu),deriv(phi[1],mu))

def density(phi,omega,mass_squared=Q(1)):
    omega2=power(omega,2)
    omega4=mul(omega2,omega2)
    kinetic=add(*(scale(mul(omega2,dot(gradient(phi,mu),gradient(phi,mu))),
                       Q(ETA[mu],2)) for mu in range(4)))
    return add(kinetic,scale(mul(omega4,dot(phi,phi)),-Q(mass_squared,2)))

def eom_density(phi,omega,mass_squared=Q(1)):
    omega2=power(omega,2)
    omega4=mul(omega2,omega2)
    return tuple(add(
        *(scale(deriv(mul(omega2,deriv(comp,mu)),mu),ETA[mu])
          for mu in range(4)),
        scale(mul(omega4,comp),mass_squared)) for comp in phi)

def first_variation(phi,delta_phi,omega,mass_squared=Q(1)):
    omega2=power(omega,2)
    omega4=mul(omega2,omega2)
    kinetic=add(*(scale(mul(omega2,dot(gradient(phi,mu),gradient(delta_phi,mu))),
                       ETA[mu]) for mu in range(4)))
    mass=scale(mul(omega4,dot(phi,delta_phi)),-mass_squared)
    return add(kinetic,mass)

def boundary_current(phi,delta_phi,omega,mu):
    return scale(mul(power(omega,2),dot(gradient(phi,mu),delta_phi)),ETA[mu])

def variational_residual(phi,delta_phi,omega,mass_squared=Q(1)):
    # delta L + delta phi·E - ∂_mu(omega² ∂^mu phi·delta phi) = 0
    boundary=add(*(deriv(boundary_current(phi,delta_phi,omega,mu),mu)
                   for mu in range(4)))
    return add(first_variation(phi,delta_phi,omega,mass_squared),
               dot(delta_phi,eom_density(phi,omega,mass_squared)),
               scale(boundary,-1))

def demo():
    phi=({(2,0,0,0):Q(2)}, {(0,1,0,0):Q(3)})
    variation=({(0,0,1,0):Q(1)}, {(1,0,0,1):Q(2)})
    omega={(0,0,0,0):Q(1),(1,0,0,0):Q(1)}
    return {"nonconstant_conformal_variational_identity":
            variational_residual(phi,variation,omega,Q(3))=={},
            "scope":"curved-background scalar density; no dynamical gravity"}
if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
