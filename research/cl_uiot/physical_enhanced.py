"""Matched-partition comparison of physical interval tightening."""
from collections import Counter,deque
from interval_basin import box,split
from invariant_capture import capture
from simplex_tightening import capture_tight

def compare(bounds=((0,1),)*4,budget=255,depth=8,cap=1,digits=12):
    if any(type(v) is not int or v<0 for v in (budget,depth,cap)):
        raise ValueError("invalid limits")
    if type(digits) is not int or not 1<=digits<=100:
        raise ValueError("invalid precision")
    todo=deque([(box(bounds),0)])
    leaves=[]
    used=0
    while todo and used<budget:
        b,d=todo.popleft()
        old=capture(b,cap,digits)["status"]
        new=capture_tight(b,cap,digits)["status"]
        used+=1
        if old!="unknown" or new!="unknown" or d==depth or all(l==h for l,h in b):
            leaves.append((b,old,new))
        else:todo.extend((c,d+1) for c in split(b))
    leaves.extend((b,"unknown","unknown") for b,d in todo)
    return {"used":used,"leaves":tuple(leaves),
            "baseline":dict(Counter(v[1] for v in leaves)),
            "tightened":dict(Counter(v[2] for v in leaves)),
            "combined_complete":all(a!="unknown" or b!="unknown" for _,a,b in leaves)}
