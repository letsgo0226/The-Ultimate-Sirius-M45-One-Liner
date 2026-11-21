"""Cumulative refinement of unresolved convergence boxes."""
from global_entry import cover
from interval_basin import box

def initial(bounds=((0,1),)*4):
    return ((box(bounds),0,"unknown",None),)

def refine(leaves,budget=31,depth=4,cap=1,digits=12):
    if any(type(v) is not int or v<0 for v in (budget,depth,cap)):
        raise ValueError("invalid limits")
    if type(digits) is not int or not 1<=digits<=100:
        raise ValueError("invalid precision")
    out=[]
    used=0
    for b,d,label,n in leaves:
        if label!="unknown" or used>=budget:
            out.append((b,d,label,n))
            continue
        r=cover(b,budget-used,depth,cap,digits)
        used+=r["used"]
        out.extend((c,d+e,s,t) for c,e,s,t in r["leaves"])
    return {"leaves":tuple(out),"used":used,
            "complete":all(v[2]!="unknown" for v in out)}
