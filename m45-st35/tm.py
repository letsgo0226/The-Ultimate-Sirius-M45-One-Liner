#!/usr/bin/env python3
"""ST35: generic single-tape runner of a checked-in fixed transition table."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DELTA=json.loads((ROOT/"delta.json").read_text())
def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()
def run(source,limit=1000):
    if not isinstance(source,str) or len(source)>1000 or any(c not in "@SK" for c in source):
        raise ValueError("invalid input")
    if type(limit) is not int or not 0<=limit<=10000:
        raise ValueError("invalid limit")
    cells={i:c for i,c in enumerate(source)}
    head=0
    state=DELTA["start"]
    trace=[]
    for _ in range(limit):
        if state in DELTA["halt"]:break
        symbol=cells.get(head,"_")
        rule=DELTA["transitions"].get(state,{}).get(symbol)
        if rule is None:
            return {"status":"REJECT","steps":len(trace),"trace":trace,"table_sha256":digest(DELTA)}
        write,move,nxt=rule
        trace.append([state,head,symbol,write,move,nxt])
        if write=="_":cells.pop(head,None)
        else:cells[head]=write
        head+={"L":-1,"R":1,"N":0}[move]
        state=nxt
    return {"status":"HALT" if state in DELTA["halt"] else "PAUSE",
            "steps":len(trace),"trace":trace,"table_sha256":digest(DELTA),
            "tape":"".join(cells.get(i,"_") for i in range(max(cells,default=-1)+1))}
def verify(source,cert):
    return cert==run(source,cert.get("steps",-1))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--expression",default="@@K@SK@KS")
    p.add_argument("--steps",type=int,default=1000)
    p.add_argument("--out",default="m45-st35-certificate.json")
    a=p.parse_args()
    result=run(a.expression,a.steps)
    Path(a.out).write_text(json.dumps({"input":a.expression,"result":result},indent=2)+"\n")
    print(canonical({"status":result["status"],"steps":result["steps"],"tape":result.get("tape")}))
