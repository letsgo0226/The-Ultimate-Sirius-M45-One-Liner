"""Budgeted, replayable cover by finite convergence certificates."""
from collections import deque
from interval_basin import box,split
from invariant_capture import capture

def cover(bounds,budget=31,depth=4,cap=2,digits=12):
    root=box(bounds)
    if any(type(v) is not int or v<0 for v in (budget,depth,cap)):
        raise ValueError("invalid limits")
    if type(digits) is not int or not 1<=digits<=100:
        raise ValueError("invalid precision")
    todo=deque([(root,0)])
    leaves=[]
    used=0
    while todo and used<budget:
        b,d=todo.popleft()
        r=capture(b,cap,digits)
        used+=1
        if r["status"]!="unknown":
            leaves.append((b,d,r["status"],r["steps"]))
        elif d<depth and any(lo<hi for lo,hi in b):
            todo.extend((c,d+1) for c in split(b))
        else:leaves.append((b,d,"unknown",cap))
    leaves.extend((b,d,"unknown",None) for b,d in todo)
    return {"root":root,"budget":budget,"depth":depth,"cap":cap,
            "digits":digits,"used":used,"leaves":tuple(leaves),
            "complete":all(v[2]!="unknown" for v in leaves)}

def verify(record):
    return record==cover(record["root"],record["budget"],record["depth"],
                         record["cap"],record["digits"])
