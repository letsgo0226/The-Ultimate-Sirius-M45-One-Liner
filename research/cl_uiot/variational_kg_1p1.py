"""Exact polynomial Euler-Lagrange check for the free scalar field in 1+1D.

L(phi,phi_t,phi_x) = 1/2(phi_t^2 - phi_x^2 - m^2 phi^2).
Euler-Lagrange expression dL/dphi - dt(dL/dphi_t) - dx(dL/dphi_x)
= -(box + m^2) phi.

This is a symbolic identity on polynomial fields, not an integral action,
boundary-value existence theorem, quantum field theory, or unified physics.
"""
from fractions import Fraction as Q
from klein_gordon_1p1 import add, scale, mul, derivative, kg, pullback
from lorentz_1p1 import boost

def lagrangian(phi, mass_squared=Q(1)):
    dt = derivative(phi, 0)
    dx = derivative(phi, 1)
    return scale(add(mul(dt, dt), scale(mul(dx, dx), -1),
                     scale(mul(phi, phi), -Q(mass_squared))), Q(1, 2))

def euler_lagrange(phi, mass_squared=Q(1)):
    """Compute dL/dphi - dt(dL/dphi_t) - dx(dL/dphi_x)."""
    m2 = Q(mass_squared)
    dL_dphi = scale(phi, -m2)
    dL_dphit = derivative(phi, 0)
    dL_dphix = scale(derivative(phi, 1), -1)
    return add(dL_dphi,
               scale(derivative(dL_dphit, 0), -1),
               scale(derivative(dL_dphix, 1), -1))

def check_variational_identity(phi, mass_squared=Q(1)):
    return euler_lagrange(phi, mass_squared) == scale(kg(phi, mass_squared), -1)

def check_lagrangian_covariance(phi, v=Q(3, 5), mass_squared=Q(1)):
    """Lorentz scalar density at transformed coordinates (det B = 1)."""
    inv = boost(-v)
    return lagrangian(pullback(phi, inv), mass_squared) == pullback(
        lagrangian(phi, mass_squared), inv)

def demo():
    phi = {(3, 1): Q(2), (0, 2): Q(3), (1, 0): Q(-1), (0, 0): Q(7)}
    return {
        "field": "2*t^3*x + 3*x^2 - t + 7",
        "euler_lagrange_equals_negative_kg": check_variational_identity(phi),
        "lagrangian_lorentz_covariant": check_lagrangian_covariance(phi),
        "scope": "exact free-scalar polynomial identity; no boundary terms modeled"
    }

if __name__ == "__main__":
    import json
    print(json.dumps(demo(), sort_keys=True))
