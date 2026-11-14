#!/usr/bin/env python3
"""Execute ST34's fixed finite transition table for atomic K applications."""
import argparse
import hashlib
import json
from pathlib import Path

TABLE=json.loads(Path(__file__).with_name("delta.json").read_text())
def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def simulate(src,limit=100):
    if not isinstance(src,str) or len(src)>1000 or any(c not in "@SK" for c in src):
        raise ValueError("invalid input")
    if type(limit)!=int or not 0<=limit<=1000:
        raise ValueError("invalid budget")
    cells={i:c for i,c in enumerate(src)}
    state,head,trace=TABLE["start"],0,[]
    for _ in range(limit):
        if state in TABLE["halt"]:break
        read=cells.get(head,"_")
        rule=TABLE["transitions"].get(state,{}).get(read)
        if rule is None:
            return {"status":"REJECT","state":state,"head":head,"trace":trace,"table_sha256":digest(TABLE)}
        write,move,nxt=rule
        trace.append({"state":state,"head":head,"read":read,"write":write,"move":move,"next":nxt})
        if write=="_":cells.pop(head,None)
        else:cells[head]=write
        head+={"L":-1,"R":1,"N":0}[move]
        state=nxt
    return {"status":"HALT" if state in TABLE["halt"] else "PAUSE",
            "state":state,"head":head,"trace":trace,"table_sha256":digest(TABLE),
            "tape":"".join(cells.get(i,"_") for i in range(max(cells,default=-1)+1))}
def verify(src,cert):
    return cert==simulate(src,len(cert.get("trace",[])))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--expression",default="@@KSK")
    p.add_argument("--steps",type=int,default=100)
    p.add_argument("--out",default="m45-st34-certificate.json")
    a=p.parse_args()
    cert=simulate(a.expression,a.steps)
    Path(a.out).write_text(json.dumps({"input":a.expression,"result":cert},indent=2)+"\n")
    print(canonical({"status":cert["status"],"tape":cert.get("tape"),"steps":len(cert["trace"])}))
