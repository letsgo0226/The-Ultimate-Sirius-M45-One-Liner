"""3+1 classical scalar-doublet + Abelian gauge-field action, exact polynomials.

L = 1/2 sum_mu eta[mu] |D_mu phi|² - 1/2 m² |phi|²
    - 1/4 F_mu_nu F^mu_nu
with D_mu phi=partial_mu phi+q A_mu J phi, J(a,b)=(-b,a).
Under delta phi=alpha J phi, delta A_mu=-partial_mu alpha/q,
the FIRST-ORDER variation of the full Lagrangian vanishes.

This is an algebraic check, not a dynamical Euler-Lagrange solver or QED.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA, add, scale, mul, deriv, lagrangian as gauge_lagrangian

def vadd(u,v):
    return (add(u[0],v[0]),add(u[1],v[1]))
def vscale(u,a):
    return (scale(u[0],a),scale(u[1],a))
def vmul(p,u):
    return (mul(p,u[0]),mul(p,u[1]))
def dot(u,v):
    return add(mul(u[0],v[0]),mul(u[1],v[1]))
def J(u):
    return (scale(u[1],-1),u[0])
def D(u,A,mu,q=Q(1)):
    if q==0:raise ValueError("charge q must be nonzero")
    return vadd((deriv(u[0],mu),deriv(u[1],mu)),
                vscale(vmul(A[mu],J(u)),q))
def matter_lagrangian(u,A,mass_squared=Q(1),q=Q(1)):
    kinetic=add(*(scale(dot(D(u,A,mu,q),D(u,A,mu,q)),Q(ETA[mu],2))
                  for mu in range(4)))
    return add(kinetic,scale(dot(u,u),-Q(mass_squared,2)))
def coupled_lagrangian(u,A,mass_squared=Q(1),q=Q(1)):
    return add(matter_lagrangian(u,A,mass_squared,q),gauge_lagrangian(A))
def delta_u(u,alpha):
    return vmul(alpha,J(u))
def delta_A(alpha,q=Q(1)):
    if q==0:raise ValueError("charge q must be nonzero")
    return tuple(scale(deriv(alpha,mu),-Q(1)/q) for mu in range(4))
def delta_D(u,A,alpha,mu,q=Q(1)):
    """First-order delta(D_mu u)=D_mu(delta u)+q delta A_mu J u."""
    du=delta_u(u,alpha)
    dA=delta_A(alpha,q)
    return vadd(D(du,A,mu,q),vscale(vmul(dA[mu],J(u)),q))
def first_order_lagrangian_variation(u,A,alpha,mass_squared=Q(1),q=Q(1)):
    du=delta_u(u,alpha)
    kinetic=add(*(scale(dot(D(u,A,mu,q),delta_D(u,A,alpha,mu,q)),ETA[mu])
                  for mu in range(4)))
    mass=scale(dot(u,du),-Q(mass_squared))
    # Gauge sector: delta F_mu_nu = d_mu delta A_nu - d_nu delta A_mu = 0.
    return add(kinetic,mass)
def check_covariance(u,A,alpha,q=Q(1)):
    return all(delta_D(u,A,alpha,mu,q)==vmul(alpha,J(D(u,A,mu,q)))
               for mu in range(4))
def demo():
    u=({(2,0,0,0):Q(2),(0,1,0,0):Q(1)},
       {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})
    A=({(0,1,0,0):Q(2)}, {(1,0,0,0):Q(1)}, {}, {(0,0,1,0):Q(3)})
    alpha={(1,1,0,0):Q(2),(0,0,0,1):Q(1)}
    return {"dimension":"3+1",
            "covariant_derivative_first_order":check_covariance(u,A,alpha,Q(2)),
            "coupled_lagrangian_first_order_invariant":
                first_order_lagrangian_variation(u,A,alpha,Q(3),Q(2))=={},
            "scope":"classical infinitesimal U(1) algebra, not QED or a unified theory"}
if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
