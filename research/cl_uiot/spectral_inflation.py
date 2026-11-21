"""Exact split-coordinate inflation on elementary abelian groups."""
from abelian_fourier import checked,transform,inverse

def pair(a,b):
    a,b=checked(a),checked(b)
    if len(a)!=len(b) or len(a)>2048:
        raise ValueError("incompatible blocks or dimension cap")
    return tuple(a),tuple(b)

def embed(a):
    a=checked(a)
    return join(a,[0]*len(a))

def join(a,b):
    a,b=pair(a,b)
    return a+b

def split(a):
    a=checked(a)
    if len(a)<2:
        raise ValueError("no extra dimension")
    n=len(a)//2
    return tuple(a[:n]),tuple(a[n:])

def spectral_join(a,b):
    a,b=pair(a,b)
    return tuple(x+y for x,y in zip(a,b))+tuple(x-y for x,y in zip(a,b))

def spectral_split(w):
    p,q=split(w)
    if any((x+y)%2 for x,y in zip(p,q)):
        raise ValueError("not an integral block spectrum")
    return tuple((x+y)//2 for x,y in zip(p,q)),tuple((x-y)//2 for x,y in zip(p,q))

def spectral_embed(w):
    w=checked(w)
    return spectral_join(w,[0]*len(w))

def recover(w):
    a,b=spectral_split(w)
    return inverse(a),inverse(b)
