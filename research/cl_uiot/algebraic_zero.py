"""Exact roots of (s-1/2)^2+c, with nonnegative rational c."""
from fractions import Fraction as Q
from exact_zero import matrix_residual

def coefficient(c):
    if type(c) not in (int,Q) or c<0:
        raise ValueError("nonnegative exact rational required")
    return Q(c)

def roots(c):
    c=coefficient(c)
    # (real part, imaginary sign, squared imaginary magnitude, multiplicity)
    if c==0:
        return ((Q(1,2),0,Q(0),2),)
    return ((Q(1,2),-1,c,1),(Q(1,2),1,c,1))

def residual_at(c,root):
    c=coefficient(c)
    a,b,d,m=root
    if type(a) not in (int,Q) or type(b) is not int or b not in (-1,0,1):
        raise ValueError("invalid root coordinates")
    d=coefficient(d)
    if (b==0)!=(d==0):
        raise ValueError("noncanonical radical")
    x=Q(a)-Q(1,2)
    # Real part and coefficient of i*sqrt(d).
    return x*x-b*b*d+c,2*x*b

def verify(c,root):
    c=coefficient(c)
    if type(root) is not tuple or len(root)!=4 or tuple(map(type,root))!=(Q,int,Q,int):
        return False
    if residual_at(c,root)!=(0,0):
        return False
    return root in roots(c)

def matrix_roots(lam,mu):
    return roots(matrix_residual(lam,mu))
