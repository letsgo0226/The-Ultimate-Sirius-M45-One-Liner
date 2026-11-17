"""Exact polynomial Klein-Gordon covariance under a 1+1 Lorentz boost.

Uses rational polynomial coefficient dictionaries and direct chain rule.
Metric diag(1,-1); scalar field transforms as phi'(x')=phi(B^{-1}x').
No symbolic algebra dependency, numerical approximation, or physics ToE claim.
"""
from fractions import Fraction as Q
from lorentz_1p1 import boost

# Polynomials in (t,x): (power_t,power_x) -> rational coefficient.
def normalize(p):
    return {k: Q(v) for k, v in p.items() if v != 0}

def add(*polys):
    out = {}
    for p in polys:
        for k, v in p.items():
            out[k] = out.get(k, Q(0)) + v
    return normalize(out)

def scale(p, a):
    return normalize({k: Q(a)*v for k, v in p.items()})

def mul(a, b):
    out = {}
    for (i,j), c in a.items():
        for (k,l), d in b.items():
            key = (i+k,j+l)
            out[key] = out.get(key, Q(0)) + c*d
    return normalize(out)

def power(p, n):
    out = {(0,0): Q(1)}
    for _ in range(n):
        out = mul(out,p)
    return out

def derivative(p, axis):
    out = {}
    for (i,j), c in p.items():
        if axis == 0 and i:
            out[(i-1,j)] = c*i
        elif axis == 1 and j:
            out[(i,j-1)] = c*j
    return normalize(out)

def box(p):
    return add(derivative(derivative(p,0),0),
               scale(derivative(derivative(p,1),1), -1))

def kg(p, mass_squared=Q(1)):
    return add(box(p), scale(p, mass_squared))

def pullback(p, b_inverse):
    """Substitute (t,x)=B^{-1}(t',x') into a scalar field polynomial."""
    t = {(1,0): Q(b_inverse[0][0]), (0,1): Q(b_inverse[0][1])}
    x = {(1,0): Q(b_inverse[1][0]), (0,1): Q(b_inverse[1][1])}
    out = {}
    for (i,j), c in p.items():
        out = add(out, scale(mul(power(t,i),power(x,j)),c))
    return out

def check_covariance(p, v=Q(3,5), mass_squared=Q(1)):
    # B(v)^(-1) = B(-v), using exact rational boosts.
    inv = boost(-v)
    return kg(pullback(p, inv), mass_squared) == pullback(kg(p, mass_squared), inv)

def demo():
    p = {(3,1): Q(2), (0,2): Q(3), (1,0): Q(-1), (0,0): Q(7)}
    return {
        "field": "2*t^3*x + 3*x^2 - t + 7",
        "boost_v": "3/5",
        "kg_covariant": check_covariance(p),
        "operator": "box + m^2",
        "scope": "exact polynomial 1+1 scalar-field covariance; not universal physics"
    }

if __name__ == "__main__":
    import json
    print(json.dumps(demo(), sort_keys=True))
