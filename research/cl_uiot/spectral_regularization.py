"""Exact rational spectral resolvent and regularized poles of cube graphs."""
from fractions import Fraction as Q
from abelian_fourier import checked,transform

def eigenvalues(f):
    return tuple(2*k.bit_count() for k in range(len(checked(f))))

def rational_inverse(w):
    a=list(map(Q,w))
    h=1
    while h<len(a):
        for i in range(0,len(a),2*h):
            for j in range(i,i+h):
                x,y=a[j],a[j+h]
                a[j],a[j+h]=x+y,x-y
        h*=2
    return tuple(x/len(a) for x in a)

def project(f,lam):
    w=transform(f)
    return rational_inverse([v if e==lam else 0 for v,e in zip(w,eigenvalues(f))])

def resolvent(f,z):
    z=Q(z)
    w=transform(f)
    e=eigenvalues(f)
    if z in e:
        raise ValueError("spectral pole")
    return rational_inverse([Q(v)/(l-z) for v,l in zip(w,e)])

def regularized(f,lam,z):
    lam,z=Q(lam),Q(z)
    e=eigenvalues(f)
    if lam not in e:
        raise ValueError("target must be eigenvalue")
    if z==lam:
        return project(f,lam)
    return tuple((lam-z)*v for v in resolvent(f,z))

def decompose(f):
    n=len(checked(f)).bit_length()-1
    return tuple(project(f,2*j) for j in range(n+1))
