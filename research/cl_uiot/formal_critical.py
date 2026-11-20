"""Truncated bivariate formal stable graph over Q(sqrt(6))."""
from fractions import Fraction as Q
from algebraic_curvature import K,critical
from universal_pauli import coefficients

def add(*ps):
    r={}
    for p in ps:
        for k,c in p.items():r[k]=r.get(k,K())+c
    return {k:c for k,c in r.items() if c!=0}

def scale(p,c):return {k:v*c for k,v in p.items() if v*c!=0}

def mul(p,q,n):
    r={}
    for (i,j),a in p.items():
        for (k,l),b in q.items():
            if i+j+k+l<=n:
                key=(i+k,j+l);r[key]=r.get(key,K())+a*b
    return {k:c for k,c in r.items() if c!=0}

def power(p,k,n):
    r={(0,0):K(1)}
    for _ in range(k):r=mul(r,p,n)
    return r

def compose(h,x,y,n):
    return add(*(scale(mul(power(x,i,n),power(y,j,n),n),c) for (i,j),c in h.items()))

def residual(h,n):
    u={(1,0):K(1)};v={(0,1):K(1)}
    w=critical()
    inp=[add({(0,0):w[0]},scale(h,-1))]
    for i,t in enumerate((u,v,scale(add(u,v),-1)),1):
        inp.append(add({(0,0):w[i]},scale(h,Q(1,3)),t))
    powers=[[power(p,k,n) for k in range(6)] for p in inp]
    out=[]
    for d in coefficients()[1:]:
        terms=[]
        for k,c in d:
            a={(0,0):K(c)}
            for i,j in enumerate(k):a=mul(a,powers[i][j],n)
            terms.append(a)
        out.append(add(*terms))
    total=add(*out)
    r=add(total,{(0,0):-sum(w[1:])})
    x,y=[add(p,scale(total,Q(-1,3))) for p in out[:2]]
    return add(r,scale(compose(h,x,y,n),-1))

def graph(n):
    if type(n) is not int or n<2:raise ValueError("order >=2 required")
    h={}
    for k in range(2,n+1):
        e=residual(h,k)
        h=add(h,scale({ij:c for ij,c in e.items() if sum(ij)==k},Q(-3,5)))
    if residual(h,n):raise ArithmeticError("invariance residual")
    return h
