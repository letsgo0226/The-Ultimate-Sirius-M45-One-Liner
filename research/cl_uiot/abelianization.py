"""Exact D4 group extension coordinates; D4 has order eight."""
def check(g,limit):
    if not isinstance(g,tuple) or len(g)!=2 or any(type(x) is not int for x in g) or not 0<=g[0]<limit or g[1] not in (0,1):
        raise ValueError("group coordinates")
    return g

def multiply(g,h):
    a,b=check(g,4)
    c,d=check(h,4)
    return ((a+(-1)**b*c)%4,b^d)

def inverse(g):
    a,b=check(g,4)
    return ((-(-1)**b*a)%4,b)

def decompose(g):
    a,b=check(g,4)
    return (a%2,b),a//2

def reconstruct(q,k):
    a,b=check(q,2)
    if type(k) is not int or k not in (0,1):
        raise ValueError("kernel bit")
    return a+2*k,b

def cocycle(q,t):
    a,b=check(q,2)
    c,d=check(t,2)
    return ((a+(-1)**b*c)//2)%2

def extended_product(x,y):
    q,k=x
    t,l=y
    reconstruct(q,k)
    reconstruct(t,l)
    return (q[0]^t[0],q[1]^t[1]),k^l^cocycle(q,t)
