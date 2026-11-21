"""Exact polynomial numerator identities for a 3+1 conformal metric.

g_ab=Omega² eta_ab, eta=diag(+---), on patches Omega>0.
Return Omega*Gamma^rho_ab, Omega²*Ricci_ab and Omega³*R,
avoiding rational-function denominators. This is prescribed geometry.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,deriv
from conformal_scalar_3p1 import power,eom_density

def box(p):
    return add(*(scale(deriv(deriv(p,mu),mu),ETA[mu]) for mu in range(4)))

def gradient_norm(p):
    return add(*(scale(mul(deriv(p,mu),deriv(p,mu)),ETA[mu]) for mu in range(4)))

def christoffel_numerator(omega,rho,mu,nu):
    """Omega Gamma^rho_{mu nu}."""
    return add(scale(deriv(omega,nu),int(rho==mu)),
               scale(deriv(omega,mu),int(rho==nu)),
               scale(deriv(omega,rho),-int(mu==nu)*ETA[mu]*ETA[rho]))

def ricci_numerator(omega,mu,nu):
    """Omega² R_mu nu, signature +---."""
    first=scale(mul(omega,deriv(deriv(omega,mu),nu)),-2)
    second=scale(mul(deriv(omega,mu),deriv(omega,nu)),4)
    trace=add(mul(omega,box(omega)),gradient_norm(omega))
    return add(first,second,scale(trace,-int(mu==nu)*ETA[mu]))

def scalar_curvature_numerator(omega):
    """Omega³ R = -6 box_eta(Omega)."""
    return scale(box(omega),-6)

def contracted_ricci_numerator(omega):
    """eta^{mu nu} (Omega² Ricci_mu nu) = Omega⁴ R = Omega*(-6 box Omega)."""
    return add(*(scale(ricci_numerator(omega,mu,mu),ETA[mu])
                 for mu in range(4)))

def contraction_residual(omega):
    return add(contracted_ricci_numerator(omega),
               scale(mul(omega,scalar_curvature_numerator(omega)),-1))

def scalar_wave_relation(phi,omega,mass_squared=Q(1)):
    """Check densitized curved scalar EOM = Omega⁴ (Box_g+m²)phi.

    For scalar Box_g phi=Omega^-2 box_eta phi
                       +2 Omega^-3 partial Omega·partial phi.
    Return numerator difference (should be zero).
    """
    out=[]
    for comp in phi:
        gradient=add(*(scale(mul(deriv(omega,mu),deriv(comp,mu)),ETA[mu])
                       for mu in range(4)))
        expression=add(mul(power(omega,2),box(comp)),
                       scale(mul(omega,gradient),2),
                       scale(mul(power(omega,4),comp),mass_squared))
        out.append(expression)
    actual=eom_density(phi,omega,mass_squared)
    return tuple(add(actual[i],scale(out[i],-1)) for i in range(2))

def demo():
    omega={(0,0,0,0):Q(2),(2,0,0,0):Q(1),
           (0,0,2,0):Q(1)}
    phi=({(1,0,0,0):Q(2)}, {(0,1,0,1):Q(3)})
    return {
        "ricci_contraction":contraction_residual(omega)=={},
        "curved_scalar_wave_identity":scalar_wave_relation(phi,omega,Q(3))==({},{}),
        "nonzero_curvature_numerator":bool(scalar_curvature_numerator(omega)),
        "scope":"conformally flat prescribed background, no Einstein equations"
    }

if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
