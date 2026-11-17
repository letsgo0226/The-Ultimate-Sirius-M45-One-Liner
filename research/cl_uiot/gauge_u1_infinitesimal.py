"""Infinitesimal U(1) gauge covariance of a real scalar doublet.

Exact polynomial arithmetic over rationals. The real 2-vector represents
a complex scalar; J(a,b)=(-b,a) and J²=-I. For D_mu=∂_mu+q A_mu J,
delta phi=alpha J phi, delta A_mu=-(∂_mu alpha)/q,
one finds delta(D_mu phi)=alpha J(D_mu phi) to FIRST ORDER in alpha.

This verifies an algebraic first-order identity, not finite gauge
transformations, quantum electrodynamics, or a unified field theory.
"""
from fractions import Fraction as Q
from klein_gordon_1p1 import add, mul, scale, derivative

ZERO = {}
def vadd(a,b):
    return (add(a[0],b[0]), add(a[1],b[1]))
def vscale(a,c):
    return (scale(a[0],c),scale(a[1],c))
def pmulvec(p,v):
    return (mul(p,v[0]),mul(p,v[1]))
def J(v):
    return (scale(v[1],-1),v[0])
def dv(v,mu):
    return (derivative(v[0],mu),derivative(v[1],mu))
def covariant(v, A, mu, q=Q(1)):
    if q == 0:
        raise ValueError("q must be nonzero for this transformation law")
    return vadd(dv(v,mu),vscale(pmulvec(A[mu],J(v)),q))
def gauge_variation(v, alpha):
    return pmulvec(alpha,J(v))
def gauge_potential_variation(alpha, mu, q=Q(1)):
    if q == 0:
        raise ValueError("q must be nonzero")
    return scale(derivative(alpha,mu),-Q(1)/q)
def check_infinitesimal_covariance(v,A,alpha,mu,q=Q(1)):
    # Linearization: δ(Dv)=D(δv)+q δA Jv.
    delta_v = gauge_variation(v,alpha)
    delta_A = gauge_potential_variation(alpha,mu,q)
    lhs = vadd(covariant(delta_v,A,mu,q),
               vscale(pmulvec(delta_A,J(v)),q))
    rhs = gauge_variation(covariant(v,A,mu,q),alpha)
    return lhs == rhs
def demo():
    v = ({(2,0):Q(2),(0,1):Q(3)}, {(1,1):Q(1),(0,0):Q(4)})
    A = ({(1,0):Q(2)}, {(0,1):Q(-1)})
    alpha = {(1,1):Q(2),(1,0):Q(1)}
    return {"first_order_gauge_covariance": all(
        check_infinitesimal_covariance(v,A,alpha,mu,Q(2))
        for mu in (0,1)),
        "scope":"exact infinitesimal U(1) doublet algebra; no finite-gauge or quantum proof"}
if __name__ == "__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
