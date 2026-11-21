"""Exact polynomial calculus on finite involutions."""
from fractions import Fraction as Q
from symbolic_algebra import normalize
from inflation_coefficients import involution,identity,mul
from direct_limit import apply as direct_apply

def reduce_expr(expr):
    c=normalize(expr)
    return sum(c[::2],Q(0)),sum(c[1::2],Q(0))

def evaluate(expr,t):
    t=involution(t)
    a,b=reduce_expr(expr)
    return tuple(tuple(a*(i==j)+b*v for j,v in enumerate(row)) for i,row in enumerate(t))

def reference(expr,t):
    t=involution(t)
    c=normalize(expr)
    u=tuple(tuple(Q(0) for _ in t) for _ in t)
    for a in reversed(c):
        u=mul(u,t)
        u=tuple(tuple(v+a*(i==j) for j,v in enumerate(row)) for i,row in enumerate(u))
    return u

def apply_prefix(expr,values):
    w=direct_apply(values)
    a,b=reduce_expr(expr)
    return tuple(a*Q(x)+b*y for x,y in zip(values,w))

def verify(expr,t,result):
    try:
        if type(result) is not tuple or any(type(row) is not tuple or any(type(v) is not Q for v in row) for row in result):
            return False
        return result==reference(expr,t)
    except (ValueError,TypeError,OverflowError):
        return False
