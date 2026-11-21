"""Exact rational 1+1 Lorentz-covariance demonstration.

Metric diag(+1,-1); c=1. Proper boost B=[[gamma,-gamma*v],
[-gamma*v,gamma]]. Verify B^T eta B=eta and mass shell E²-p²=m².
This does not implement or solve the Klein-Gordon PDE.
"""
from fractions import Fraction as Q

def boost(v):
    v = Q(v)
    # For exact rational examples gamma must be supplied as a rational.
    if v == Q(3, 5):
        return ((Q(5, 4), Q(-3, 4)), (Q(-3, 4), Q(5, 4)))
    if v == Q(-3, 5):
        return ((Q(5, 4), Q(3, 4)), (Q(3, 4), Q(5, 4)))
    if v == 0:
        return ((Q(1), Q(0)), (Q(0), Q(1)))
    raise ValueError("Only exact rational demonstration boosts v=0, ±3/5 supported")

def apply(m, x):
    if len(x) != 2:
        raise ValueError("expected a 1+1 vector")
    return (m[0][0]*x[0]+m[0][1]*x[1],
            m[1][0]*x[0]+m[1][1]*x[1])

def minkowski_square(x):
    return x[0]*x[0] - x[1]*x[1]

def lorentz_invariant(b):
    basis = ((Q(1), Q(0)), (Q(0), Q(1)), (Q(1), Q(1)))
    return all(minkowski_square(apply(b, x)) == minkowski_square(x)
               for x in basis)

def mass_shell(energy, momentum, mass):
    return energy*energy - momentum*momentum == mass*mass

def demo():
    b = boost(Q(3, 5))
    k = (Q(5), Q(3))
    transformed = apply(b, k)
    return {
        "boost": [[str(z) for z in row] for row in b],
        "four_momentum_before": [str(z) for z in k],
        "four_momentum_after": [str(z) for z in transformed],
        "mass_shell_before": mass_shell(*k, Q(4)),
        "mass_shell_after": mass_shell(*transformed, Q(4)),
        "lorentz_invariant": lorentz_invariant(b),
        "scope": "1+1 exact algebraic example; not a PDE or physical ToE"
    }

if __name__ == "__main__":
    import json
    print(json.dumps(demo(), sort_keys=True))
