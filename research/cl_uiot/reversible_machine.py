"""Finite reversible binary tape machine and native Walsh signal update."""
from abelian_fourier import transform,inverse,checked

def validate(q,h,t):
    if type(q) is not int or q not in (0,1):
        raise ValueError("control")
    if not isinstance(t,tuple) or not 1<=len(t)<=4096 or len(t)&(len(t)-1):
        raise ValueError("tape size")
    if type(h) is not int or not 0<=h<len(t):
        raise ValueError("head")
    if any(type(b) is not int or b not in (0,1) for b in t):
        raise ValueError("binary tape")

def step(state):
    q,h,t=state
    validate(q,h,t)
    b=t[h]
    u=q^b
    a=t[:h]+(q,)+t[h+1:]
    return u,(h+1-2*u)%len(t),a

def backward(state):
    u,j,a=state
    validate(u,j,a)
    h=(j-1+2*u)%len(a)
    q=a[h]
    return q,h,a[:h]+(q^u,)+a[h+1:]

def encode(state):
    q,h,t=state
    validate(q,h,t)
    return q,h,transform(t)

def decode(state):
    q,h,w=state
    t=inverse(w)
    validate(q,h,t)
    return q,h,t

def spectral_step(state):
    q,h,w=state
    decode(state)  # validate complete encoded domain
    b=sum((-1)**((k&h).bit_count()%2)*v for k,v in enumerate(w))//len(w)
    u=q^b
    delta=q-b
    return u,(h+1-2*u)%len(w),tuple(v+delta*(-1)**((k&h).bit_count()%2) for k,v in enumerate(w))

def spectral_backward(state):
    u,j,w=state
    decode(state)
    h=(j-1+2*u)%len(w)
    q=sum((-1)**((k&h).bit_count()%2)*v for k,v in enumerate(w))//len(w)
    delta=(q^u)-q
    return q,h,tuple(v+delta*(-1)**((k&h).bit_count()%2) for k,v in enumerate(w))
