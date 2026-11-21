"""Independent algebraic metric-variation audit of the coupled stress tensor.

At flat g^{mu nu}=diag(+---), vary a symmetric inverse metric component.
For L=1/2 g^{ab} D_a phi·D_b phi - m² phi²/2
       -1/4 g^{ac}g^{bd}F_ab F_cd,
the Hilbert tensor is T_ab=2 dL/dg^{ab}-g_ab L.
Off-diagonal symmetric variation counts both g^{ab} and g^{ba}, so
T_ab=dL/d(epsilon) there; diagonal variation uses 2*dL/d(epsilon).
This checks algebra at a flat metric, not curved-spacetime dynamics.
"""
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add,scale,mul,strength
from coupled_scalar_u1_3p1 import D,dot
from stress_energy_coupled_3p1 import total_stress

def metric_lagrangian(phi,A,g,mass_squared=Q(1),q=Q(1)):
    kinetic={}
    for a in range(4):
        for b in range(4):
            if g[a][b]:
                kinetic=add(kinetic,scale(dot(D(phi,A,a,q),D(phi,A,b,q)),Q(g[a][b],2)))
    mass=scale(dot(phi,phi),-Q(mass_squared,2))
    gauge={}
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    if g[a][c] and g[b][d]:
                        gauge=add(gauge,scale(mul(strength(A,a,b),strength(A,c,d)),
                            -Q(g[a][c]*g[b][d],4)))
    return add(kinetic,mass,gauge)

def varied_metric(mu,nu,eps):
    g=[[Q(ETA[a] if a==b else 0) for b in range(4)] for a in range(4)]
    g[mu][nu]+=eps
    if mu!=nu:g[nu][mu]+=eps
    return g

def metric_stress_component(phi,A,mu,nu,mass_squared=Q(1),q=Q(1)):
    plus=metric_lagrangian(phi,A,varied_metric(mu,nu,Q(1)),mass_squared,q)
    minus=metric_lagrangian(phi,A,varied_metric(mu,nu,Q(-1)),mass_squared,q)
    # Quadratic metric dependence means symmetric difference is exact.
    deriv=scale(add(plus,scale(minus,-1)),Q(1,2))
    baseline=metric_lagrangian(phi,A,varied_metric(mu,nu,Q(0)),mass_squared,q)
    return add(scale(deriv,2 if mu==nu else 1),
               scale(baseline,-ETA[mu] if mu==nu else 0))

def check_metric_variation(phi,A,mass_squared=Q(1),q=Q(1)):
    for mu in range(4):
        for nu in range(4):
            expected=scale(total_stress(phi,A,mu,nu,mass_squared,q),ETA[mu])
            if metric_stress_component(phi,A,mu,nu,mass_squared,q)!=expected:
                return False
    return True

def demo():
    phi=({(1,0,0,0):Q(2),(0,1,0,0):Q(1)},
         {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})
    A=({(0,1,0,0):Q(2)}, {(1,0,0,0):Q(1)}, {},
       {(0,0,1,0):Q(3)})
    return {"all_16_components_match":check_metric_variation(phi,A,Q(3),Q(2)),
            "scope":"exact flat-metric algebra audit; no curved geometry or Einstein equations"}
if __name__=="__main__":
    import json
    print(json.dumps(demo(),sort_keys=True))
