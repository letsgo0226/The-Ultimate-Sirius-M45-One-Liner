"""Exact quadratic-field arithmetic and critical directional jets."""
from fractions import Fraction as Q
from math import comb
from universal_pauli import coefficients

class K:
    def __init__(self,a=0,b=0):
        self.a,self.b=Q(a),Q(b)
    def __add__(self,y):
        y=lift(y);return K(self.a+y.a,self.b+y.b)
    __radd__=__add__
    def __neg__(self):return K(-self.a,-self.b)
    def __sub__(self,y):return self+-lift(y)
    def __mul__(self,y):
        y=lift(y);return K(self.a*y.a+6*self.b*y.b,self.a*y.b+self.b*y.a)
    __rmul__=__mul__
    def __pow__(self,n):
        if type(n) is not int or n<0:raise ValueError("nonnegative exponent required")
        a=K(1)
        for _ in range(n):a=a*self
        return a
    def __eq__(self,y):
        y=lift(y);return (self.a,self.b)==(y.a,y.b)
    def __repr__(self):return f"K({self.a},{self.b})"

def lift(x):return x if isinstance(x,K) else K(x)
def critical():
    p=K(Q(3,4),Q(-1,4));return (K(1)-p,)+(p*Q(1,3),)*3

def jet(v):
    v=tuple(map(lift,v))
    if len(v)!=4 or sum(v)!=0:raise ValueError("invalid tangent")
    out=[]
    for d in coefficients():
        a=[K() for _ in range(6)]
        for k,c in d:
            b=[K(c)]
            for x,y,m in zip(critical(),v,k):
                q=[comb(m,j)*x**(m-j)*y**j for j in range(m+1)]
                z=[K() for _ in range(len(b)+len(q)-1)]
                for i,u in enumerate(b):
                    for j,s in enumerate(q):z[i+j]=z[i+j]+u*s
                b=z
            for i,u in enumerate(b):a[i]=a[i]+u
        out.append(tuple(a))
    return tuple(out)

def radial_quadratic(v):
    v=tuple(map(lift,v))
    if len(v)!=4 or v[0]!=0 or sum(v)!=0:raise ValueError("transverse tangent required")
    return sum(a[2] for a in jet(v)[1:])

def curvature(v):return Q(-3,5)*radial_quadratic(v)
