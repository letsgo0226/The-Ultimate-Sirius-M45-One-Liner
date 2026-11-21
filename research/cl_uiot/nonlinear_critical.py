"""Exact directional Taylor jets and quadratic stable graph."""
from fractions import Fraction as Q
from math import comb
from universal_pauli import coefficients,weights

def jet(w,v):
    w=weights(w);v=tuple(map(Q,v))
    if len(v)!=4 or sum(v)!=0:raise ValueError("not a simplex tangent")
    out=[]
    for d in coefficients():
        a=[Q(0)]*6
        for k,c in d:
            b=[Q(c)]
            for x,y,m in zip(w,v,k):
                q=[Q(comb(m,j))*x**(m-j)*y**j for j in range(m+1)]
                z=[Q(0)]*(len(b)+len(q)-1)
                for i,u in enumerate(b):
                    for j,s in enumerate(q):z[i+j]+=u*s
                b=z
            for i,u in enumerate(b):a[i]+=u
        out.append(tuple(a))
    return tuple(out)

def radial_quadratic(w,v):
    return sum(a[2] for a in jet(w,v)[1:])

def stable_graph_coefficient(w,v):
    v=tuple(map(Q,v))
    if len(v)!=4 or v[0]!=0 or sum(v)!=0:raise ValueError("transverse tangent required")
    # Valid as the quadratic graph formula at the critical fixed point;
    # rational w permits evaluation of its polynomial extension.
    return -Q(3,5)*radial_quadratic(w,v)

def hessian_action(w,u,v):
    u,v=tuple(map(Q,u)),tuple(map(Q,v))
    a,b,c=jet(w,u),jet(w,v),jet(w,tuple(x+y for x,y in zip(u,v)))
    return tuple(z[2]-x[2]-y[2] for x,y,z in zip(a,b,c))
