"""Exact coordinate hull on the physical probability simplex."""
from fractions import Fraction as Q
from interval_basin import box,step
from invariant_capture import capture

def tighten(bounds):
    b=box(bounds)
    return box(tuple((max(lo,1-sum(v[1] for j,v in enumerate(b) if j!=i)),
                      min(hi,1-sum(v[0] for j,v in enumerate(b) if j!=i)))
                     for i,(lo,hi) in enumerate(b)))

def capture_tight(bounds,cap=1,digits=12):
    b=tighten(bounds)
    if type(cap) is not int or cap<0:raise ValueError("invalid cap")
    for n in range(cap+1):
        r=capture(b,0,digits)
        if r["status"]!="unknown":return {"status":r["status"],"steps":n}
        if n<cap:b=tighten(step(b,digits))
    return {"status":"unknown","steps":cap}
