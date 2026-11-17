"""Exact 1+1 Abelian field-strength and Maxwell Euler-Lagrange model.

Metric (+,-), covariant A=(A_0,A_1), F_01=dt A_1-dx A_0.
L=-1/4 F_mu_nu F^mu_nu = +1/2 F_01^2.
Euler-Lagrange derivatives w.r.t A_nu equal ∂_mu F^{mu nu}
= (∂x F_01, -∂t F_01).
No boundary terms, field quantization or propagating photons are modeled.
"""
from fractions import Fraction as Q
from klein_gordon_1p1 import add, scale, mul, derivative

def field_strength(A):
    if len(A) != 2:
        raise ValueError("A must have 2 covariant components")
    return add(derivative(A[1], 0), scale(derivative(A[0], 1), -1))

def gauge_shift(A, chi):
    """A'_mu=A_mu+∂_mu chi; chi=-alpha/q in earlier U(1) convention."""
    return (add(A[0], derivative(chi, 0)),
            add(A[1], derivative(chi, 1)))

def lagrangian(A):
    f = field_strength(A)
    return scale(mul(f, f), Q(1,2))

def euler_lagrange(A):
    """EL[A_nu] = ∂L/∂A_nu - ∂mu(∂L/∂(∂mu A_nu))."""
    f = field_strength(A)
    return (derivative(f, 1), scale(derivative(f, 0), -1))

def maxwell_divergence(A):
    """∂_mu F^{mu nu}, nu=0,1, with metric (+,-)."""
    f = field_strength(A)
    return (derivative(f, 1), scale(derivative(f, 0), -1))

def current_conserved(j):
    """∂_nu j^nu = 0 (identity for j=∂F)."""
    return add(derivative(j[0], 0), derivative(j[1], 1)) == {}

def check_gauge_invariance(A, chi):
    return field_strength(gauge_shift(A, chi)) == field_strength(A) and (
        lagrangian(gauge_shift(A, chi)) == lagrangian(A))

def demo():
    A = ({(1,1):Q(2)}, {(2,0):Q(3),(0,1):Q(1)})
    chi = {(3,1):Q(2),(0,2):Q(1)}
    j = maxwell_divergence(A)
    return {
        "gauge_invariant": check_gauge_invariance(A,chi),
        "euler_lagrange_equals_divergence": euler_lagrange(A) == j,
        "induced_current_conserved": current_conserved(j),
        "scope": "1+1 classical Abelian polynomial identities; no propagating photon modes"
    }

if __name__ == "__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
