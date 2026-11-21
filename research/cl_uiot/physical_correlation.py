"""Exact affine Bloch hull of a box intersected with the simplex."""
from fractions import Fraction as Q
from interval_basin import box,step
from simplex_tightening import tighten

def bloch_hull(bounds):
    b=box(bounds)
    out=[]
    for i,j in ((2,3),(1,3),(1,2)):
        k,l=tuple(t for t in range(4) if t not in (i,j))
        lo=max(b[i][0]+b[j][0],1-b[k][1]-b[l][1])
        hi=min(b[i][1]+b[j][1],1-b[k][0]-b[l][0])
        out.append((1-2*hi,1-2*lo))
    return tuple(out)

def magnitudes(bounds):
    return tuple((Q(0) if lo<=0<=hi else min(abs(lo),abs(hi)),max(abs(lo),abs(hi)))
                 for lo,hi in bloch_hull(bounds))

def capture(bounds,cap=1,digits=12):
    b=tighten(bounds)
    if type(cap) is not int or cap<0:raise ValueError("invalid cap")
    for n in range(cap+1):
        for i,(lo,hi) in enumerate(b):
            if lo>Q(9,10):return {"status":"IXYZ"[i],"steps":n}
        a=magnitudes(b);m=min(v[0] for v in a);M=max(v[1] for v in a)
        if M*M<Q(2,3):return {"status":"uniform","steps":n}
        if m>0 and 5*m*m>=3*M*M:return {"status":"invariant_cone","steps":n}
        if n<cap:b=tighten(step(b,digits))
    return {"status":"unknown","steps":cap}
