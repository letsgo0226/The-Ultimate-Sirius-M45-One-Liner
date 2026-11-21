"""Matched hybrid cover with cumulative residual refinement."""
from collections import Counter,deque
from fractions import Fraction as Q
from interval_basin import box,split
from simplex_tightening import tighten,capture_tight
from physical_correlation import magnitudes
from polynomial_enclosure import enhanced_step

def capture_hybrid(bounds,cap=1,digits=12):
    b=tighten(bounds)
    if type(cap) is not int or cap<0:raise ValueError("invalid cap")
    for n in range(cap+1):
        for i,(lo,hi) in enumerate(b):
            if lo>Q(9,10):return "IXYZ"[i]
        a=magnitudes(b);m=min(v[0] for v in a);M=max(v[1] for v in a)
        if M*M<Q(2,3):return "uniform"
        if m>0 and 5*m*m>=3*M*M:return "invariant_cone"
        if n<cap:b=enhanced_step(b,digits)
    return "unknown"

def initial():
    return ((box(((0,1),)*4),0,"unknown","unknown"),)

def refine(leaves,budget=255,depth=8,cap=1,digits=12):
    if any(type(v) is not int or v<0 for v in (budget,depth,cap)):
        raise ValueError("invalid limits")
    if type(digits) is not int or not 1<=digits<=100:raise ValueError("invalid precision")
    todo=deque(leaves);out=[];used=0
    while todo and used<budget:
        b,d,a,h=todo.popleft()
        if a!="unknown" or h!="unknown":
            out.append((b,d,a,h));continue
        a=capture_tight(b,cap,digits)["status"]
        h=capture_hybrid(b,cap,digits)
        used+=1
        if a!="unknown" or h!="unknown" or d>=depth or all(l==u for l,u in b):
            out.append((b,d,a,h))
        else:todo.extend((c,d+1,"unknown","unknown") for c in split(b))
    out.extend(todo)
    return {"leaves":tuple(out),"used":used,
            "baseline":dict(Counter(v[2] for v in out)),
            "hybrid":dict(Counter(v[3] for v in out)),
            "complete":all(v[2]!="unknown" or v[3]!="unknown" for v in out)}
