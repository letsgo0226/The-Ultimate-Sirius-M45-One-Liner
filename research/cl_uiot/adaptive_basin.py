"""Budgeted coverage and deterministic replay verification."""
from collections import deque
from interval_basin import box,certify,split

def cover(bounds=((0,1),)*4,budget=64,depth=8,cap=3,digits=12):
    if any(type(x) is not int or x<0 for x in (budget,depth,cap)):raise ValueError("invalid budget")
    root=box(bounds)
    queue=deque([(root,0)])
    leaves=[]
    used=0
    while queue and used<budget:
        b,d=queue.popleft()
        r=certify(b,cap,digits)
        used+=1
        if r["basin"] is not None:
            leaves.append((b,d,r["basin"],r["steps"]))
        elif d>=depth or all(lo==hi for lo,hi in b):
            leaves.append((b,d,None,None))
        else:
            queue.extend((c,d+1) for c in split(b))
    leaves.extend((b,d,None,None) for b,d in queue)
    return {"root":root,"budget":budget,"depth":depth,"cap":cap,"digits":digits,
            "used":used,"leaves":tuple(leaves)}

def verify(record):
    try:
        return cover(record["root"],record["budget"],record["depth"],
                     record["cap"],record["digits"])==record
    except (ValueError,TypeError,KeyError,ArithmeticError):return False

def counts(record):
    out={k:0 for k in ("I","X","Y","Z","uniform",None)}
    for _,_,label,_ in record["leaves"]:out[label]+=1
    return out
