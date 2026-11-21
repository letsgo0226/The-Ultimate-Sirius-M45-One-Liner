"""Restricted Einstein-Hilbert first variation in conformal 3+1 geometry.

On Omega>0, g_ab=Omega² eta_ab, sqrt(-g)R=-6 Omega Box_eta Omega.
Variation is ONLY with respect to the conformal factor, not an arbitrary metric.
Exact polynomial off-shell identity includes the boundary divergence.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,deriv
from conformal_geometry_3p1 import box,scalar_curvature_numerator

def eh_density(omega):
    return scale(mul(omega,box(omega)),-6)

def first_variation(omega,delta):
    return scale(add(mul(delta,box(omega)),mul(omega,box(delta))),-6)

def boundary_current(omega,delta,mu):
    return scale(add(mul(omega,deriv(delta,mu)),
                     scale(mul(delta,deriv(omega,mu)),-1)),
                 -6*ETA[mu])

def euler_lagrange_density(omega):
    """Functional derivative after integrating by parts."""
    return scale(box(omega),-12)

def variation_residual(omega,delta):
    boundary=add(*(deriv(boundary_current(omega,delta,mu),mu)
                   for mu in range(4)))
    rhs=add(mul(delta,euler_lagrange_density(omega)),boundary)
    return add(first_variation(omega,delta),scale(rhs,-1))

def trace_relation_residual(omega):
    """EH conformal variation equals 2 Omega³ R = -12 Box Omega.

    Omega³ R is a polynomial from the independent Ricci calculation.
    """
    return add(euler_lagrange_density(omega),
               scale(scalar_curvature_numerator(omega),-2))

def demo():
    omega={(0,0,0,0):Q(2),(2,0,0,0):Q(1),
           (0,0,2,0):Q(1)}
    delta={(1,0,0,0):Q(3),(0,1,0,0):Q(2)}
    return {
        "restricted_eh_variation_identity":variation_residual(omega,delta)=={},
        "einstein_trace_consistency":trace_relation_residual(omega)=={},
        "scope":"conformal metric variation only; not full Einstein field equations"
    }

if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
