"""Polynomial Brinkmann metric in Cartesian-like (t,X,Y,z) coordinates."""
from fractions import Fraction as Q
from maxwell_3p1 import add,mul,scale,deriv
from tt_gravity_wave_3p1 import profile
from formal_einstein_3p1 import coefficients

def perturbation(k):
    # ds²=du dv-dX²-dY²+K(u)(X²-Y²)du²
    H=mul(profile(k),{(0,2,0,0):Q(1),(0,0,2,0):Q(-1)})
    l=(1,0,0,-1)
    return [[scale(H,a*b) for b in l] for a in l]

def transverse_laplacian(k):
    H=perturbation(k)[0][0]
    return add(deriv(deriv(H,1),1),deriv(deriv(H,2),2))

def curvature_components(k):
    # R_uXuX=-H_XX/2, R_uYuY=-H_YY/2
    H=perturbation(k)[0][0]
    return tuple(scale(deriv(deriv(H,i),i),-Q(1,2)) for i in (1,2))

def pullback_residual(A,Ap,App,B,Bp,Bpp,K):
    """Pointwise du² coefficient after X=A*x,Y=B*y,V=v+A*A'*x²+B*B'*y²."""
    A,Ap,App,B,Bp,Bpp,K=map(Q,(A,Ap,App,B,Bp,Bpp,K))
    return A*(App+K*A),B*(Bpp-K*B)

def determinant():
    # Null rank-one update, matrix determinant lemma, eta^ab l_a l_b=0.
    return Q(-1)
