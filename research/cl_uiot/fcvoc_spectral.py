"""Direct exact spectral update on valid encoded binary four-cell states."""
ROOTS=((1,0),(0,-1),(-1,0),(0,1))

def read(w,h):
    r=im=0
    for k,(a,b) in enumerate(w):
        c,d=ROOTS[(-k*h)%4]
        r+=a*c-b*d
        im+=a*d+b*c
    if im or r not in (0,4):
        raise ValueError("invalid binary cell")
    return r//4

def step(s,handedness=1):
    q,h,w=s
    if handedness not in (-1,1):
        raise ValueError("invalid handedness")
    if q==2:
        return s
    b=read(w,h)
    delta=1-2*b
    u=tuple((a+delta*c,b0+delta*d)
            for k,(a,b0) in enumerate(w)
            for c,d in (ROOTS[(k*h)%4],))
    return (2 if q==1 and b==1 else b,
            (h+handedness*delta)%4,u)
