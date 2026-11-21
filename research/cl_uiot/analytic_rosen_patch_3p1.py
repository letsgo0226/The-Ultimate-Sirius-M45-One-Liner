"""Exact rational Taylor solution of an affine polarized Rosen wave."""
from fractions import Fraction as Q

def metric_coefficients():
    """g11=-(1+e*u)^2, g22=-(1-e*u)^2 (both affine scale factors)."""
    return ((Q(-1),Q(-2),Q(-1)),(Q(-1),Q(2),Q(-1)))

def transverse_metric(e,u):
    x=Q(e)*Q(u)
    if abs(x)>=1:raise ValueError("restricted nonsingular patch |e*u|<1")
    return (-(1+x)**2,-(1-x)**2)
