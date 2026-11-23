"""Finite capture in a proven invariant ratio cone."""
from fractions import Fraction as Q
from interval_basin import box,step,classify
from sync_capture import magnitudes

def capture(bounds,cap=4,digits=12):
    b=box(bounds)
    if type(cap) is not int or cap<0:raise ValueError("invalid cap")
    for n in range(cap+1):
        label=classify(b)
        if label:return {"status":label,"steps":n}
        a=magnitudes(b)
        m=min(v[0] for v in a)
        M=max(v[1] for v in a)
        if m>0 and 5*m*m>=3*M*M:
            return {"status":"invariant_cone","steps":n}
        if n<cap:b=step(b,digits)
    return {"status":"unknown","steps":cap}
