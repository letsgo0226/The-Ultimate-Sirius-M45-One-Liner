"""Finite-step capture certificates using physical probability boxes."""
from fractions import Fraction as Q
from interval_basin import box,step,classify

def magnitudes(bounds):
    b=box(bounds)
    out=[]
    for i,j in ((2,3),(1,3),(1,2)):
        lo=1-2*(b[i][1]+b[j][1])
        hi=1-2*(b[i][0]+b[j][0])
        lower=0 if lo<=0<=hi else min(abs(lo),abs(hi))
        out.append((Q(lower),min(Q(1),max(abs(lo),abs(hi)))))
    return tuple(out)

def capture(bounds,cap=4,digits=12):
    b=box(bounds)
    if type(cap) is not int or cap<0:raise ValueError("invalid cap")
    for n in range(cap+1):
        label=classify(b)
        if label:return {"status":label,"steps":n}
        a=magnitudes(b)
        m=min(v[0] for v in a)
        M=max(v[1] for v in a)
        if m>0 and 5*m*m>=3*M**4:
            return {"status":"cone_entry","steps":n}
        if n<cap:b=step(b,digits)
    return {"status":"unknown","steps":cap}
