"""Unaveraged polynomial kernel of the TT Isaacson effective tensor.

K_ab = sum_ij partial_a h_ij partial_b h_ij.
Actual Isaacson tensor requires suitable shortwave averaging and normalization.
Here we use only local polynomial plane-wave examples, not actual averaging.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,deriv
from tt_gravity_wave_3p1 import tt_wave

def kernel(h,a,b):
    return add(*(mul(deriv(h[i][j],a),deriv(h[i][j],b))
                 for i in range(1,4) for j in range(1,4)))

def trace_kernel(h):
    return add(*(scale(kernel(h,a,a),ETA[a]) for a in range(4)))

def divergence(h,b):
    return add(*(scale(deriv(kernel(h,a,b),a),ETA[a]) for a in range(4)))

def demo():
    h=tt_wave([0,0,2],[0,0,3])
    return {"nonzero_kernel":bool(kernel(h,0,0)),
            "null_trace":trace_kernel(h)=={},
            "conserved_plane_wave_kernel":all(divergence(h,b)=={} for b in range(4)),
            "scope":"unaveraged TT plane-wave kernel only"}
