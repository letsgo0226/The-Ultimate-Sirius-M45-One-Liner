"""Bounded, pure four-cell machine with exact spectral representation."""
from fcvoc import fourier, inverse, mirror

# state = (control bit, head index, four binary cells)
def step(s, handedness=1):
    q,h,t=s
    if q==2:
        return s
    b=t[h]
    u=list(t)
    u[h]=1-b
    return (2 if q==1 and b==1 else b,
            (h+handedness*(1 if b==0 else -1))%4,tuple(u))

def reflect(s):
    q,h,t=s
    return q,(-h)%4,mirror(t)

def encode(s):
    q,h,t=s
    return q,h,fourier(t)

def decode(s):
    q,h,w=s
    return q,h,inverse(w)

def spectral_step(s, handedness=1):
    return encode(step(decode(s),handedness))

def run(s, steps, handedness=1):
    if type(steps) is not int or not 0<=steps<=1024:
        raise ValueError("step budget must be 0..1024")
    for _ in range(steps):
        if s[0]==2:
            break
        s=step(s,handedness)
    return s
