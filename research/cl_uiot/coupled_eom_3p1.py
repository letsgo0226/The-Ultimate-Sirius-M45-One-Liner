"""Exact polynomial coupled scalar-U(1) Euler-Lagrange identities in 3+1D.

Conventions: eta=(+---), D_mu phi=partial_mu phi+q A_mu J phi,
J(a,b)=(-b,a). Matter EOM E_phi=D_mu D^mu phi + m² phi=0.
Gauge EOM div F = j, j^nu=-q (D^nu phi) dot (J phi).
Off-shell Noether identity: div j = -q E_phi dot (J phi).
These are identities for polynomial fields, not PDE solutions.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA, add, scale, mul, deriv, maxwell_divergence
from coupled_scalar_u1_3p1 import D, J, dot, vadd, vscale, vmul

def eom_scalar(phi,A,mass_squared=Q(1),q=Q(1)):
    out=({},{})
    for mu in range(4):
        out=vadd(out,vscale(D(D(phi,A,mu,q),A,mu,q),ETA[mu]))
    return vadd(out,vscale(phi,mass_squared))

def matter_current(phi,A,q=Q(1)):
    """Contravariant j^nu = -q eta^nu nu dot(D_nu phi,J phi)."""
    return tuple(scale(dot(D(phi,A,nu,q),J(phi)),-Q(q)*ETA[nu])
                 for nu in range(4))

def divergence(j):
    if len(j)!=4:
        raise ValueError("expected four current components")
    return add(*(deriv(j[mu],mu) for mu in range(4)))

def noether_residual(phi,A,mass_squared=Q(1),q=Q(1)):
    """Must vanish identically, including off shell."""
    return add(divergence(matter_current(phi,A,q)),
               scale(dot(eom_scalar(phi,A,mass_squared,q),J(phi)),q))

def gauge_equation_residual(phi,A,q=Q(1)):
    """Maxwell EL expression: div F - j (vanishes on shell)."""
    f=maxwell_divergence(A)
    j=matter_current(phi,A,q)
    return tuple(add(f[nu],scale(j[nu],-1)) for nu in range(4))

def demo():
    phi=({(1,0,0,0):Q(2),(0,1,0,0):Q(1)},
         {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})
    A=({(0,1,0,0):Q(2)}, {(1,0,0,0):Q(1)}, {},
       {(0,0,1,0):Q(3)})
    return {
        "off_shell_noether_identity":noether_residual(phi,A,Q(3),Q(2))=={},
        "matter_current_conserved_off_shell":divergence(matter_current(phi,A,Q(2)))=={},
        "gauge_equations_satisfied":all(not p for p in gauge_equation_residual(phi,A,Q(2))),
        "scope":"off-shell identity, not generic on-shell solution"
    }

if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
