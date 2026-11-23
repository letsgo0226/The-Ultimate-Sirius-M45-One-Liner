"""Bounded full-simplex experiment, with exact replay."""
from collections import Counter
from global_entry import cover,verify

def experiment(budget=127,depth=6,cap=1,digits=12):
    r=cover(((0,1),)*4,budget,depth,cap,digits)
    if not verify(r):raise ArithmeticError("replay failed")
    counts=dict(Counter(v[2] for v in r["leaves"]))
    return {"used":r["used"],"counts":counts,"complete":r["complete"],
            "unresolved":tuple(v[0] for v in r["leaves"] if v[2]=="unknown")}

if __name__=="__main__":
    import json
    print(json.dumps(experiment(),default=str))
